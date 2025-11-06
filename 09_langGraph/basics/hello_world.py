from typing import TypedDict
from langgraph.graph import END, START, StateGraph
from util.langgraph_util import display  # relative import from basics to util

class HelloWorldState(TypedDict):
    message: str

def hello(state: HelloWorldState):
    print(f"Hello Node : {state['message']}")
    return {"message": "Hello  " + state['message']}

def bye(state: HelloWorldState):
    print(f"Bye Node : {state['message']}")
    return {"message": "Bye  " + state['message']}


graph=StateGraph(HelloWorldState)
graph.add_node("hello",hello)
graph.add_node("bye",bye)

graph.add_edge(START,"hello")
# graph.set_entry_point("hello") line 20 & 21 perform same function
graph.add_edge("hello","bye")
graph.add_edge("bye",END)

runnable=graph.compile()
output =runnable.invoke({"message":"Manidhar"})
display(runnable)
print(output)