import os

from autogen import ConversableAgent, LLMConfig
from dotenv import load_dotenv
load_dotenv()
key_prefix = os.getenv("KEY_PREFIX")
api_key = os.getenv(f"{key_prefix}_API_KEY")
base_url = os.getenv(f"{key_prefix}_BASE_URL")
model = os.getenv(f"{key_prefix}_MODEL")
llm_config=LLMConfig(api_type="openai", model=model, api_key=api_key,base_url=base_url)



with llm_config:
    student_agent = ConversableAgent(
        name="Student_Agent",
        system_message="You are a student willing to learn.",
    )
    teacher_agent = ConversableAgent(
        name="Teacher_Agent",
        system_message="You are a math teacher.",
    )

chat_result = student_agent.initiate_chat(
    teacher_agent,
    message="What is triangle inequality?",
    # summary_method="reflection_with_llm",
    max_turns=2,
)

print(chat_result.summary)