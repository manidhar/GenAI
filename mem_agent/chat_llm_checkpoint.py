from typing import Annotated
from typing_extensions import TypedDict

from langgraph.graph import StateGraph,START,END
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.mongodb import MongoDBSaver
from dotenv import load_dotenv
import os
load_dotenv()

GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")
base_url=os.getenv("base_url")

llm = init_chat_model(
    model="gemini-2.5-flash",
    model_provider="google_genai",
    api_key=GEMINI_API_KEY
)

class State(TypedDict):
    messages: Annotated[list,add_messages]

graph_builder = StateGraph(State)

def chatbot(state:State):
    response=llm.invoke(state.get("messages"))
    #print(f"Chatbot Node : {state['messages']}")
    #print("\n\n")
    return {"messages": [response]}
    #return {"messages": ["Hi, This is a message from Chatbot Node!"]}



graph_builder.add_node("chatbot",chatbot)


graph_builder.add_edge(START,"chatbot")
graph_builder.add_edge("chatbot",END)

#graph=graph_builder.compile()

def compile_graph_with_checkpoint(checkpointer):
    return graph_builder.compile(checkpointer=checkpointer)  # <-- must return

DB_URL = "mongodb://localhost:27017/"

with MongoDBSaver.from_conn_string(DB_URL) as checkpointer:
    graph_with_checkpoint = compile_graph_with_checkpoint(checkpointer)
    config = {"configurable": {"thread_id": "manidhar"}}

    for chunk in graph_with_checkpoint.stream(
        {"messages": [{"role":"user","content":"what am i learning?"}]},
        config=config,
        stream_mode="values",   # <-- not 'steam_mode'
    ):
        last = chunk["messages"][-1]
        print(getattr(last, "content", last))
