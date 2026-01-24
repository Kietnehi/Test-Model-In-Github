import asyncio
import json
import hashlib
import re
from urllib.parse import urlparse, urlunparse
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.async_dispatcher import MemoryAdaptiveDispatcher
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

def normalize_url(url):
    """Chuẩn hóa URL để tránh trùng lặp và loại bỏ rác"""
    try:
        parsed = urlparse(url)
        path = parsed.path.rstrip('/')
        return urlunparse((parsed.scheme.lower(), parsed.netloc.lower(), path, '', '', ''))
    except:
        return url

async def universal_crawler_engine(base_url: str):
    # --- 1. THIẾT LẬP BỘ LỌC THÔNG MINH (Dùng cho mọi web) ---
    # Bộ lọc này tự tính toán mật độ văn bản để tìm ra bài viết chính
    prune_filter = PruningContentFilter(
        threshold=0.48,           # Ngưỡng tối ưu cho hầu hết các trang tin/blog
        threshold_type="dynamic", # Tự thích nghi với từng cấu trúc web khác nhau
        min_word_threshold=15     # Bỏ qua các khối văn bản quá ngắn
    )
    md_generator = DefaultMarkdownGenerator(content_filter=prune_filter)

    # --- 2. CẤU HÌNH TRÌNH DUYỆT (Tàng hình & Đa năng) ---
    browser_config = BrowserConfig(
        headless=True,
        enable_stealth=True,
        browser_type="chromium",
        user_agent_mode="random"  # Mỗi lần chạy giả danh một trình duyệt khác nhau
    )

    # --- 3. CẤU HÌNH CHẠY (Cuộn trang & Vượt rào) ---
    run_config = CrawlerRunConfig(
        cache_mode=CacheMode.ENABLED,
        markdown_generator=md_generator,
        magic=True,               # Tự động vượt qua các bẫy chặn bot
        scan_full_page=True,      # Cuộn xuống để load hết link ẩn/nội dung động
        scroll_delay=0.5,
        word_count_threshold=30   # Chỉ lấy những trang có nội dung thực sự
    )

    async with AsyncWebCrawler(config=browser_config) as crawler:
        # BƯỚC A: KHÁM PHÁ MỌI LINK
        print(f"🔍 Đang thám hiểm hệ thống link của: {base_url}")
        initial_res = await crawler.arun(url=base_url, config=run_config)
        
        if not initial_res.success:
            print(f"❌ Không thể truy cập trang web này: {initial_res.error_message}")
            return

        # Lấy tất cả link nội bộ
        internal_links = initial_res.links.get("internal", [])
        
        # Lọc URL: Loại bỏ các link chắc chắn là rác (ảnh, css, js, login, logout)
        exclude_patterns = [r'\.(jpg|png|pdf|zip|css|js)$', r'/(login|logout|signin|signup)', r'#']
        
        urls_to_crawl = []
        for link in internal_links:
            href = link.get('href')
            if href and not any(re.search(p, href, re.IGNORECASE) for p in exclude_patterns):
                urls_to_crawl.append(normalize_url(href))
        
        urls_to_crawl = list(set(urls_to_crawl)) # Chỉ giữ lại các URL duy 
        urls_to_crawl = urls_to_crawl[:100]
        print(f"✅ Tìm thấy {len(urls_to_crawl)} trang tiềm năng để quét sạch.")

        # BƯỚC B: TỔNG TẤN CÔNG (Quét hàng loạt)
        # Sử dụng tối đa 5 tab để không làm website mục tiêu "phát hoảng" mà chặn bạn
        dispatcher = MemoryAdaptiveDispatcher(
            memory_threshold_percent=75.0,
            max_session_permit=5 
        )

        print(f"🚀 Bắt đầu hút dữ liệu hàng loạt...")
        results = await crawler.arun_many(
            urls=urls_to_crawl,
            config=run_config,
            dispatcher=dispatcher
        )

        # BƯỚC C: TỔNG HỢP & LỌC TRÙNG NỘI DUNG TUYỆT ĐỐI
        final_data = []
        seen_hashes = set()

        for res in results:
            if res.success:
                # Lấy nội dung đã được bộ lọc thông minh làm sạch
                content = res.markdown.fit_markdown or res.markdown.raw_markdown
                if not content or len(content) < 100: continue # Bỏ qua trang quá ít chữ

                # Tạo vân tay nội dung để đảm bảo không lưu trùng dù URL khác nhau
                c_hash = hashlib.md5(content.encode('utf-8')).hexdigest()
                
                if c_hash not in seen_hashes:
                    seen_hashes.add(c_hash)
                    final_data.append({
                        "url": res.url,
                        "title": res.metadata.get('title', 'No Title'),
                        "content": content,
                        "hash": c_hash
                    })

        # XUẤT KẾT QUẢ
        domain_name = urlparse(base_url).netloc.replace('.', '_')
        output_file = f"scraped_{domain_name}.json"
        
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(final_data, f, ensure_ascii=False, indent=2)

        print(f"🎉 HOÀN THÀNH! Đã quét sạch {len(final_data)} trang chất lượng.")
        print(f"📂 Dữ liệu nằm tại file: {output_file}")

if __name__ == "__main__":
    # Bạn chỉ cần đổi link ở đây là nó sẽ tự quét sạch web đó
    target_url = "https://vnexpress.net/" 
    asyncio.run(universal_crawler_engine(target_url))