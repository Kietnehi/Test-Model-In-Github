# 📢 Hướng dẫn Cài đặt Text-To-Speech Vietnamese

## 1. Cài đặt cho `vieneu-tts.py`

Sử dụng mô-đun `vieneu` để chuyển văn bản thành giọng nói tiếng Việt.

```bash
!apt update
!apt install -y espeak-ng
!pip install vieneu
```

> **Lưu ý:**
> - `espeak-ng` là thư viện TTS cần thiết cho `vieneu`.
> - Các lệnh trên dùng cho Jupyter/Colab. Nếu chạy local, hãy dùng terminal/cmd tương ứng.

---

## 2. Cài đặt cho `edge-tts.py`

Sử dụng mô-đun `edge-tts` để chuyển văn bản thành giọng nói bằng dịch vụ Microsoft Edge TTS.

```bash
!pip install edge-tts
```

> **Lưu ý:**
> - Chỉ cần cài gói Python `edge-tts`.
> - Cần Internet để sử dụng.

---

## 3. Cài đặt cho `gTts.py`

Sử dụng mô-đun `gtts` để chuyển văn bản thành giọng nói tiếng Việt qua Google Translate.

```bash
!pip install gtts
```

> **Lưu ý:**
> - Cần Internet để sử dụng `gTTS`.
> - Lệnh trên dùng cho Jupyter/Colab, nếu dùng local thì chạy trong terminal/cmd.

---

## 4. Cài đặt cho `pyttsx3-tts.py`

Sử dụng mô-đun `pyttsx3` để chuyển văn bản thành giọng nói **offline** (không cần Internet).

```bash
!pip install pyttsx3
```

### Yêu cầu theo hệ điều hành

- **Windows**
  - Không cần cài thêm gì (dùng SAPI5 có sẵn)

- **Linux (Ubuntu/Debian)**
  ```bash
  !apt update
  !apt install -y espeak
  ```

- **macOS**
  - Không cần cài thêm (dùng NSSpeechSynthesizer)

> **Lưu ý:**
> - `pyttsx3` chạy **offline**
> - Giọng tiếng Việt phụ thuộc vào engine hệ điều hành, chất lượng thường thấp hơn `edge-tts`

---

## ▶️ Ví dụ code `pyttsx3-tts.py`

```python
import pyttsx3

engine = pyttsx3.init()

text = "Xin chào, đây là ví dụ chuyển văn bản thành giọng nói bằng pyttsx3"

engine.say(text)
engine.runAndWait()
```
