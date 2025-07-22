from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="EMPTY"
)

# Sử dụng cho completions
completion_response = client.chat.completions.create(
    model="qwen2.5",  # tên đã dùng ở --served-model-name
    messages=[
        {"role": "system", "content": "你是一位得力助手"}, # You are a help full assistant
        {"role": "user", "content": "介绍越南这个国家。必须用中文回答"} # Introduce Vietnam country. You must be answer in Chinese
    ],
    extra_body={
        "logits_processors": [
            "llm_block_chinese.logits_processor.filter_chinese"
        ]
    }
)

print(completion_response.choices[0].message.content)
