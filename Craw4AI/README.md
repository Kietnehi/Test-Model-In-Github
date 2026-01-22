#  🚀🤖 Crawl4AI: Open-source LLM Friendly Web Crawler & Scrapper
<div align="center">

<a href="https://trendshift.io/repositories/11716" target="_blank"><img src="https://trendshift.io/api/badge/repositories/11716" alt="unclecode%2Fcrawl4ai | Trendshift" style="width: 250px; height: 55px;" width="250" height="55"/></a>

[![GitHub Stars](https://img.shields.io/github/stars/unclecode/crawl4ai?style=social)](https://github.com/unclecode/crawl4ai/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/unclecode/crawl4ai?style=social)](https://github.com/unclecode/crawl4ai/network/members)

[![PyPI version](https://badge.fury.io/py/crawl4ai.svg)](https://badge.fury.io/py/crawl4ai)
[![Python Version](https://img.shields.io/pypi/pyversions/crawl4ai)](https://pypi.org/project/crawl4ai/)
[![Downloads](https://static.pepy.tech/badge/crawl4ai/month)](https://pepy.tech/project/crawl4ai)

[![License](https://img.shields.io/github/license/unclecode/crawl4ai)](https://github.com/unclecode/crawl4ai/blob/main/LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)

</div>

Crawl4AI đơn giản hóa việc thu thập dữ liệu và trích xuất dữ liệu web bất đồng bộ, giúp cho các mô hình ngôn ngữ lớn (LLM) và các ứng dụng trí tuệ nhân tạo (AI) dễ dàng tiếp cận hơn. 🆓🌐

### **Crawl4AI là gì?**

Crawl4AI là một thư viện Python mã nguồn mở, miễn phí, được thiết kế chuyên biệt để thu thập dữ liệu (crawling/scraping) từ các trang web và biến đổi chúng thành định dạng sạch, có cấu trúc (như Markdown hoặc JSON) để phục vụ cho các mô hình ngôn ngữ lớn (LLMs) và các ứng dụng AI.

Khác với các công cụ truyền thống (như BeautifulSoup chỉ lấy HTML thô), Crawl4AI tập trung vào việc tạo ra dữ liệu mà AI có thể hiểu ngay lập tức.

---

### **Các tính năng chính**

Thư viện này giải quyết những vấn đề khó khăn nhất khi làm việc với dữ liệu web hiện đại:

1. **Tối ưu hóa cho LLM (LLM-Friendly):**
* Tự động chuyển đổi nội dung web lộn xộn (HTML) thành **Markdown** sạch sẽ, loại bỏ các phần tử thừa (quảng cáo, thanh điều hướng, footer) để giảm lượng token khi đưa vào AI.
* Hỗ trợ trích xuất dữ liệu có cấu trúc (JSON) dựa trên schema hoặc hướng dẫn từ LLM.


2. **Xử lý nội dung động (Dynamic Content):**
* Sử dụng **Playwright** ở bên dưới để render JavaScript. Điều này cho phép Crawl4AI lấy được dữ liệu từ các trang Single Page Applications (SPA) hoặc các trang web tải nội dung dần dần (lazy loading) mà các thư viện request thông thường không làm được.


3. **Hiệu suất cao & Bất đồng bộ (Asynchronous):**
* Hỗ trợ crawl nhiều URL cùng lúc (multi-URL crawling) với tốc độ cao.
* Cơ chế caching thông minh để tránh tải lại các trang đã xử lý.


4. **Trích xuất thông minh (Extraction Strategies):**
* **Cosine Clustering:** Phân cụm nội dung dựa trên ý nghĩa.
* **CSS/XPath:** Trích xuất chính xác phần tử mong muốn.
* **LLM Extraction:** Dùng chính AI để trích xuất thông tin theo yêu cầu cụ thể từ trang web.


5. **Miễn phí & Chạy cục bộ:**
* Hoàn toàn mã nguồn mở (Open Source), không cần API key trả phí như Firecrawl hay ScrapingBee. Bạn có thể chạy nó trên máy cá nhân hoặc server riêng.



---

### **So sánh nhanh: Crawl4AI vs. Công cụ khác**

| Đặc điểm | BeautifulSoup | Crawl4AI | Firecrawl |
| --- | --- | --- | --- |
| **Loại dữ liệu** | HTML thô (cần tự xử lý) | Markdown sạch / JSON (Sẵn sàng cho AI) | Markdown / JSON |
| **Xử lý JS** | Không (cần thêm Selenium/Playwright) | Có (Tích hợp sẵn Playwright) | Có |
| **Chi phí** | Miễn phí | **Miễn phí (Open Source)** | Trả phí (SaaS API) |
| **Mục đích** | Scraping cơ bản | Xây dựng RAG, AI Agent | Xây dựng RAG (nhanh, không cần setup) |

---

### **Ví dụ sử dụng (Code)**

Dưới đây là một đoạn code Python đơn giản để bạn hình dung cách nó hoạt động:

```python
import asyncio
from crawl4ai import AsyncWebCrawler

async def main():
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url="https://example.com",
        )
        # Kết quả trả về là Markdown sạch, sẵn sàng đưa vào ChatGPT/Claude
        print(result.markdown)

if __name__ == "__main__":
    asyncio.run(main())

```

### **Khi nào bạn nên dùng Crawl4AI?**

* Bạn đang xây dựng ứng dụng RAG (Retrieval-Augmented Generation) và cần dữ liệu sạch từ web.
* Bạn cần crawl các trang web phức tạp có nhiều JavaScript mà không muốn tốn tiền cho các dịch vụ API đắt đỏ.
* Bạn muốn tự chủ về hạ tầng và không muốn phụ thuộc vào bên thứ ba.

Bạn có muốn tôi hướng dẫn cách cài đặt thư viện này hoặc viết một đoạn code mẫu để lấy dữ liệu từ một trang web cụ thể không?