import os
from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel


# --------------------------------------------------
# 1. Load API key from .env
# --------------------------------------------------

load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API key not found")


# Create Groq client
client = Groq(api_key=my_api_key)


# --------------------------------------------------
# 2. Model
# --------------------------------------------------

model = "openai/gpt-oss-120b"


# --------------------------------------------------
# 3. Create Pydantic model
# --------------------------------------------------

class Ticket(BaseModel):
    name: str
    email: str
    issue: str
    phone_number: int


# Convert Pydantic model → JSON Schema
schema = Ticket.model_json_schema()


# --------------------------------------------------
# 4. Tell Groq to return JSON
# --------------------------------------------------

response_format = {
    "type": "json_object"
}


# --------------------------------------------------
# 5. System prompt
# --------------------------------------------------

system_prompt = f"""
Extract the following information from the customer ticket.

Return ONLY valid JSON.

Follow this schema:

{schema}
"""


message_system = {
    "role": "system",
    "content": system_prompt
}


# --------------------------------------------------
# 6. Customer ticket
# --------------------------------------------------

text = """
Hello my name is Umang Srivastava.
I have an iPhone which is not working at all.
My address is Delhi.
My email is abc@gmail.com.
My contact number is 36464637.
"""


prompt = f"""
This is a customer ticket.
Extract the required information from it.

Ticket:
{text}
"""


message = {
    "role": "user",
    "content": prompt
}


messages = [message_system, message]


# --------------------------------------------------
# 7. Send request to Groq
# --------------------------------------------------

response = client.chat.completions.create(
    model=model,
    messages=messages,
    response_format=response_format
)


# --------------------------------------------------
# 8. Get JSON response from LLM
# --------------------------------------------------
answer = response.choices[0].message.content

print("Raw JSON:")
print(answer)


# --------------------------------------------------
# 9. JSON → Pydantic + Validation
# --------------------------------------------------

ticket = Ticket.model_validate_json(answer)

print("\nValidated Pydantic object:")
print(ticket)


# Access individual fields
print("\nName:", ticket.name)
print("Email:", ticket.email)
print("Issue:", ticket.issue)
print("Phone:", ticket.phone_number)