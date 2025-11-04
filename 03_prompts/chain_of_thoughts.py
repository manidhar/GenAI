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

SYSTEM_PROMPT="""
You are an expert AI assistant in resolving queries using chain of thoughts.
You work on START,PLAN and OUTPUT steps.
You need to first PLAN whats needs to be done. The PLAN can be multiple steps.
Once you think enough PLAN has been done, finally you can give the OUTPUT.

Rule:
- Strictly Follow the ouptut in JSON format
- Only run one step at a time.
- The sequence of steps is START (where user gives an input), PLAN (That can be multiple times) and finally OUTPUT (which is going to bes displayed to the user).

Output JSON Format:
{"step": "START"| "PLAN" | "OUTPUT","content": "string"}

Example:
START: Hey, can you solve 2+3*5/10
PLAN:{"step":"PLAN","content":"Seems like user is interested in solving a mathematical expression."}
PLAN:{"step":"PLAN","content":"Looking at the problem, I need to follow BODMAS rule."}
PLAN:{"step":"PLAN","content":"BODMAS stands for Brackets, Orders (i.e. powers and square roots, etc.), Division and Multiplication, Addition and Subtraction."}
PLAN:{"step":"PLAN","content":"BOADMAS seems to be the correct rule."}
PLAN:{"step":"PLAN","content":"First I will solve 3*5=15"}
PLAN:{"step":"PLAN","content":"Then I will solve 15/10=1.5"}
PLAN:{"step": "PLAN", "content": "Finally I will add 2+1.5=3.5"}
OUTPUT:{"step":"OUTPUT","content":"The final answer to the expression 2+3*5/10 is 3.5"}

"""
response = client.chat.completions.create(
    model="gemini-2.5-flash",
    response_format={"type": "json_object"},
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
       
        {
            "role": "user",
            "content": "write java code to reverse a string"
        },
        {
            "role": "assistant",
            "content": '''{"step":"START","content":"Sure! I can help you with that."}'''
        },{
            "role": "assistant",
            "content": '''{
            "step": "PLAN",
 "content": "The user wants Java code to reverse a string. I should provide a clear and concise Java code example."
}'''
        },
        {
            "role": "assistant",
            "content": '''
{"step": "PLAN", "content": "I will provide a Java method that takes a string as input and returns its reversed version."}
'''
        }
    ]
)
print(response.choices[0].message.content)