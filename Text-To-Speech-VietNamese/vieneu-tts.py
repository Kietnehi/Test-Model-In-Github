from vieneu import Vieneu
import os

# Initialization
tts = Vieneu()  # Default: 0.3B-Q4 GGUF for CPU
os.makedirs("outputs", exist_ok=True)

# 1. List preset voices
available_voices = tts.list_preset_voices()
for desc, name in available_voices:
    print(f"   - {desc} (ID: {name})")

# 2. Use specific voice (dynamically select second voice)
if available_voices:
    _, my_voice_id = available_voices[1] if len(available_voices) > 1 else available_voices[0]
    voice_data = tts.get_preset_voice(my_voice_id)
    audio_spec = tts.infer(text="Chào bạn, tôi đang nói bằng giọng của bác sĩ Tuyên.", voice=voice_data)
    tts.save(audio_spec, f"outputs/standard_{my_voice_id}.wav")
    print(f"💾 Saved synthesis to: outputs/standard_{my_voice_id}.wav")

# 3. Standard synthesis (uses default voice)
text = "Xin chào, tôi là VieNeu. Tôi có thể giúp bạn đọc sách, làm chatbot thời gian thực, hoặc thậm chí clone giọng nói của bạn."
audio = tts.infer(text=text)
tts.save(audio, "outputs/standard_output.wav")
print("💾 Saved synthesis to: outputs/standard_output.wav")

# 4. Zero-shot voice cloning
if os.path.exists("examples/audio_ref/example_ngoc_huyen.wav"):
    cloned_audio = tts.infer(
        text="Đây là giọng nói đã được clone thành công từ file mẫu.",
        ref_audio="examples/audio_ref/example_ngoc_huyen.wav",
        ref_text="Tác phẩm dự thi bảo đảm tính khoa học, tính đảng, tính chiến đấu, tính định hướng."
    )
    tts.save(cloned_audio, "outputs/standard_cloned_output.wav")
    print("💾 Saved cloned voice to: outputs/standard_cloned_output.wav")

# 5. Cleanup
tts.close()
