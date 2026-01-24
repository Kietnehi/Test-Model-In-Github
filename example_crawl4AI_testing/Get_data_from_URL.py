import asyncio
import json
import hashlib
from urllib.parse import urlparse, urlunparse
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.async_dispatcher import MemoryAdaptiveDispatcher
# --- THÊM CÁC IMPORT SAU ---
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

def normalize_url(url):
    """Chuẩn hóa URL để tránh trùng lặp kỹ thuật"""
    parsed = urlparse(url)
    path = parsed.path.rstrip('/')
    return urlunparse((parsed.scheme.lower(), parsed.netloc.lower(), path, '', '', ''))

async def crawl_full_website(base_url: str):
    # 1. Cấu hình bộ lọc nội dung (Lọc bỏ Menu, Footer, Sidebar)
    # Threshold 0.45 là mức trung bình, giúp giữ lại bài viết chính.
    prune_filter = PruningContentFilter(
        threshold=0.45, 
        threshold_type="dynamic", 
        min_word_threshold=5
    )
    
    # 2. Tạo Markdown Generator sử dụng bộ lọc trên
    md_generator = DefaultMarkdownGenerator(content_filter=prune_filter)

    # 3. Cấu hình Trình duyệt
    browser_config = BrowserConfig(
        headless=True,
        enable_stealth=True,
        browser_type="chromium"
    )

    # 4. Cấu hình Chạy (Quan trọng: Phải gán md_generator vào đây)
    run_config = CrawlerRunConfig(
        cache_mode=CacheMode.ENABLED,
        markdown_generator=md_generator, # Kích hoạt fit_markdown
        word_count_threshold=10,
        process_iframes=True
    )

    async with AsyncWebCrawler(config=browser_config) as crawler:
        # --- BƯỚC 1: KHÁM PHÁ URL ---
        print(f"--- Đang phân tích cấu trúc trang: {base_url} ---")
        discovery_result = await crawler.arun(url=base_url, config=run_config)
        
        if not discovery_result.success:
            print(f"Lỗi: {discovery_result.error_message}")
            return

        raw_links = discovery_result.links.get("internal", [])
        urls_to_crawl = list(set(normalize_url(link['href']) for link in raw_links if link.get('href')))
        
        print(f"Tìm thấy {len(urls_to_crawl)} URL duy nhất sau khi chuẩn hóa.")

        # --- BƯỚC 2: QUÉT HÀNG LOẠT ---
        dispatcher = MemoryAdaptiveDispatcher(
            memory_threshold_percent=80.0,
            max_session_permit=15
        )

        print(f"--- Đang bắt đầu quét dữ liệu chi tiết ---")
        results = await crawler.arun_many(
            urls=urls_to_crawl,
            config=run_config,
            dispatcher=dispatcher
        )

        # --- BƯỚC 3: TỔNG HỢP VÀ LỌC TRÙNG NỘI DUNG ---
        final_dataset = []
        seen_content_hashes = set()

        for result in results:
            if result.success:
                # Ưu tiên lấy fit_markdown (Dữ liệu đã sạch Menu/Sidebar)
                content = result.markdown.fit_markdown
                
                # Nếu lọc quá gắt dẫn đến rỗng, lấy raw làm dự phòng
                if not content:
                    content = result.markdown.raw_markdown
                
                if not content: continue

                # Hash dựa trên nội dung bài viết ĐÃ LỌC
                content_hash = hashlib.md5(content.encode('utf-8')).hexdigest()

                if content_hash not in seen_content_hashes:
                    seen_content_hashes.add(content_hash)
                    final_dataset.append({
                        "url": result.url,
                        "content_hash": content_hash,
                        "content": content,
                        "metadata": result.metadata
                    })
                else:
                    print(f"Bỏ qua URL trùng nội dung bài viết: {result.url}")

        # Lưu vào file JSON
        with open("clean_fit_data.json", "w", encoding="utf-8") as f:
            json.dump(final_dataset, f, ensure_ascii=False, indent=2)

        print(f"--- HOÀN THÀNH ---")
        print(f"Đã lưu {len(final_dataset)} trang 'sạch' vào file clean_fit_data.json")

if __name__ == "__main__":
    target_site = "https://vnexpress.net/" 
    asyncio.run(crawl_full_website(target_site))