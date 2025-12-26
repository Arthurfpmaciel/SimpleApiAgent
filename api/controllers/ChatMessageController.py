# controller dos resultados do sistema de lpr
from flask_restx import Namespace, Resource, fields
from flask import request, jsonify
import numpy as np
from api.services.ChatMessageService import ChatMessageService

# instancia do service
service = ChatMessageService()

# criação do namespace
message_ns = Namespace("mensagem", description="operações com os registros de mensagens")

# criação dos modelos
buscar_id_model = message_ns.model('BuscarPorId', {
    'id': fields.Integer(required=True, description="ID da mensagem")
})

buscar_uuid_chat_model = message_ns.model('BuscarPorUuidChat', {
    'uuid': fields.String(required=True, description="UUID do chat")
})

# criação das requisições
# listar registros
@message_ns.route("/listar")
class ListarConversas(Resource):
    def post(self):
        results = service.list_messages()
        return {"registros": results}, 200

# buscar por id
@message_ns.route("/buscar_por_id")
class BuscarPorID(Resource):
    @message_ns.expect(buscar_id_model, validate=True)
    def post(self):
        data = request.json
        result = service.get_message_by_id(data["id"])
        if result:
            return {"registro": result}, 200
        return {"error": "Resultado não encontrado"}, 404

@message_ns.route("/buscar_por_uuid_chat")
class BuscarPorUuidChat(Resource):
    @message_ns.expect(buscar_uuid_chat_model, validate=True)
    def post(self):
        data = request.json
        result = service.get_messages_by_chat(data["uuid"])
        if result:
            return {"registro": result}, 200
        return {"error": "Resultado não encontrado"}, 404