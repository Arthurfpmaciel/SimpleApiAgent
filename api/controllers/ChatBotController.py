# controller dos resultados do sistema de lpr
from flask_restx import Namespace, Resource, fields
from flask import request, jsonify
from api.services.ChatBotService import ChatBotService

# instancia do service
service = ChatBotService()

# criação do namespace
chatbot_ns = Namespace("chatbot", description="conversar com um agente")

# criação dos modelos
mensagem_model = chatbot_ns.model('ConversarComIA', {
    'mensagem': fields.String(required=True, description="Texto de entrada para o agente"),
    'uuid': fields.String(required=True, description="UUID do chat")
})

@chatbot_ns.route("/conversar_com_agente")
class ConversarComAgente(Resource):
    @chatbot_ns.expect(mensagem_model, validate=True)
    def post(self):
        data = request.json
        result = service.conversar_com_agente(data["mensagem"],data["uuid"])
        if result:
            return {"registro": result}, 200
        return {"error": "Usuário não encontrado"}, 404