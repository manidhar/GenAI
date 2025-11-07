from mem0 import Memory
import os
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr
import json

load_dotenv()
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
#GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")
#base_url=os.getenv("base_url")
model="gpt-4.1-mini"
embedding="text-embedding-3-small"
client = OpenAI()
config={
    "version":"v1.1",
    "embedder":{
        "provider":"openai",
        "config":{
            "api_key":OPENAI_API_KEY,
            "model":embedding
            }
    },
    "llm":{
        "provider":"openai",
        "config":{
            "api_key":OPENAI_API_KEY,
            "model":"gpt-4.1"
            }
    },
    "vector_store":{
        "provider":"qdrant",
        "config":{
            "host":"localhost",
            "port":6333}
    }
    
}

mem_client=Memory.from_config(config)

while True:

    user_query=input("👉")
    # search for memory
    search_memory=mem_client.search(query=user_query,user_id="thasya")
    print("Search Memory: ",search_memory)
    memories=[
        f"ID : {mem.get("id")}\nMemory: {mem.get("memory")}" for mem in search_memory.get("results")
    ]
    print("Found memories...",memories)
    SYSTEM_PROMPT=f"""
        You are a fact extractor. From the following message, extract any personal facts
    about the user (like their name, hobbies, interests, job, favorites, relationships, etc.).
        {json.dumps(memories,indent=2)}
    """

    response=client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role":"system","content":SYSTEM_PROMPT},
            {"role":"user","content":user_query}
        ]
    )
    ai_response=response.choices[0].message.content
    print("AI : ",ai_response)
    messages=[
            {"role":"user","content":user_query},
            {"role":"assistant","content":ai_response}
        ]

    mem_client.add(messages,user_id="thaysa")

    print("Memory has been saved...")
