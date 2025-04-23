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

assistant = AssistantAgent("assistant", llm_config)
user_proxy = UserProxyAgent(
    "user_proxy",
    llm_config=llm_config,
    code_execution_config={
        "workd_dir": "code_execution",
        "use_docker": False,
    },
    human_input_mode="NEVER",
)

# start the agents
user_proxy.initiate_chat(
    assistant,
    message="法国的首都是哪个?",
)
