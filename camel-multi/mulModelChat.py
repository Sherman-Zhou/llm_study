from camel.agents import ChatAgent
from camel.models import ModelFactory
from camel.types import ModelPlatformType
from camel.messages import BaseMessage

from io import BytesIO
import requests
from PIL import Image
import dotenv
import os
dotenv.load_dotenv()
key_prefix= "DASHSCOPE"
api_key = os.getenv(f"{key_prefix}_API_KEY")
base_url = os.getenv(f"{key_prefix}_BASE_URL")
module = os.getenv(f"{key_prefix}_MULTI_MODEL")
model = ModelFactory.create(
    model_platform=ModelPlatformType.OPENAI_COMPATIBLE_MODEL,
    model_type =module,
    url = base_url,
    api_key=api_key
)

agent = ChatAgent(
    model=model,
    output_language='中文'
)

# 图片URL
url = "https://img0.baidu.com/it/u=2205376118,3235587920&fm=253&fmt=auto&app=120&f=JPEG?w=846&h=800"
response = requests.get(url)
img = Image.open(BytesIO(response.content))

user_msg = BaseMessage.make_user_message(
    role_name="User",
    content="请描述这张图片的内容",
    image_list=[img]  # 将图片放入列表中
)
# user_msg.to_dict()

response = agent.step(user_msg)
print(response.msgs[0].content)