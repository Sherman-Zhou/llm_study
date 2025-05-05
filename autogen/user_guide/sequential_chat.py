from autogen import ConversableAgent, LLMConfig

from dotenv import load_dotenv
import os
load_dotenv()
key_prefix = os.getenv("KEY_PREFIX")
api_key = os.getenv(f"{key_prefix}_API_KEY")
base_url = os.getenv(f"{key_prefix}_BASE_URL")
model = os.getenv(f"{key_prefix}_MODEL")
llm_config=LLMConfig(api_type="openai", model=model, api_key=api_key,base_url=base_url)

# Three chats:
# 1. Teacher and Curriculum designer > summary is a topic for next chat
# 2. Teacher and Lesson planner (with 1 revision) > summary is lesson plan for next chat
# 3. Teacher and Formatter > summary is a formatted lesson plan

# Curriculum designer
curriculum_message = """You are a curriculum designer for a fourth grade class. Nominate an appropriate a topic for a lesson, based on the given subject."""

# Lesson planner
planner_message = """You are a classroom lesson agent.
Given a topic, write a lesson plan for a fourth grade class in bullet points. Include the title, learning objectives, and script.
"""

# Formatter
formatter_message = """You are a lesson plan formatter. Format the complete plan as follows:
<title>Lesson plan title</title>
<learning_objectives>Key learning objectives</learning_objectives>
<script>How to introduce the topic to the kids</script>
"""

# Teacher who initiates the chats
teacher_message = """You are a classroom teacher.
You decide topics for lessons and work with a lesson planner, you provide one round of feedback on their lesson plan.
Then you will work with a formatter to get a final output of the lesson plan.
"""

with llm_config:
    lesson_curriculum = ConversableAgent(
        name="curriculm_agent",
        system_message=curriculum_message,
    )

    lesson_planner = ConversableAgent(
        name="planner_agent",
        system_message=planner_message,
    )

    lesson_formatter = ConversableAgent(
        name="formatter_agent",
        system_message=formatter_message,
    )

    teacher = ConversableAgent(
        name="teacher_agent",
        system_message=teacher_message,
    )

# Our sequential chat, each chat is a chat between the teacher and the recipient agent
# max_turns determines if there's back and forth between the teacher and the recipient
# max_turns = 1 means no back and forth
chat_results = teacher.initiate_chats(
    [
        {
            "recipient": lesson_curriculum,
            "message": "Let's create a science lesson, what's a good topic?",
            "max_turns": 1,
            "summary_method": "last_msg",
        },
        {
            "recipient": lesson_planner,
            "message": "Create a lesson plan.",
            "max_turns": 2, # One revision
            "summary_method": "last_msg",
        },
        {
            "recipient": lesson_formatter,
            "message": "Format the lesson plan.",
            "max_turns": 1,
            "summary_method": "last_msg",
        },
    ]
)

# The result of `initiate_chats` is a list of chat results
# each chat result has a summary
print("\n\nCurriculum summary:\n", chat_results[0].summary)
print("\n\nLesson Planner summary:\n", chat_results[1].summary)
print("\n\nFormatter summary:\n", chat_results[2].summary)

#1. teacher_agent (to curriculm_agent):
#2. curriculm_agent (to teacher_agent):

#max tunes 2
#3. teacher_agent (to planner_agent):
#4. planner_agent (to teacher_agent)
#5. teacher_agent (to planner_agent):
#6. planner_agent (to teacher_agent):

#7.teacher_agent (to formatter_agent):
#8.formatter_agent (to teacher_agent):

