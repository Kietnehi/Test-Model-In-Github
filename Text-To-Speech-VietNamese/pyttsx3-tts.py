import pyttsx3

engine = pyttsx3.init()
engine.setProperty('voice', 'vi') # Phải đảm bảo máy bạn đã cài gói tiếng Việt
engine.say("Chào bạn, tôi đang nói offline.")
engine.runAndWait()