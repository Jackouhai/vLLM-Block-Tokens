# from openai import OpenAI

# client = OpenAI(
#     base_url="http://localhost:8000/v1",
#     api_key="EMPTY"
# )

# # Sử dụng cho completions
# completion_response = client.chat.completions.create(
#     model="qwen2.5",  # tên đã dùng ở --served-model-name
#     messages=[
#         {"role": "system", "content": "你是一位得力助手"}, # You are a help full assistant
#         {"role": "user", "content": "介绍越南这个国家。"} # Introduce Vietnam country. You must be answer in Chinese
#     ]

# )
# print(completion_response.choices[0].message.content)


import re
from openai import OpenAI

def filter_chinese_characters(text):
    """
    Lọc bỏ tất cả các ký tự tiếng Trung khỏi text.
    
    Args:
        text (str): Văn bản cần lọc
        
    Returns:
        str: Văn bản đã loại bỏ các ký tự tiếng Trung
    """
    # Unicode ranges cho tiếng Trung:
    # \u4e00-\u9fff: CJK Unified Ideographs (chữ Hán phổ biến)
    # \u3400-\u4dbf: CJK Unified Ideographs Extension A
    # \u20000-\u2a6df: CJK Unified Ideographs Extension B
    # \uf900-\ufaff: CJK Compatibility Ideographs
    # \u3000-\u303f: CJK Symbols and Punctuation
    
    # Pattern để match các ký tự tiếng Trung
    chinese_pattern = re.compile(
        r'[\u4e00-\u9fff\u3400-\u4dbf\u20000-\u2a6df\uf900-\ufaff\u3000-\u303f]+'
    )
    
    # Loại bỏ các ký tự tiếng Trung
    filtered_text = chinese_pattern.sub('', text)
    
    # Loại bỏ khoảng trắng thừa
    filtered_text = re.sub(r'\s+', ' ', filtered_text).strip()
    
    return filtered_text

def contains_chinese(text):
    """
    Kiểm tra xem text có chứa ký tự tiếng Trung hay không.
    
    Args:
        text (str): Văn bản cần kiểm tra
        
    Returns:
        bool: True nếu có ký tự tiếng Trung, False nếu không
    """
    chinese_pattern = re.compile(
        r'[\u4e00-\u9fff\u3400-\u4dbf\u20000-\u2a6df\uf900-\ufaff\u3000-\u303f]'
    )
    return bool(chinese_pattern.search(text))

# Modify OpenAI's API key and API base to use vLLM's API server.
openai_api_key = "EMPTY"
openai_api_base = "http://localhost:8000/v1"

client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=openai_api_key,
    base_url=openai_api_base,
)

def get_safe_response(completion):
    raw_content = completion.choices[0].message.content
    
    if contains_chinese(raw_content):
        return "Xin lỗi tôi không thể trả lời câu hỏi này"
    else:
        return raw_content


model = "qwen2.5"

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "bạn là trợ lý ảo tiếng Trung."
        }, 
        {
            "role": "user",
            "content": "hãy viết cho tôi 1 câu xin chào tiếng trung"
        }
    ],

    model=model,
)

# Can thiệp NGAY LÚC lấy response
original_response = get_safe_response(chat_completion)

print(original_response)

