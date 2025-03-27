import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv();
# key_prefix= os.getenv('KEY_PREFIX')
key_prefix ='DASHSCOPE'
client = OpenAI(
        # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
        api_key=os.getenv(f"{key_prefix}_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
messages = [
      {
        "role": "user",
        "content": "第二个SELECT语句返回一个数字，表示在没有LIMIT子句的情况下，第一个SELECT语句返回了多少行。"
      }
    ]
translation_options = {
      "source_lang": "Chinese",
      "target_lang": "English",
      "domains": "The sentence is from Ali Cloud IT domain. It mainly involves computer-related software development and usage methods, including many terms related to computer software and hardware. Pay attention to professional troubleshooting terminologies and sentence patterns when translating. Translate into this IT domain style."
    }
    
completion = client.chat.completions.create(
    model="qwen-mt-turbo",
    messages=messages,
    extra_body={
        "translation_options": translation_options
    }
)
print(completion.choices[0].message.content)