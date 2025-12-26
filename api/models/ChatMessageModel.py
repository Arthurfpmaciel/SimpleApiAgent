from api.configs.db_config import db

# modelo de registro das conversas do chatbot
class ChatMessage(db.Model):
    __tablename__ = 'chat_messages'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    chat_id = db.Column(db.Integer, db.ForeignKey('chats.id'), nullable=False)
    # mensagem enviada pelo usuário
    user_message = db.Column(db.Text, nullable=False)
    # resposta gerada pelo LLM
    assistant_message = db.Column(db.Text, nullable=False)
    # quantidade de tokens de entrada
    input_tokens = db.Column(db.Integer, nullable=True)
    # quantidade de tokens de saída
    output_tokens = db.Column(db.Integer, nullable=True)
    # custo estimado da requisição
    request_duration = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime,server_default=db.func.now())
    violation = db.Column(db.Text, nullable = True)
    
    def to_dict(self):
        return {
            "id": self.id,
            "chat_id": self.chat_id,
            "user_message": self.user_message,
            "assistant_message": self.assistant_message,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "request_duration": self.request_duration,
            "created_at": self.created_at,
            "violation":self.violation
            }
