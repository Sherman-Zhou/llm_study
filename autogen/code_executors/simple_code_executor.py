import os
from autogen import AssistantAgent, UserProxyAgent
from dotenv import load_dotenv

load_dotenv()

key_prefix= os.getenv("KEY_PREFIX")
api_key = os.getenv(f"{key_prefix}_API_KEY")
base_url = os.getenv(f"{key_prefix}_BASE_URL")

model = os.getenv(f"{key_prefix}_MODEL")

llm_config = {
    
    # "model": "llama3.2", # Loaded with LiteLLM command
    "model": model,
    # "api_key": "NotRequired", # Not needed
    "api_key": api_key,
    # "base_url": "http://localhost:11434/v1"  # Your LiteLLM URL
    "base_url": base_url 
}


assistant = AssistantAgent(
    name="Assistant",
    llm_config=llm_config,
)

user_proxy = UserProxyAgent(
    name="user",
    human_input_mode="ALWAYS",  
    code_execution_config={
        "work_dir": "coding",
        "use_docker": False,  # make it True if you want to use docker
    },
)

user_proxy.initiate_chat(
    # assistant, message="Plot a chart of META and TESLA stock price change."
    assistant, message="绘制META和TESLA股票价格变化的图表"
)

