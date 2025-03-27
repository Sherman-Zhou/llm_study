import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
# key_prefix= os.getenv('KEY_PREFIX')
key_prefix ='DASHSCOPE'
client = OpenAI(
    api_key=os.getenv(f"{key_prefix}_API_KEY"), # 如果您没有配置环境变量，请在此处用您的API Key进行替换
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # 填写DashScope服务的base_url
)
completion = client.chat.completions.create(
    model="qwen-plus",
    messages=[{
        "role": "user",
        "content": "请对“春天来了，大地”这句话进行续写，来表达春天的美好和作者的喜悦之情"
    },
    {
        "role": "assistant",
        "content": "春天来了，大地",
        "partial": True
    }]
    )
print(completion.choices[0].message.content)