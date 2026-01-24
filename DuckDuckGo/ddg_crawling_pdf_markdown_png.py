import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import asyncio
import re
import base64
import os
from ddgs import DDGS
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode


# ================== HÀM TẠO TÊN FILE AN TOÀN ==================
def clean_filename(url):
    name = re.sub(r'[\\/*?:"<>|]', "", url.split("//")[-1])
    return name[:50]


# ================== TẠO 3 FOLDER CỐ ĐỊNH ==================
MD_DIR = "output_md"
PDF_DIR = "output_pdf"
IMG_DIR = "output_img"

os.makedirs(MD_DIR, exist_ok=True)
os.makedirs(PDF_DIR, exist_ok=True)
os.makedirs(IMG_DIR, exist_ok=True)


# ================== PHẦN SEARCH DUCKDUCKGO ==================
def get_links(choice, query, max_results):
    links = []

    with DDGS() as ddgs:

        # ================= TEXT =================
        if choice == "1":
            results = list(ddgs.text(query, max_results=max_results))

            print("\n===== KẾT QUẢ TEXT =====")
            for i, r in enumerate(results, 1):
                print(f"\n--- Kết quả {i} ---")
                print("Tiêu đề:", r.get("title"))
                print("Link:", r.get("href"))
                print("Mô tả:", r.get("body"))

                if r.get("href"):
                    links.append(r["href"])


        # ================= NEWS =================
        elif choice == "2":
            results = list(ddgs.news(query, max_results=max_results))

            print("\n===== KẾT QUẢ NEWS =====")
            for i, r in enumerate(results, 1):
                print(f"\n--- Tin {i} ---")
                print("Ngày:", r.get("date"))
                print("Tiêu đề:", r.get("title"))
                print("Nguồn:", r.get("source"))
                print("Link:", r.get("url"))
                print("Tóm tắt:", r.get("body"))

                if r.get("url"):
                    links.append(r["url"])


        # ================= BOOKS =================
        elif choice == "3":
            results = list(ddgs.books(query, max_results=max_results))

            print("\n===== KẾT QUẢ BOOKS =====")
            for i, r in enumerate(results, 1):
                print(f"\n--- Sách {i} ---")
                print("Tên:", r.get("title"))
                print("Tác giả:", r.get("author"))
                print("NXB:", r.get("publisher"))
                print("Link:", r.get("url"))

                if r.get("url"):
                    links.append(r["url"])

    return links



# ================== PHẦN CRAWL BẰNG crawl4ai ==================
async def crawl_links(urls):
    if not urls:
        print("❌ Không có link nào để crawl.")
        return

    run_cfg = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        stream=True,
        pdf=True,
        screenshot=True
    )

    async with AsyncWebCrawler() as crawler:
        async for result in await crawler.arun_many(urls, config=run_cfg):
            if result.success:
                base_name = clean_filename(result.url)
                print(f"💾 Đang xử lý: {base_name}...")

                # Lưu Markdown
                md_path = os.path.join(MD_DIR, f"{base_name}.md")
                with open(md_path, "w", encoding="utf-8") as f:
                    f.write(f"# URL: {result.url}\n\n")
                    f.write(result.markdown.raw_markdown)

                # Lưu PDF
                if result.pdf:
                    pdf_path = os.path.join(PDF_DIR, f"{base_name}.pdf")    
                    with open(pdf_path, "wb") as f:
                        f.write(result.pdf)

                # Lưu Screenshot (PNG)
                if result.screenshot:
                    img_path = os.path.join(IMG_DIR, f"{base_name}.png")
                    img_data = base64.b64decode(result.screenshot)
                    with open(img_path, "wb") as f:
                        f.write(img_data)

                print(f"✅ Đã lưu xong cho: {result.url}")

            else:
                print(f"❌ Lỗi tại {result.url}: {result.error_message}")


# ================== MAIN ==================
def main():
    print("=== SEARCH + CRAWL DUCKDUCKGO + CRAWL4AI ===")
    print("Chọn loại tìm kiếm:")
    print("1 - Text (Web)")
    print("2 - News (Tin tức)")
    print("3 - Books (Sách)")

    choice = input("Nhập lựa chọn (1-3): ").strip()
    query = input("Nhập nội dung cần tìm: ").strip()

    try:
        max_results = int(input("Số kết quả muốn lấy (mặc định 5): ") or 5)
    except ValueError:
        max_results = 5

    print("\n🔎 Đang tìm kiếm trên DuckDuckGo...")
    links = get_links(choice, query, max_results)

    if not links:
        print("❌ Không lấy được link nào từ DuckDuckGo.")
        return

    print("\n📌 Danh sách link sẽ crawl:")
    for i, link in enumerate(links, 1):
        print(f"{i}. {link}")

    print("\n🕷️ Bắt đầu crawl bằng crawl4ai...\n")
    asyncio.run(crawl_links(links))


if __name__ == "__main__":
    main()
