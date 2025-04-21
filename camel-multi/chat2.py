
from camel.agents import ChatAgent
from camel.models import ModelFactory
from camel.types import ModelPlatformType
import dotenv
import os
dotenv.load_dotenv()
key_prefix= os.getenv("KEY_PREFIX")
api_key = os.getenv(f"{key_prefix}_API_KEY")
base_url = os.getenv(f"{key_prefix}_BASE_URL")

module = os.getenv(f"{key_prefix}_MODEL")

model = ModelFactory.create(
    model_platform=ModelPlatformType.OPENAI_COMPATIBLE_MODEL,
    model_type=module,
    url=base_url,
    api_key = api_key
)
# 创建系统消息，告诉ChatAgent自己的角色定位
system_msg = "You are a helpful assistant that responds to user queries."

# 实例化一个ChatAgent
chat_agent = ChatAgent(model=model, system_message=system_msg,output_language='zh')

# 构造用户消息
user_msg = "Hello! Can you tell me something about CAMEL AI?"

# 将用户消息传给ChatAgent，并获取回复
response = chat_agent.step(user_msg)
print("Assistant Response:", response.msgs[0].content)