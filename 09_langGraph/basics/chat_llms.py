from typing import Optional, Literal
from typing_extensions import TypedDict

from langgraph.graph import StateGraph,START,END
from langchain.chat_models import init_chat_model
from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()

client = OpenAI()

GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")
base_url=os.getenv("base_url")

llm = init_chat_model(
    model="gemini-2.5-flash",
    model_provider="google_genai",
    api_key=GEMINI_API_KEY
)

class State(TypedDict):
    user_query: str
    llm_output: Optional[str]
    is_good: Optional[bool]

graph_builder = StateGraph(State)

def chatbot(state:State):
    print("Chatbot Node Invoked: ", state)
    response=client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": state.get("user_query")}
        ]
    )
    state["llm_output"] = response.choices[0].message.content
    return state
    

def evaluate_response(state:State)->Literal["chatbot_gemini", "end_node"]:
    print("\n")
    print("Evaluate Node Invoked: ", state)
    if False:
        return "end_node"
    else:
        return "chatbot_gemini"

def chatbot_gemini(state:State):
    print("\n")
    print("Gemini Node Invoked: ", state)
    response=llm.invoke([{"role": "user", "content": state.get("llm_output")}])
    state["llm_output"] =response
    return state

def end_node(state:State):
    return state

graph_builder.add_node("chatbot",chatbot)
graph_builder.add_node("chatbot_gemini",chatbot_gemini)
graph_builder.add_node("end_node",end_node)


graph_builder.add_edge(START,"chatbot")
graph_builder.add_conditional_edges("chatbot",evaluate_response)
graph_builder.add_edge("chatbot_gemini","end_node")
graph_builder.add_edge("end_node",END)

graph=graph_builder.compile()
output=graph.invoke(State({"user_query":"Explain AI in 1 line"}))
print('\n')
print(output)
