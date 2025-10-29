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

# Compile pattern một lần duy nhất khi load module (tối ưu hiệu năng)
CHINESE_CHAR_PATTERN = re.compile(
    r'[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff\u3000-\u303f]'
)

def filter_chinese_characters(text):
    """
    Lọc bỏ các ký tự tiếng Trung khỏi text, giữ lại tất cả ký tự khác.
    Sử dụng regex pre-compiled để tối ưu hiệu năng.
    
    Args:
        text (str): Văn bản cần lọc
        
    Returns:
        str: Văn bản đã loại bỏ các ký tự tiếng Trung
    """
    # Xóa các ký tự chữ Hán (CHỈ xóa các ký tự trong các range tiếng Trung)
    filtered_text = CHINESE_CHAR_PATTERN.sub('', text)
    
    # Xóa các dấu câu tiếng Trung (full-width)
    chinese_punctuation = '。""''「」『』【】《》〈〉、…—～·'
    for punct in chinese_punctuation:
        filtered_text = filtered_text.replace(punct, '')
    
    # Chuẩn hóa: xóa khoảng trắng thừa
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
    """
    Can thiệp ngay lúc lấy response từ vLLM.
    Loại bỏ tất cả các ký tự tiếng Trung khỏi response.
    """
    raw_content = completion.choices[0].message.content + ",xin chào tôi tên là A hiện tại tôi đang là sinh viên"
    print("Response gốc:", raw_content )
    print("=" * 50)
    
    # Loại bỏ ký tự tiếng Trung
    filtered = filter_chinese_characters(raw_content)
    return filtered


model = "qwen2.5"

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "你是一位得力助手"
        }, 
        {
            "role": "user",
            "content": "介绍越南这个国家"
        }
    ],

    model=model,
)

# Can thiệp NGAY LÚC lấy response - loại bỏ ký tự tiếng Trung
original_response = get_safe_response(chat_completion)

print("\nResponse đã lọc (không có tiếng Trung):")
print(original_response)

