from dotenv import load_dotenv
import os
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

key_prefix= os.getenv('KEY_PREFIX')

# Retrieve API key and base URL from environment variables
api_key = os.getenv(f"{key_prefix}_API_KEY")
base_url = os.getenv(f"{key_prefix}_BASE_URL") 

print(f"url={base_url}, model={os.getenv(f"{key_prefix}_MODEL")}")

# Initialize the OpenAI client
client = OpenAI(api_key=api_key, base_url=base_url)

response = client.chat.completions.create(
    model= os.getenv(f"{key_prefix}_MODEL"),
    messages=[
        # {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "who are you?"},
    ],
    stream=False
)

print(response.choices[0].message.content)
