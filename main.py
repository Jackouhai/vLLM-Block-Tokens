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


from openai import OpenAI

# Modify OpenAI's API key and API base to use vLLM's API server.
openai_api_key = "EMPTY"
openai_api_base = "http://localhost:8000/v1"

client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=openai_api_key,
    base_url=openai_api_base,
)

model = "qwen2.5"

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "你是一位得力助手"
        }, 
        {
            "role": "user",
            "content": "介绍越南这个国家。"
        }
    ],

    model=model,
)

print("Chat completion results:")
print(chat_completion.choices[0].message.content)
