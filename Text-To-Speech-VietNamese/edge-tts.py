import edge_tts
import asyncio
import nest_asyncio
from IPython.display import Audio, display

# Cho phép chạy async trong Colab
nest_asyncio.apply()

async def text_to_speech_cloud(text, voice="vi-VN-HoaiMyNeural"):
    """
    Chuyển đổi text thành voice và hiển thị trình phát nhạc ngay trong ô kết quả.
    """
    output_file = "speech_output.mp3"
    
    # 1. Tạo file âm thanh
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)
    
    # 2. Sử dụng trình phát âm thanh của trình duyệt (IPython)
    # Autoplay=True giúp nó tự động phát sau khi chuyển đổi xong
    display(Audio(output_file, autoplay=True))
    
    print(f"Đã chuyển đổi xong: {text}")

def speak(content):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(text_to_speech_cloud(content))

# --- CHẠY THỬ ---
if __name__ == "__main__":
    noi_dung = "Chào bạn, tôi đã sửa lỗi loa rồi đây. Bây giờ bạn có thể nghe thấy tôi nói trực tiếp trên trình duyệt."
    speak(noi_dung)