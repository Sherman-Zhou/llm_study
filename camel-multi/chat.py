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

agent = ChatAgent(
    model=model,
    # output_language='english'
)

response = agent.step("who are you")
print(response.msgs[0].content)