Dưới đây là bản **tóm tắt ngắn gọn các ý chính và phần cần thiết** của LangExtract để bạn có thể đưa trực tiếp vào README.

---

## LangExtract – Tóm tắt nhanh cho README

### Giới thiệu

**LangExtract** là thư viện Python dùng LLM để trích xuất dữ liệu có cấu trúc từ văn bản không cấu trúc (clinical notes, báo cáo, tài liệu dài…) dựa trên prompt và ví dụ người dùng cung cấp.

---

### Tính năng chính

* 🎯 **Grounding chính xác**: Mỗi extraction được gắn đúng vị trí trong văn bản gốc.
* 📦 **Output có cấu trúc ổn định**: Tuân theo schema và ví dụ few-shot.
* 📚 **Xử lý tài liệu dài**: Chia nhỏ, chạy song song, nhiều lượt để tăng recall.
* 🖥️ **Visual hóa kết quả**: Sinh file HTML tương tác để kiểm tra entity trong ngữ cảnh.
* 🔌 **Hỗ trợ nhiều model**:

  * Google Gemini (cloud)
  * OpenAI
  * Local LLM qua Ollama
* 🧩 **Dễ mở rộng**: Thêm custom model provider qua plugin.

---

### Cài đặt

```bash
pip install langextract
```

---

### Thiết lập API key (cloud models)

Cách khuyến nghị:

```bash
export LANGEXTRACT_API_KEY="your-api-key"
```

Hoặc dùng file `.env`.

Hỗ trợ key từ:

* Google AI Studio / Vertex AI (Gemini)
* OpenAI Platform

---

### Quick Start (ví dụ ngắn)

```python
import langextract as lx

prompt = "Extract characters and emotions."
examples = [...]  # few-shot examples

result = lx.extract(
    text_or_documents="Lady Juliet gazed longingly at the stars...",
    prompt_description=prompt,
    examples=examples,
    model_id="gemini-2.5-flash",
)
```

---

### Lưu & Visualize kết quả

```python
lx.io.save_annotated_documents([result], "results.jsonl", ".")
html = lx.visualize("results.jsonl")

with open("visualization.html", "w") as f:
    f.write(html.data if hasattr(html, "data") else html)
```

---

### Xử lý tài liệu dài

* Hỗ trợ URL trực tiếp (VD: Project Gutenberg)
* Chạy song song + nhiều passes:

```python
result = lx.extract(
    text_or_documents=url,
    extraction_passes=3,
    max_workers=20,
    max_char_buffer=1000
)
```

---

### Dùng OpenAI

```python
pip install langextract[openai]
```

```python
result = lx.extract(
    model_id="gpt-4o",
    fence_output=True,
    use_schema_constraints=False
)
```

---

### Dùng Local LLM với Ollama

```python
result = lx.extract(
    model_id="gemma2:2b",
    model_url="http://localhost:11434",
    fence_output=False,
    use_schema_constraints=False
)
```

---

### Mở rộng Provider

* Hỗ trợ plugin system
* Đăng ký provider bằng `@registry.register(...)`
* Phân phối như package riêng

---

### Testing & Dev

```bash
pytest tests
tox
```

---

### Ghi chú

* Không phải sản phẩm chính thức của Google.
* Dùng cho y tế chỉ mang tính minh họa, không thay thế tư vấn chuyên môn.
* License: Apache 2.0

---

Nếu bạn muốn, mình có thể:

* Viết lại bản này **bằng tiếng Anh chuẩn README**
* Hoặc rút gọn hơn nữa thành **1 trang “Minimal README”**
* Hoặc chỉnh theo style project hiện tại của bạn (bullet, badges, sections).
