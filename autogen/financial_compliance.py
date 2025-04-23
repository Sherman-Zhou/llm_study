import os
import random
from typing import Annotated, Any
from datetime import datetime, timedelta

from autogen import ConversableAgent, AfterWorkOption, initiate_swarm_chat, LLMConfig, register_function

# Note: Make sure to set your API key in your environment first

# Configure the LLM
llm_config = LLMConfig(
    api_type="openai",
    model="gpt-4o-mini",
    api_key=os.environ.get("OPENAI_API_KEY"),
    temperature=0.2,
)

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

# Define the system message for the summary agent
summary_system_message = """
You are a financial summary assistant. You will be given a set of transaction details and their approval status.
Your task is to summarize the results of the transactions processed by the finance bot.
Generate a markdown table with the following columns:
- Vendor
- Memo
- Amount
- Status (Approved/Rejected)
- Reason (especially note if rejected due to being a duplicate)

The summary should include the total number of transactions, the number of approved transactions, and the number of rejected transactions.
The summary should be concise and clear.

Once you've generated the summary append the below in the summary:
==== SUMMARY GENERATED ====
"""

# Create the finance agent with LLM intelligence
with llm_config:
    finance_bot = ConversableAgent(
        name="finance_bot",
        system_message=finance_system_message,
        functions=[check_duplicate_payment],
    )
    summary_bot = ConversableAgent(
        name="summary_bot",
        system_message=summary_system_message,
    )

# Create the human agent for oversight
human = ConversableAgent(
    name="human",
    human_input_mode="ALWAYS",  # Always ask for human input
)

def is_termination_msg(msg: dict[str, Any]) -> bool:
    content = msg.get("content", "")
    return (content is not None) and "==== SUMMARY GENERATED ====" in content

# Generate sample transactions - this creates different transactions each time you run
VENDORS = ["Staples", "Acme Corp", "CyberSins Ltd", "Initech", "Globex", "Unicorn LLC"]
MEMOS = ["Quarterly supplies", "Confidential", "NDA services", "Routine payment", "Urgent request", "Reimbursement"]

# Generate new transactions including a duplicate
transactions = [
    "Transaction: $500 to Staples. Memo: Quarterly supplies.",  # Duplicate of an existing transaction
    "Transaction: $4000 to Unicorn LLC. Memo: Reimbursement.",
    "Transaction: $12000 to Globex. Memo: Confidential.",  # Duplicate of an existing transaction
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
        "llm_config": llm_config,
        "is_termination_msg": is_termination_msg,
    },
    after_work=AfterWorkOption.SWARM_MANAGER
)