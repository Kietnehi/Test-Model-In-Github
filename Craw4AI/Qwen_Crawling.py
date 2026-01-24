import asyncio
import json
import torch
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
from transformers import AutoModelForCausalLM, AutoTokenizer
from pydantic import BaseModel, Field
import asyncio
import nest_asyncio
nest_asyncio.apply()
# --- Cấu hình Model Local (Qwen 2.5) ---
# Chọn model phù hợp với VRAM của bạn. 
# Qwen/Qwen2.5-3B-Instruct là lựa chọn tốt thay thế cho "2.5B" (vì dòng 2.5 có các size 0.5, 1.5, 3, 7...)
MODEL_ID = "Qwen/Qwen2.5-3B-Instruct" 

print(f"Loading model {MODEL_ID}...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    torch_dtype=torch.bfloat16, # Dùng bfloat16 để nhẹ và nhanh hơn trên GPU đời mới
    device_map="auto",          # Tự động chia layer vào GPU/CPU
    trust_remote_code=True
)

# --- Định nghĩa Schema (Dùng để tạo Prompt) ---
class OpenAIModelFee(BaseModel):
    model_name: str = Field(..., description="Name of the OpenAI model.")
    input_fee: str = Field(..., description="Fee for input token for the OpenAI model.")
    output_fee: str = Field(..., description="Fee for output token for the OpenAI model.")

schema_json = OpenAIModelFee.model_json_schema()

# --- Hàm trích xuất dữ liệu bằng Transformers ---
def extract_with_local_qwen(content: str):
    # Tạo prompt hướng dẫn model trả về JSON
    prompt = f"""
    You are a helpful data extraction assistant. 
    Analyze the following text and extract all OpenAI model names and their fees (input and output).
    
    Return the result strictly as a JSON array matching this schema:
    {json.dumps(schema_json, indent=2)}

    Text to analyze:
    {content[:8000]} # Cắt bớt nếu text quá dài để tránh tràn context window
    
    Answer (JSON only):
    """

    messages = [
        {"role": "system", "content": "You are a helpful assistant that extracts structured data in JSON format."},
        {"role": "user", "content": prompt}
    ]
    
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

    generated_ids = model.generate(
        **model_inputs,
        max_new_tokens=1024,
        temperature=0.1, # Giảm nhiệt độ để kết quả chính xác hơn
        do_sample=False  # Greedy decoding cho tác vụ trích xuất
    )
    
    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]

    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    
    # Xử lý chuỗi JSON trả về (phòng trường hợp model chèn thêm text)
    try:
        # Tìm đoạn bắt đầu bằng [ và kết thúc bằng ]
        start_idx = response.find('[')
        end_idx = response.rfind(']') + 1
        if start_idx != -1 and end_idx != -1:
            json_str = response[start_idx:end_idx]
            return json.loads(json_str)
        else:
            print("Không tìm thấy JSON hợp lệ trong phản hồi.")
            print("Raw response:", response)
            return []
    except Exception as e:
        print(f"Lỗi parse JSON: {e}")
        return []

# --- Hàm Crawl và Chạy ---
async def main():
    print("\n--- Crawling Data from OpenAI Pricing ---")
    
    # Cấu hình crawler cơ bản (không dùng LLMExtractionStrategy ở đây)
    config = CrawlerRunConfig(
        word_count_threshold=1,
        cache_mode=CacheMode.ENABLED
    )

    async with AsyncWebCrawler(verbose=True) as crawler:
        result = await crawler.arun(
            url="https://openai.com/api/pricing/",
            config=config
        )
        
        if result.success:
            print("Crawl thành công! Đang trích xuất dữ liệu bằng Qwen...")
            # Lấy nội dung markdown sạch
            markdown_content = result.markdown 
            
            # Gọi hàm xử lý local
            extracted_data = extract_with_local_qwen(markdown_content)
            
            print("\n--- KẾT QUẢ TRÍCH XUẤT ---")
            print(json.dumps(extracted_data, indent=2, ensure_ascii=False))
        else:
            print("Crawl thất bại:", result.error_message)

if __name__ == "__main__":
    asyncio.run(main())