from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
import os

BASE_URL=os.getenv("base_url")
API_KEY=os.getenv("GEMINI_API_KEY")


client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
    
        {
            "role": "user",
            "content": "Explain to me how AI works"
        }
    ]
)
print(response.choices[0].message.content)