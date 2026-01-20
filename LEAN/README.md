

### 🚀 LEANN là gì?

LEANN là một **cơ sở dữ liệu vector (vector database) sáng tạo và siêu nhẹ**, được thiết kế để "dân chủ hóa" AI cá nhân. Mục tiêu chính của nó là biến chiếc laptop bình thường của bạn thành một hệ thống RAG (Retrieval-Augmented Generation) mạnh mẽ, có khả năng tìm kiếm ngữ nghĩa (semantic search) trên hàng triệu tài liệu mà không tốn nhiều tài nguyên.

### ✨ Điểm nổi bật chính

* **Tiết kiệm lưu trữ khổng lồ (97%):**
* LEANN sử dụng dung lượng lưu trữ ít hơn **97%** so với các cơ sở dữ liệu vector truyền thống (như FAISS) mà **không làm giảm độ chính xác**.
* *Ví dụ thực tế:* Để lập chỉ mục (index) cho 60 triệu đoạn văn bản, LEANN chỉ cần **6GB**, trong khi các giải pháp khác cần tới **201GB**.


* **Cơ chế hoạt động độc đáo:**
* Thay vì lưu trữ tất cả các vector embeddings (vốn rất nặng), LEANN sử dụng kỹ thuật **"tính toán lại có chọn lọc dựa trên đồ thị"** (graph-based selective recomputation).
* Nó cắt tỉa đồ thị thông minh và chỉ tính toán embeddings *theo yêu cầu* (on-demand) trong quá trình tìm kiếm, giúp giảm tải bộ nhớ và ổ cứng tối đa.


* **Quyền riêng tư tuyệt đối (Privacy-First):**
* Toàn bộ dữ liệu được xử lý và lưu trữ **cục bộ (local)** trên laptop của bạn.
* Không gửi dữ liệu lên đám mây, không phụ thuộc vào bên thứ ba.



### 🔍 Khả năng ứng dụng ("RAG Everything")

LEANN cho phép bạn tìm kiếm thông minh trên hầu hết mọi dữ liệu cá nhân:

1. **Tài liệu:** PDF, TXT, Markdown, DOCX.
2. **Lịch sử Chat:** WeChat, iMessage, ChatGPT, Claude, Slack.
3. **Hoạt động Web:** Lịch sử duyệt web (Chrome history), Email (Apple Mail), Twitter Bookmarks.
4. **Lập trình:** Tìm kiếm trong Codebase (Tương thích hoàn toàn với Claude Code và hỗ trợ chunking thông minh dựa trên AST).

### 🛠️ Tích hợp & Công nghệ

* **Hỗ trợ đa dạng LLM:** Hoạt động với OpenAI, Ollama (để chạy offline hoàn toàn), HuggingFace, Anthropic.
* **MCP (Model Context Protocol):** Hỗ trợ kết nối với dữ liệu trực tiếp (live data) từ các nền tảng bên ngoài như Slack hay Twitter thông qua giao thức MCP.
* **Cài đặt dễ dàng:** Viết bằng Python, hỗ trợ cài đặt qua `uv` hoặc `pip` trên macOS, Linux và WSL.

---

### Hướng dẫn chạy LEANN trên windows bằng wsl .
Tuyệt vời! Nếu bạn đã có WSL, chúng ta sẽ chuyển từ môi trường Windows sang môi trường Linux ngay trên cửa sổ CMD của bạn.

Hãy làm theo đúng 4 bước sau ngay tại cửa sổ CMD bạn đang mở:

### Bước 1: Vào môi trường WSL và về thư mục gốc

Gõ lệnh này vào CMD để chuyển sang Linux:

```cmd
wsl

```

*(Dấu nhắc lệnh sẽ đổi từ `C:\Users...` sang tên user của Linux, ví dụ `username@PCname:~$`)*.

Sau đó gõ lệnh này để về thư mục gốc của Linux (giúp chạy nhanh hơn và tránh lỗi quyền hạn):

```bash
cd ~

```

### Bước 2: Cài đặt các thư viện hệ thống cần thiết (Bắt buộc)

LEANN cần một số thư viện C++ để chạy trên Linux. Bạn copy nguyên đoạn này và paste vào (có thể nó sẽ hỏi mật khẩu Linux của bạn):

```bash
sudo apt-get update && sudo apt-get install -y libomp-dev libboost-all-dev protobuf-compiler libzmq3-dev pkg-config libabsl-dev libaio-dev libprotobuf-dev libmkl-full-dev git curl

```

### Bước 3: Cài đặt `uv` cho Linux

(Lưu ý: `uv` bạn cài lúc nãy là cho Windows, giờ phải cài lại cho Linux).

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh

```

Sau khi chạy xong, gõ lệnh sau để cập nhật đường dẫn:

```bash
source $HOME/.local/bin/env

```

### Bước 4: Tải và cài đặt LEANN

Giờ bạn làm lại thao tác cài đặt, nhưng lần này sẽ thành công vì đang ở Linux:

1. **Tải code:**
```bash
git clone https://github.com/yichuan-w/LEANN.git leann
cd leann

```


2. **Tạo môi trường và cài đặt:**
```bash
uv venv
source .venv/bin/activate
uv pip install leann

```


*(Lúc này bạn sẽ thấy nó tải các file `manylinux` và cài đặt thành công, không còn lỗi màu đỏ nữa).*

### Bước 5: Chạy thử

Sau khi cài xong, bạn chạy thử lệnh này để kiểm tra:

```bash
python -m apps.document_rag --help

```

Nếu nó hiện ra hướng dẫn sử dụng, chúc mừng bạn đã cài đặt thành công! Bạn có thể bắt đầu dùng LEANN ngay trên cửa sổ này.
