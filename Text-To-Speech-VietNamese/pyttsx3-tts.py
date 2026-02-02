import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')

found_vi = False
for voice in voices:
    # Tìm giọng nói có ngôn ngữ Việt Nam
    if "vietnam" in voice.name.lower() or "vi-vn" in voice.id.lower():
        engine.setProperty('voice', voice.id)
        found_vi = True
        break

if not found_vi:
    print("Cảnh báo: Hệ thống chưa cài hoặc chưa tải xong giọng Tiếng Việt!")
else:
    engine.setProperty('rate', 150)
    engine.say("Chào bạn, tôi đã tìm thấy giọng tiếng Việt.")
    engine.runAndWait()