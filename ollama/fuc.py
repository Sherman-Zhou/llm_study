from openai import AsyncOpenAI
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel

openai_client = AsyncOpenAI(
    api_key="test",
    base_url="http://localhost:11434/v1",
)
# 如果你创建的模型名称不是 deepseek-v3t，需要自己修改
# model = OpenAIModel("deepseek-v3t", openai_client=openai_client)
model = OpenAIModel("deepseek-r1:7b", openai_client=openai_client)

agent = Agent(
    model
)

# 为 agent 添加一个工具函数
@agent.tool
async def get_time():
    import datetime
    return f"Current time is {datetime.datetime.now()}"

async def main():
    response = await agent.run("What time is it?")
    print(response)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
