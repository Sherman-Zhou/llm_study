import os
from autogen import ConversableAgent
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
agent = ConversableAgent(
    name="chatbot",
    llm_config=llm_config,
    code_execution_config=False,
    human_input_mode="NEVER",
)

response = agent.generate_reply(
    messages=[{"role": "user", "content": "你是谁"}],
)
print(response)
