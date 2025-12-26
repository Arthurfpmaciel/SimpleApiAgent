# controller dos resultados do sistema de lpr
from flask_restx import Namespace, Resource, fields
from flask import request, jsonify
from api.services.ChatService import ChatService

# instancia do service
service = ChatService()

# criação do namespace
chat_ns = Namespace("chat", description="operações com chats")

# criação dos modelos
criar_chat = chat_ns.model('CriarChat', {
    'nome': fields.String(required=True, description="Nome do chat"),
    # 'preferencia': fields.String(required=False, description="preferencia do usuário"),
})

buscar_id_model = chat_ns.model('BuscarPorId', {
    'id': fields.Integer(required=True, description="ID do chat")
})

buscar_uuid_model = chat_ns.model('BuscarPorUuid', {
    'uuid': fields.String(required=True, description="UUID do chat")
})

# criar registro
@chat_ns.route("/criar")
class CriarChat(Resource):
    @chat_ns.expect(criar_chat, validate=True)
    def post(self):
        data = request.json
        result = service.add_chat(data["nome"],None)
        return {"registro": result}, 201

# listar registros
@chat_ns.route("/listar")
class ListarChats(Resource):
    def post(self):
        results = service.list_chats()
        return {"registros": results}, 200

# buscar por id
@chat_ns.route("/buscar_por_id")
class BuscarPorID(Resource):
    @chat_ns.expect(buscar_id_model, validate=True)
    def post(self):
        data = request.json
        result = service.get_chat_by_id(data["id"])
        if result:
            return {"registro": result}, 200
        return {"error": "Resultado não encontrado"}, 404

@chat_ns.route("/buscar_por_uuid")
class BuscarPorUuid(Resource):
    @chat_ns.expect(buscar_uuid_model, validate=True)
    def post(self):
        data = request.json
        result = service.get_chat_by_uuid(data["uuid"])
        if result:
            return {"registro": result}, 200
        return {"error": "Resultado não encontrado"}, 404
    
# deletar por id
@chat_ns.route("/deletar")
class DeletarChat(Resource):
    @chat_ns.expect(buscar_id_model, validate=True)
    def delete(self):
        data = request.json
        result = service.delete_chat(data["id"])
        if result:
            return {"mensagem": "Registro deletado com sucesso"}, 200
        return {"error": "Registro não encontrado"}, 404