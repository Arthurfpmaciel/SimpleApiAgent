from api.configs.db_config import session_scope
from api.models.ChatMessageModel import ChatMessage
from api.models.ChatModel import Chat
from sqlalchemy import and_


class ChatMessageRepository:
    def add_message(self, chat_id:int, user_message:str, assistant_message:str, input_tokens:int, output_tokens:int, request_duration:float, violation:str):
        new_message = ChatMessage(
            chat_id = chat_id,
            user_message = user_message,
            assistant_message = assistant_message,
            input_tokens = input_tokens,
            output_tokens = output_tokens,
            request_duration = request_duration,
            violation = violation
        )
        with session_scope() as session:
            session.add(new_message)
            return new_message.to_dict()

    # retorna todos os registros
    def get_all_messages(self):
        with session_scope() as session:
            results = session.query(ChatMessage).all()
            results = [r.to_dict() for r in results]
            return results

    # retorna registro por id
    def get_messages_by_chat_id(self, message_id: int):
        with session_scope() as session:
            result = session.get(ChatMessage, message_id)
            if result:
                return result.to_dict()
            return None

    # deleta registro por id
    def delete_message(self, message_id:int):
        with session_scope() as session:
            result = session.get(ChatMessage, message_id)
            if result:
                session.delete(result)
                return True
            return False
        
    def get_messages_by_chat_uuid(self, chat_uuid: str, n:int):
        with session_scope() as session:
            chat = (
                session.query(Chat)
                .filter(Chat.uuid == chat_uuid)
                .first()
            )
            if not chat:
                return []
            messages = (
                session.query(ChatMessage)
                .filter(ChatMessage.chat_id == chat.id)
                .order_by(ChatMessage.created_at.desc())
                .limit(n)
                .all()
            )
            return [m.to_dict() for m in messages]
