from langchain_groq import ChatGroq
from agent.runners.SimpleAgentRunner import build_graph
from agent.config.models_config import configs
from agent.tools.multi_agent_tools import tools

class AgentFactory:
    @staticmethod
    def create():
        model1 = configs["model1"]
        model = model1["name"]
        temperature = model1["temperature"]
        llm = ChatGroq(model=model, temperature=temperature).bind_tools(tools)
        agent = build_graph(llm, tools)
        return agent
