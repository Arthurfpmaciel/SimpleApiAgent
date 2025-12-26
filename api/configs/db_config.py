# configuração do banco de dados
from flask_sqlalchemy import SQLAlchemy
from contextlib import contextmanager

# criação do objeto de integração do Flask com o SLQAlchemy que será configurado em ./create_app.py
db = SQLAlchemy()

# criação de um contexto seguro uso da sessão de banco de dados
@contextmanager
def session_scope():
    session = db.session
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        try:
            db.session.remove()
        except AttributeError:
            session.close()