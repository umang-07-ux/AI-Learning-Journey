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

# 3 prompts

prompt1="Hi!"
prompt2="Explain time travel in brief"
prompt3="Write a 200 word essay on Machine Learning"

prompts=[prompt1,prompt2,prompt3]
for prompt in prompts:
    message={
        "role": role,
        "content": prompt
    }
    messages=[message]
    response=client.chat.completions.create(model=model , messages=messages , max_tokens=50)
    answer=response.choices[0].message.content
    usage=response.usage

    # Printing Each answer
    print("ANSWER")
    print(answer)

    print()
    # Then its token usage
    print(f"Prompt:{prompt} -->your tokens: {usage.prompt_tokens} completion_tokens: {usage.completion_tokens} total tokens: {usage.total_tokens} Finish Reason: {response.choices[0].finish_reason}")

    # If Finish reason is 'stop' that means answer max_tokens ki limit ke andar khatam ho gaya par agar 
    # Finish reason 'length' hai toh iska matlab answer khatam hone se pehle hi max_tokens ki limit reach ho gayi.

    print('-' *100)