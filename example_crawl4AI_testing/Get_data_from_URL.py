import asyncio
import json
import hashlib
from urllib.parse import urlparse, urlunparse
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.async_dispatcher import MemoryAdaptiveDispatcher
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

def normalize_url(url):
    """Chuẩn hóa URL: bỏ query param, bỏ fragment, bỏ slash cuối"""
    parsed = urlparse(url)
    # Chỉ giữ lại scheme, netloc và path để tránh trùng lặp do query string
    path = parsed.path.rstrip('/')
    return urlunparse((parsed.scheme.lower(), parsed.netloc.lower(), path, '', '', ''))

def is_internal_link(base_url, target_url):
    """Kiểm tra xem link có thuộc cùng domain không"""
    base_domain = urlparse(base_url).netloc
    target_domain = urlparse(target_url).netloc
    return base_domain == target_domain

async def crawl_full_website_deep(base_url: str, max_depth=2):
    # 1. Cấu hình Content Filter & Markdown
    prune_filter = PruningContentFilter(
        threshold=0.45,
        threshold_type="dynamic",
        min_word_threshold=5
    )
    md_generator = DefaultMarkdownGenerator(content_filter=prune_filter)

    # 2. Cấu hình Browser
    browser_config = BrowserConfig(
        headless=True,
        enable_stealth=True, 
        browser_type="chromium",
        verbose=False 
    )

    # 3. Cấu hình Run
    run_config = CrawlerRunConfig(
        cache_mode=CacheMode.ENABLED,
        markdown_generator=md_generator,
        word_count_threshold=10,
        process_iframes=True,
        check_robots_txt=True,
        magic=True,
    )

    # Quản lý hàng đợi URL
    visited_urls = set()
    urls_to_crawl = {normalize_url(base_url)}
    final_dataset = []
    
    # Dispatcher cho quét song song
    dispatcher = MemoryAdaptiveDispatcher(
        memory_threshold_percent=85.0,
        max_session_permit=10, 
        rate_limiter=None 
    )

    async with AsyncWebCrawler(config=browser_config) as crawler:
        current_depth = 0
        
        while current_depth <= max_depth and urls_to_crawl:
            print(f"\n--- ĐANG QUÉT ĐỘ SÂU {current_depth} (Số lượng URL: {len(urls_to_crawl)}) ---")
            
            # Lọc ra các URL chưa từng ghé thăm
            batch_urls = [u for u in urls_to_crawl if u not in visited_urls]
            
            if not batch_urls:
                break

            # Đánh dấu đã ghé thăm
            for u in batch_urls:
                visited_urls.add(u)

            # Thực hiện quét hàng loạt
            results = await crawler.arun_many(
                urls=batch_urls,
                config=run_config,
                dispatcher=dispatcher
            )

            # Tập hợp URL mới cho vòng lặp sau
            new_urls = set()

            for result in results:
                if not result.success:
                    print(f"Lỗi tại {result.url}: {result.error_message}")
                    continue

                # --- XỬ LÝ NỘI DUNG ---
                content = result.markdown.fit_markdown or result.markdown.raw_markdown
                if content:
                    content_hash = hashlib.md5(content.encode('utf-8')).hexdigest()
                    if not any(d['content_hash'] == content_hash for d in final_dataset):
                        final_dataset.append({
                            "url": result.url,
                            "depth": current_depth,
                            "title": result.metadata.get("title", ""),
                            "content_hash": content_hash,
                            "content": content
                        })

                # --- TRÍCH XUẤT LINK MỚI (Cho vòng lặp sau) ---
                if current_depth < max_depth:
                    internal_links = result.links.get("internal", [])
                    
                    # [ĐÃ CHỈNH SỬA] Đã xóa phần ignored_extensions
                    for link in internal_links:
                        href = link.get('href')
                        if href:
                            normalized = normalize_url(href)
                            
                            # Chỉ thêm nếu chưa visit và là link nội bộ
                            if (normalized not in visited_urls and 
                                is_internal_link(base_url, normalized)):
                                new_urls.add(normalized)
            
            # Cập nhật danh sách cần quét cho vòng lặp kế tiếp
            urls_to_crawl = new_urls
            current_depth += 1

    # Lưu kết quả
    with open("crawled_data_deep.json", "w", encoding="utf-8") as f:
        json.dump(final_dataset, f, ensure_ascii=False, indent=2)
    
    print(f"\n--- HOÀN THÀNH ---")
    print(f"Tổng số trang đã quét: {len(visited_urls)}")
    print(f"Tổng số bài viết lưu trữ: {len(final_dataset)}")

if __name__ == "__main__":
    asyncio.run(crawl_full_website_deep("https://docs.crawl4ai.com", max_depth=1))