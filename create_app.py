from flask import Flask
from api.configs.flask_config import Config
from api.configs.db_config import db
from api.configs.restx_config import api
from flask_cors import CORS

# construção da aplicação flask
def create_app(config_class=Config):
    app = Flask(__name__)
    # politica de segurança que limita as requisições ao dominio do servidor da api
    CORS(app)
    # cofiguração da aplicação flask
    app.config.from_object(config_class)
    # inicialização do banco
    db.init_app(app)
    # inicialização da api restuful
    api.init_app(app)
    # construção do banco de dados
    with app.app_context():
        db.create_all()
    return app