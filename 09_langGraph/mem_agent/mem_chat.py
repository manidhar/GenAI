from mem0 import Memory
from openai import OpenAI
import os
from dotenv import load_dotenv
import json
import gradio as gr

# --- Load environment variables ---
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# --- Initialize OpenAI client ---
client = OpenAI(api_key=OPENAI_API_KEY)
model = "gpt-4.1-mini"
embedding = "text-embedding-3-small"
USER_ID = "thasya"

# --- Configure mem0 (Qdrant vector DB) ---
config = {
    "version": "v1.1",
    "embedder": {
        "provider": "openai",
        "config": {
            "api_key": OPENAI_API_KEY,
            "model": embedding
        }
    },
    "llm": {
        "provider": "openai",
        "config": {
            "api_key": OPENAI_API_KEY,
            "model": model
        }
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": "localhost",
            "port": 6333
        }
    }
}

# --- Initialize Memory ---
mem_client = Memory.from_config(config)

# --- Function: Extract personal facts ---
def extract_facts(message):
    prompt = f"""
    You are a fact extractor. From the following message, extract any personal facts
    about the user (like their name, hobbies, interests, job, favorites, relationships, etc.).
    Return them as simple sentences, e.g.:
    - The user's name is Thasya.
    - The user likes Italian food.
    - The user works in software engineering.

    If there are no personal facts, return "No personal facts found."

    Message: "{message}"
    """

    fact_response = client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": prompt}]
    )

    facts = fact_response.choices[0].message.content.strip()
    return [] if "No personal facts" in facts else facts.split("\n")

# --- Function: Chat with memory ---
def chat_with_memory(user_query, history):
    # 1️⃣ Retrieve related memories
    search_memory = mem_client.search(query=user_query, user_id=USER_ID)
    results = search_memory.get("results", [])
    memory_context = "\n".join(f"- {mem.get('memory')}" for mem in results)

    # 2️⃣ Build system prompt
    SYSTEM_PROMPT = f"""
    You are a friendly assistant that remembers facts about the user.
    Use the information below to personalize your response.
    User Memory:
    {memory_context or "No known memory yet."}
    """

    # 3️⃣ Generate AI reply
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_query}
        ]
    )

    ai_response = response.choices[0].message.content

    # 4️⃣ Extract and store new facts
    facts = extract_facts(user_query)
    if facts:
        for fact in facts:
            mem_client.add(user_id=USER_ID, messages=[{"role": "system", "content": fact}])

    # 5️⃣ Save the chat itself
    mem_client.add(
        user_id=USER_ID,
        messages=[
            {"role": "user", "content": user_query},
            {"role": "assistant", "content": ai_response}
        ]
    )

    # 6️⃣ Update Gradio chat history
    history.append((user_query, ai_response))
    return history, history, f"🧠 Retrieved memory:\n{memory_context or '(none)'}"

# --- Gradio UI ---
with gr.Blocks(title="Smart Memory Chatbot 🤖") as demo:
    gr.Markdown("# 🧠 Smart Memory Chatbot\nThis bot remembers your facts and uses them naturally in conversation.")

    chatbox = gr.Chatbot(height=450)
    user_input = gr.Textbox(placeholder="Say something...")
    memory_output = gr.Textbox(label="Retrieved Memory", interactive=False)

    clear = gr.Button("🧹 Clear Chat")

    user_input.submit(chat_with_memory, [user_input, chatbox], [chatbox, chatbox, memory_output])
    clear.click(lambda: ([], [], "Memory cleared."), None, [chatbox, chatbox, memory_output])

if __name__ == "__main__":
    demo.launch()
