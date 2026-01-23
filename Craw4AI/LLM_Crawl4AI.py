import os
import json
import asyncio
import sys # 1. Thêm sys để fix lỗi Windows

# --- FIX LỖI CHO WINDOWS (BẮT BUỘC) ---
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
# --------------------------------------

from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, LLMConfig, CacheMode
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load file .env (Giữ nguyên đường dẫn của bạn)
load_dotenv(r"C:\Users\ADMIN\Desktop\Github Fulll Project\Test Model AI in Colab\.env")

api_key = os.environ.get("GEMINI_API_KEY")

class OpenAIModelFee(BaseModel):
    model_name: str = Field(..., description="Name of the OpenAI model.")
    input_fee: str = Field(..., description="Fee for input token for the OpenAI model.")
    output_fee: str = Field(..., description="Fee for output token for the OpenAI model.")

async def extract_structured_data_using_llm(provider: str, api_token: str = None, extra_headers: dict = None):
    print(f"\n--- Extracting Structured Data with {provider} ---")

    # Skip if API token is missing (for providers that require it)
    if api_token is None and provider != "ollama":
        print(f"API token is required for {provider}. Skipping this example.")
        return

    extra_args = {"extra_headers": extra_headers} if extra_headers else {}

    config = CrawlerRunConfig(
        word_count_threshold=1,
        extraction_strategy=LLMExtractionStrategy(
            llm_config = LLMConfig(provider=provider, api_token=api_token),
            schema=OpenAIModelFee.model_json_schema(),
            extraction_type="schema",
            # 2. Sửa lại chuỗi instruction cho đỡ bị lỗi cú pháp
            instruction="Extract all model names along with fees for input and output tokens. Example: {model_name: 'GPT-4', input_fee: 'US$10.00 / 1M tokens', output_fee: 'US$30.00 / 1M tokens'}.",
            # 3. Sửa lỗi logic: Truyền thẳng dict vào tham số extra_args thay vì bung nó ra (**)
            extra_args=extra_args 
        ),
        # 4. Quan trọng: Dùng BYPASS để ép chạy mới, tránh lỗi 404 cũ lưu trong cache
        cache_mode = CacheMode.BYPASS
    )

    async with AsyncWebCrawler(verbose=True) as crawler:
        result = await crawler.arun(
            url="https://openai.com/api/pricing/",
            config=config
        )
        
        if result.success:
            try:
                print(json.loads(result.extracted_content))
            except Exception as e:
                print("Raw content:", result.extracted_content)
        else:
            print(f"Error: {result.error_message}")

# Usage:
# Nếu chạy file .py thông thường (Terminal/CMD):
if __name__ == "__main__":
    # Dùng asyncio.run() để chạy hàm async
    asyncio.run(extract_structured_data_using_llm("openai/gpt-4o-mini", os.getenv("GEMINI_API_KEY")))

# Nếu chạy trên Jupyter Notebook / Colab thì giữ nguyên dòng dưới và bỏ dòng if __name__...:
# await extract_structured_data_using_llm("gemini/gemini-1.5-pro", os.getenv("GEMINI_API_KEY"))