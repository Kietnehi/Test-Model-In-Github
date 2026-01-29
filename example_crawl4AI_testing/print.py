import json
import os

os.makedirs("md_output", exist_ok=True)

with open("crawled_data_deep.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for i, item in enumerate(data, 1):
    raw_title = item.get("title") or f"page_{i}"
    title = raw_title.strip()

    # Lọc ký tự an toàn cho Windows/Linux
    safe_title = "".join(c for c in title if c.isalnum() or c in " _-").strip()
    safe_title = safe_title[:60]

    filename = os.path.join("md_output", f"{i:03d}_{safe_title}.md")

    content = item.get("content", "").strip()
    if not content:
        continue

    with open(filename, "w", encoding="utf-8") as out:
        out.write(f"# {title}\n\n")
        out.write(f"- **URL:** {item['url']}\n")
        out.write(f"- **Depth:** {item.get('depth', '')}\n")
        out.write(f"- **Hash:** {item.get('content_hash', '')}\n\n")
        out.write(content)

print("✅ Đã xuất xong các file markdown trong thư mục md_output/")
