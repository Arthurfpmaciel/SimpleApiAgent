from api.repositories.ChatRepository import ChatRepository

class ChatService:
    def __init__(self):
        self.repo = ChatRepository()

    def add_chat(self, name, user_preferences):
        new = self.repo.add_chat(name, user_preferences)
        return new
    
    def list_chats(self):
        return self.repo.get_all_chats()
    
    def get_chat_by_id(self, id):
        return self.repo.get_chat_by_id(id)
    
    def get_chat_by_uuid(self, uuid):
        return self.repo.get_chat_by_uuid(uuid)
    
    def delete_chat(self, id):
        return self.repo.delete_chat(id)