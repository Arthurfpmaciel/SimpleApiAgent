from langchain_core.messages import SystemMessage, HumanMessage
from agent.factory.AgentFactory import AgentFactory
from agent.facade.policies.safety import InputGuardrail, OutputGuardrail
from agent.prompts.simple_agent_prompt import AGENT_SYSTEM_PROMPT
from agent.infrastructure.observability.Metrics import Metrics
from api.services.ChatMemoryService import ChatMemoryService

class SimpleAgentFacade:
    def __init__(self):
        self.agent = AgentFactory.create()
        self.in_g = InputGuardrail()
        self.out_g = OutputGuardrail()
        self.memory = ChatMemoryService()

    def run(self, user_input: str, session_id: str) -> str:
        user_input, obs = self.in_g(user_input)
        clean_output = ""
        metrics = Metrics()
        if obs is None:
            messages = [SystemMessage(content=AGENT_SYSTEM_PROMPT)] + self.memory.load(session_id) + [HumanMessage(content=user_input)]
            result = self.agent.invoke({"messages": messages})
            metrics = result.get("metrics")
            raw_output = result.get("output")
            obs = result.get("obs")
            
            clean_output = self.out_g.clean_llm_output(raw_output)
            self.memory.append(session_id, [{"role": "user", "content": user_input}, {"role": "assistant", "content": raw_output}])
        return clean_output, metrics.to_dict(), obs, raw_output