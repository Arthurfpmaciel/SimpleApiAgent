# configuração da api restful
import os
from flask import render_template
from flask_restx import Api, Swagger, apidoc
from werkzeug.utils import cached_property
from api.controllers.ChatBotController import chatbot_ns
from api.controllers.ChatController import chat_ns
from api.controllers.ChatMessageController import message_ns

prefix = os.environ.get("BASE_PATH", "")
base_url = os.environ.get("BASE_URL", "")

# definindo o swagger
class ApiSwagger(Api):
    @cached_property
    def __schema__(self):
        if not self._schema:
            try:
                self._schema = Swagger(self).as_dict()
                self._schema["host"] = base_url
            except Exception:
                return {"error": "Unable to render schema"}
        return self._schema

@apidoc.apidoc.add_app_template_global
def swagger_static(filename):
    return f"{prefix}/swaggerui/{filename}"

api = ApiSwagger(
    title="API Agente",
    version="1.0.0", # modelo Major.Minor.Patch
    description="API para agente",
)
@api.documentation
def custom_ui():
    return render_template(
        "swagger-ui.html", title=api.title, specs_url=f"{prefix}/swagger.json"
    )

# aqui abaixo são definidos os namespaces
api.add_namespace(chatbot_ns, path=f"{prefix}/chatbot")
api.add_namespace(chat_ns, path=f"{prefix}/chat")
api.add_namespace(message_ns, path=f"{prefix}/message")
