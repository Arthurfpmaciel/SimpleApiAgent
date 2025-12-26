from api.configs.db_config import session_scope
from api.models.ChatModel import Chat

class ChatRepository:
    def add_chat(self, name, user_preferences):
        new_chat = Chat(name=name,
                        user_preferences=user_preferences)
        with session_scope() as session:
            session.add(new_chat)
            return new_chat.to_dict()

    # retorna todos os registros
    def get_all_chats(self):
        with session_scope() as session:
            results = session.query(Chat).all()
            results = [r.to_dict() for r in results]
            return results

    # retorna registro por id
    def get_chat_by_id(self, chat_id):
        with session_scope() as session:
            result = session.get(Chat, chat_id)
            if result:
                return result.to_dict()
            return None
        
    def get_chat_by_uuid(self, chat_uuid: str):
        with session_scope() as session:
            chat = (
                session.query(Chat)
                .filter(Chat.uuid == chat_uuid)
                .first()
            )
            if not chat:
                return None
            return chat.to_dict()

    # deleta registro por id
    def delete_chat(self, chat_id):
        with session_scope() as session:
            result = session.get(Chat, chat_id)
            if result:
                session.delete(result)
                return True
            return False