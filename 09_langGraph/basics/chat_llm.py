from typing import Annotated
from typing_extensions import TypedDict

from langgraph.graph import StateGraph,START,END
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
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
    print(f"Chatbot Node : {state['messages']}")
    print("\n\n")
    return {"messages": [response]}
    #return {"messages": ["Hi, This is a message from Chatbot Node!"]}


def sampleNode(state:State):
    print(f"Sample Node : {state['messages']}")
    print("\n\n")
    return {"messages": ["Hi, This is a message from Sample Node!"]}

graph_builder.add_node("chatbot",chatbot)
graph_builder.add_node("sampleNode",sampleNode)

graph_builder.add_edge(START,"chatbot")
graph_builder.add_edge("chatbot","sampleNode")
graph_builder.add_edge("sampleNode",END)

graph=graph_builder.compile()
output=graph.invoke({"messages":["Hi my name is Manidhar Karnatakam"]})
print(output)
