import os
import random
import json
from typing import Annotated, Any, List, Dict
from datetime import datetime, timedelta
from pydantic import BaseModel

from autogen import ConversableAgent, AfterWorkOption, initiate_swarm_chat, LLMConfig, register_function

# Mock database of previous transactions
def get_previous_transactions() -> list[dict[str, Any]]:
    return [
        {"vendor": "Staples", "amount": 500, "date": "2025-04-15", "memo": "Quarterly supplies"},
        {"vendor": "Acme Corp", "amount": 1500, "date": "2025-04-16", "memo": "NDA services"},
        {"vendor": "Globex", "amount": 12000, "date": "2025-04-17", "memo": "Confidential"},
    ]

# Simple duplicate detection function
def check_duplicate_payment(
    vendor: Annotated[str, "The vendor name"],
    amount: Annotated[float, "The transaction amount"],
    memo: Annotated[str, "The transaction memo"]
) -> dict[str, Any]:
    """Check if a transaction appears to be a duplicate of a recent payment"""
    previous_transactions = get_previous_transactions()

    today = datetime.now()

    for tx in previous_transactions:
        tx_date = datetime.strptime(tx["date"], "%Y-%m-%d")
        date_diff = (today - tx_date).days

        # If vendor, memo and amount match, and transaction is within 7 days
        if (
            tx["vendor"] == vendor and
            tx["memo"] == memo and
            tx["amount"] == amount and
            date_diff <= 7
        ):
            return {
                "is_duplicate": True,
                "reason": f"Duplicate payment to {vendor} for ${amount} on {tx['date']}"
            }

    return {
        "is_duplicate": False,
        "reason": "No recent duplicates found"
    }

# Configure the LLM for finance bot (standard configuration)
finance_llm_config = LLMConfig(
    api_type="openai",
    model="gpt-4o-mini",
    api_key=os.environ.get("OPENAI_API_KEY"),
    temperature=0.2
)

# Define the system message for our finance bot
finance_system_message = """
You are a financial compliance assistant. You will be given a set of transaction descriptions.

For each transaction:
1. First, extract the vendor name, amount, and memo
2. Check if the transaction is a duplicate using the check_duplicate_payment tool
3. If the tool identifies a duplicate, automatically reject the transaction
4. If not a duplicate, continue with normal evaluation:
    - If it seems suspicious (e.g., amount > $10,000, vendor is unusual, memo is vague), ask the human agent for approval
    - Otherwise, approve it automatically

Provide clear explanations for your decisions, especially for duplicates or suspicious transactions.
When all transactions are processed, summarize the results and say "You can type exit to finish".
"""

# Create the agents with respective LLM configurations
with finance_llm_config:
    finance_bot = ConversableAgent(
        name="finance_bot",
        system_message=finance_system_message,
        functions=[check_duplicate_payment],
    )

# Create the human agent for oversight
human = ConversableAgent(
    name="human",
    human_input_mode="ALWAYS",  # Always ask for human input
)

# Define structured output for audit logs
class TransactionAuditEntry(BaseModel):
    vendor: str
    amount: float
    memo: str
    status: str  # "approved" or "rejected"
    reason: str

class AuditLogSummary(BaseModel):
    total_transactions: int
    approved_count: int
    rejected_count: int
    transactions: List[TransactionAuditEntry]
    summary_generated_time: str

# Configure the LLM for summary bot with structured output
summary_llm_config = LLMConfig(
    api_type="openai",
    model="gpt-4o-mini",
    api_key=os.environ.get("OPENAI_API_KEY"),
    temperature=0.2,
    response_format=AuditLogSummary,  # Using the Pydantic model for structured output
)

# Define the system message for the summary agent
# Note: No formatting instructions needed!
summary_system_message = """
You are a financial summary assistant that generates audit logs.
Analyze the transaction details and their approval status from the conversation.
Include each transaction with its vendor, amount, memo, status and reason.
"""

with summary_llm_config:
    summary_bot = ConversableAgent(
        name="summary_bot",
        system_message=summary_system_message,
    )

def is_termination_msg(x: dict[str, Any]) -> bool:
    content = x.get("content", "")
    try:
        # Try to parse the content as JSON (structured output)
        data = json.loads(content)
        return isinstance(data, dict) and "summary_generated_time" in data
    except:
        # If not JSON, check for text marker
        return (content is not None) and "==== SUMMARY GENERATED ====" in content

# Generate new transactions including a duplicate
transactions = [
    "Transaction: $500 to Staples. Memo: Quarterly supplies.",  # Duplicate
    "Transaction: $4000 to Unicorn LLC. Memo: Reimbursement.",
    "Transaction: $12000 to Globex. Memo: Confidential.",  # Duplicate
    "Transaction: $9999 to Initech. Memo: Urgent request."
]

# Format the initial message
initial_prompt = (
    "Please process the following transactions one at a time, checking for duplicates:\n\n" +
    "\n".join([f"{i+1}. {tx}" for i, tx in enumerate(transactions)])
)

result, _, _ = initiate_swarm_chat(
    initial_agent=finance_bot,
    agents=[finance_bot, summary_bot],
    user_agent=human,
    messages=initial_prompt,
    swarm_manager_args={
        "llm_config": finance_llm_config,
        "is_termination_msg": is_termination_msg,
    },
    after_work=AfterWorkOption.SWARM_MANAGER
)

# Pretty-print the transaction_data
final_message = result.chat_history[-1]["content"]
structured_data = json.loads(final_message)
print(json.dumps(structured_data, indent=4))