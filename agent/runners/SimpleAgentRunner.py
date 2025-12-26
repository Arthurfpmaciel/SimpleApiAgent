import time
from typing import TypedDict, List, Annotated
from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage, SystemMessage
from langchain_groq import ChatGroq
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph.message import add_messages
from agent.infrastructure.observability.Metrics import Metrics

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    output: str
    metrics: dict

def llm_node(llm: ChatGroq):
    def _node(state: AgentState) -> dict:
        start = time.time()
        response = llm.invoke(state["messages"])
        latency = round(time.time() - start, 4)
        usage = response.usage_metadata or {}
        metrics_data = Metrics(latency,usage.get('input_tokens', 0),usage.get('output_tokens', 0))
        return {"messages":[response], "output": response.content, "metrics":metrics_data}
    return _node

def build_graph(llm: ChatGroq, tools):
    graph = StateGraph(AgentState)

    graph.add_node("llm", llm_node(llm))
    graph.add_node("tools", ToolNode(tools))
    graph.add_conditional_edges("llm",tools_condition)
    graph.add_edge("tools","llm")

    graph.set_entry_point("llm")
    
    return graph.compile()



