# Zero short prompting
from dotenv import load_dotenv
from openai import OpenAI
import os
load_dotenv()

BASE_URL=os.getenv("base_url")
API_KEY=os.getenv("GEMINI_API_KEY")


client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)
# zero-shot prompt: Directly giving the instructions to the model without any examples
SYSTEM_PROMPT="You should only and only answer the coding related questions. Do not answer anything else. Your name is ZeroBot. If your asks other than coding just say sorry I can't help with that."

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": "Explain to me how AI works"
        }
    ]
)
print(response.choices[0].message.content)
