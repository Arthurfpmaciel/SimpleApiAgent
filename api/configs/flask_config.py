# configurações da aplicação flask
import os
from dotenv import load_dotenv
load_dotenv('.env')

# classe que estabelece as configurações da aplicação flask baseada no ./.env
class Config:
    # URI do banco de dados: string padrão que define o acesso a um banco de dados
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # chave secreta do flask
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default-secret-key')
    # modo de execução do flask: 'development' ou 'production'
    FLASK_ENV = os.environ.get('FLASK_ENV', 'development')