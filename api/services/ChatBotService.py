from agent.config.models_config import configs
from agent.facade.AgentFacade import SimpleAgentFacade
from api.services.ChatService import ChatService
from api.services.ChatMessageService import ChatMessageService
from dotenv import load_dotenv
import os
load_dotenv()

class ChatBotService:
    def __init__(self, model = configs['model1']):
        self.model_config = model
        
        # com rag tera download da base de conhecimento
        # client = MLflowClient()
        # client.download_artifact(os.getenv("MLFLOW_RUN_ID"))
        
        self.agent = SimpleAgentFacade()
        self.chat_service = ChatService()
        self.chat_message_service = ChatMessageService()

        print("-------------------- API DE EXEMPLO PARA AGENTES DE IA --------------------", flush=True)
        print("----> O serviço iniciou!", flush=True)
        print("----> Acesse http:/localhost:5000", flush=True)
    
    def conversar_com_agente(self,mensagem,uuid):
        chat = self.chat_service.get_chat_by_uuid(uuid)
        if chat is None:
            return None
        chat_id = chat["id"]
        response, metrics, obs, raw_output = self.agent.run(mensagem, uuid)
        self.chat_message_service.add_message(chat_id,
                                              mensagem,
                                              raw_output,
                                              metrics["input_tokens"],
                                              metrics["output_tokens"],
                                              metrics["latency"],
                                              obs)
        return {"resposta":response}