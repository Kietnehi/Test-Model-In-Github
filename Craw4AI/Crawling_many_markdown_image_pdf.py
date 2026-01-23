import asyncio
import re
import base64 # Cần import thêm thư viện này để giải mã ảnh
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode

# Hàm tạo tên file an toàn (đã bỏ phần thêm đuôi.md ở đây để dùng chung cho nhiều định dạng)
def clean_filename(url):
    # Lấy tên file tối đa 50 ký tự, loại bỏ ký tự đặc biệt
    clean_name = re.sub(r'[\\/*?:"<>|]', "", url.split("//")[-1])[:50]
    return clean_name

async def main():
    urls = [
        "https://vnexpress.net/tin-tuc-24h",
        "https://dantri.com.vn/su-kien.htm"
    ]

    # Cấu hình: BẬT thêm pdf và screenshot
    run_cfg = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS, 
        stream=True,
        pdf=True,        # <--- Yêu cầu xuất PDF
        screenshot=True  # <--- Yêu cầu chụp màn hình
    )

    async with AsyncWebCrawler() as crawler:
        # Duyệt qua từng kết quả ngay khi tải xong
        async for result in await crawler.arun_many(urls, config=run_cfg):
            if result.success:
                # 1. Tạo tên file cơ sở (không có đuôi file)
                base_name = clean_filename(result.url)
                print(f"💾 Đang xử lý: {base_name}...")
                
                # 2. Lưu nội dung Markdown (.md)
                with open(f"{base_name}.md", "w", encoding="utf-8") as f:
                    f.write(f"# URL: {result.url}\n\n")
                    f.write(result.markdown.raw_markdown)
                
                # 3. Lưu file PDF (.pdf)
                # PDF trả về dạng bytes nên dùng mode 'wb' (write binary)
                if result.pdf:
                    with open(f"{base_name}.pdf", "wb") as f:
                        f.write(result.pdf)
                
                # 4. Lưu Screenshot (.png)
                # Screenshot trả về dạng chuỗi Base64, cần giải mã trước khi lưu
                if result.screenshot:
                    img_data = base64.b64decode(result.screenshot)
                    with open(f"{base_name}.png", "wb") as f:
                        f.write(img_data)
                
                print(f"✅ Đã lưu đầy đủ (MD, PDF, PNG) cho: {result.url}")
            else:
                print(f"❌ Lỗi tại {result.url}: {result.error_message}")

if __name__ == "__main__":
    asyncio.run(main())