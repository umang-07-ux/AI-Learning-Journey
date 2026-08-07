import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
my_api_key=os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API not found")

client=Groq(api_key=my_api_key)

model="llama-3.3-70b-versatile"
role="user"
prompt="Suggest me a food brand name."

# SYSTEM:
message_system={
    "role":"system",
    "content":"You are a brand manager who suggest name for my food company.Name should be in one word.Give me one word answer only."
}

message={
    "role": role,
    "content": prompt
}

messages=[message_system,message]

# TEMPERATURE:
response=client.chat.completions.create(model=model , messages=messages ,temperature=1)     #By default the temperature is 0.
# print(response)

print("########################################################################################")

answer=response.choices[0].message.content
print(answer)