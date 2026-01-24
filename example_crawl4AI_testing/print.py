import json

# Giả sử bạn đã có dữ liệu từ file clean_fit_data.json
with open("clean_fit_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Duyệt qua từng trang đã crawl và in ra file .md riêng biệt để kiểm tra
for i, entry in enumerate(data):
    url = entry['url']
    content = entry['content']
    
    # Tạo tên file an toàn từ URL hoặc số thứ tự
    filename = f"page_{i}.md"
    
    with open(filename, "w", encoding="utf-8") as md_file:
        md_file.write(f"Source: {url}\n\n")
        md_file.write(content)
    
    print(f"Đã xuất nội dung trang {url} ra file: {filename}")