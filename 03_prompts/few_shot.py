# few short prompting
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()
BASE_URL=os.getenv("base_url")
API_KEY=os.getenv("GEMINI_API_KEY")
client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL)
# few-shot prompt: Directly giving the instructions to the model along with some examples
SYSTEM_PROMPT="""You should only and only answer the coding related questions. Do not answer anything else. Your name is ZeroBot. If your asks other than coding just say sorry I can't help with that.

Examples:

Q: Can you explain a+b whole squared?
A: Sorry I can can help with Coding related questions only.

Q: Write a python function to check if a number is prime.
A:
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True
"""

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": "write program to implement fibonacci series in python"
        }
    ]
)
print(response.choices[0].message.content)
