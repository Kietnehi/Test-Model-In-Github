Dưới đây là phiên bản **README.md ngắn gọn, súc tích**, chỉ tập trung đúng mục đích và link model:

---


# 🧠 Open-Source Reasoning LLM Testing

This folder is used to **test and benchmark open-source reasoning LLMs** on limited GPU resources.

## 🎯 Purpose

- Test reasoning / chain-of-thought models  
- Compare quality, speed, and VRAM usage  
- Run on **Google Colab – Tesla T4 (16GB)**  

## 🤖 Tested Models

Links to tested models on Hugging Face:

- [DavidAU/Llama3.3-8B-Instruct-Thinking-Claude-4.5-Opus-High-Reasoning](https://huggingface.co/DavidAU/Llama3.3-8B-Instruct-Thinking-Claude-4.5-Opus-High-Reasoning)

- [deepseek-ai/DeepSeek-R1-Distill-Qwen-7B](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-7B)


## 🖥️ Environment

- Platform: Google Colab  
- GPU: NVIDIA Tesla T4 (16GB)  
- Frameworks: `torch`, `transformers`, `accelerate`, `bitsandbytes`  

## ▶️ Run

```bash
pip install -U transformers accelerate torch bitsandbytes
````

Open the notebook and run on Colab with GPU enabled.

## 📊 Notes

* Some models require 8-bit / 4-bit loading
* Performance depends on prompt and context length


