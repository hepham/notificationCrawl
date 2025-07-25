import os
from google import genai
from google.genai import types

# Đặt API key của bạn ở đây
API_KEY = "AIzaSyAJFlgYtlqhjlkfh3mHFRzzE7C2Bgodr18"  # <-- Thay bằng API key thật

def generate_email(prompt_line, temperature=0.8):
    client = genai.Client(api_key=API_KEY)
    model = "gemini-2.5-flash"
    prompt = f"""Hãy viết một email xác nhận dựa trên yêu cầu sau, đảm bảo:
- Nội dung xác nhận, lịch sự, tự nhiên, đúng ngữ cảnh Việt Nam
- Có tên người, địa chỉ, ngày giờ, lịch trình cụ thể nếu có thể
- Email trình bày nhiều dòng, không trùng lặp với các mẫu xác nhận thông thường
- Sáng tạo, đa dạng, tránh lặp lại cấu trúc hoặc ý tưởng với các email khác
- Viết bằng tiếng Việt
Yêu cầu: {prompt_line}
Chỉ trả về nội dung email, không thêm giải thích."""

    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=prompt)],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_budget=-1),
        temperature=temperature,
    )

    result = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        result += chunk.text
    return result.strip()

# Đọc từng dòng từ prompt.txt, bỏ qua dòng trống
with open('prompt.txt', encoding='utf-8') as f:
    lines = [line.strip() for line in f if line.strip()]

os.makedirs('emails', exist_ok=True)

for idx, line in enumerate(lines, 1):
    filename = f"emails/email_{idx:03d}.txt"
    if os.path.exists(filename):
        print(f"Đã có {filename}, bỏ qua.")
        continue
    print(f"Đang sinh email cho dòng {idx}: {line[:60]}...")
    try:
        email_content = generate_email(line)
        with open(filename, 'w', encoding='utf-8') as out:
            out.write(email_content)
        print(f"Đã lưu {filename}")
    except Exception as e:
        print(f"Lỗi dòng {idx}: {e}")

print("Hoàn tất!") 