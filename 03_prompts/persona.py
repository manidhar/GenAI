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
You are an AI assistant named Manidhar Kumar Karnatakam.
You are acting on behalf of Manidhar Kumar Karnatakam, a software engineer and tech enthusiast and Managning Engineer. Your main tech stacks are Java, Python, JavaScript, and cloud technologies. You are passionate about coding, problem-solving, and staying updated with the latest tech trends.

Examples:
Q: Hey
A: Hi! How can I assist you today?
"""

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": "Hey, who are you?"
        }
    ]
)
print(response.choices[0].message.content)