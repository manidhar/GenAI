from dotenv import load_dotenv
from openai import OpenAI
import requests
import os
load_dotenv()
BASE_URL=os.getenv("base_url")
API_KEY=os.getenv("GEMINI_API_KEY")

client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL)

def get_weather(city:str):
    url=f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)
    if response.status_code == 200:
        return f"The weather in {city} is {response.text}"
    else:
        return "Could not retrieve weather data."

def main():
    user_message = input("👉 ")
    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[
            {
                "role": "user",
                "content": user_message
            }
        ]
    )
    print("🤖:", response.choices[0].message.content)

if __name__ == "__main__":
    main()
    print(get_weather("Bangalore"))
    print(get_weather("Delhi"))