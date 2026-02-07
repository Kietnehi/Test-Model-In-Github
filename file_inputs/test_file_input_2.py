from openai import OpenAI
client = OpenAI(api_key="")
# 1️⃣ Upload file local
file = client.files.create(
    file=open(
        r"C:\Users\ADMIN\Desktop\NCKH\PAPER\Yang_2024_Phys._Med._Biol._69_045019.pdf",
        "rb"
    ),
    purpose="assistants"
)

print("Uploaded file_id:", file.id)

# 2️⃣ Gửi request + file_id
response = client.responses.create(
    model="gpt-4.1-mini",
    input=[
        {
            "role": "user",
            "content": [
                {
                    "type": "input_text",
                    "text": "Analyze the paper and summarize the key points."
                },
                {
                    "type": "input_file",
                    "file_id": file.id
                }
            ]
        }
    ]
)

print(response.output_text)