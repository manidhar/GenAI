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

Rule:
- Strictly follow the ouptut in JSON format

Output Format:
{
{
"code": "string" or None,
"isCodingQuestion": boolean
}
}

Examples:

Q: Can you explain a+b whole squared?
A: {{
"code": None,
"isCodingQuestion": false}}

Q: Write a python function to check if a number is prime.
A: {{
"code": "def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True",
"isCodingQuestion": true
}}

"""

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        # {
        #     "role": "user",
        #     "content": "Explain to me how AI works"
        # }
        {
            "role": "user",
            "content": "write java code to reverse a string"
        }
    ]
)
print(response.choices[0].message.content)
