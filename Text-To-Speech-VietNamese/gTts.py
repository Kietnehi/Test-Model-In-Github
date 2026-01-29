from gtts import gTTS
from IPython.display import Audio

text = "Chào bạn, đây là giọng đọc từ Google Translate."
tts = gTTS(text, lang='vi')
tts.save("google_voice.mp3")

Audio("google_voice.mp3", autoplay=True)