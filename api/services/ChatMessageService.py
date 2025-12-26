from api.repositories.ChatMessageRepository import ChatMessageRepository

class ChatMessageService:
    def __init__(self):
        self.repo = ChatMessageRepository()

    def add_message(self, chat_id, user_message, assistant_message, input_tokens, output_tokens, request_duration, violation):
        new = self.repo.add_message(chat_id, user_message, assistant_message, input_tokens, output_tokens, request_duration, violation)
        return new
    
    def list_messages(self):
        return self.repo.get_all_messages()
    
    def get_message_by_id(self, id):
        return self.repo.get_messages_by_chat_id(id)
    
    def delete_message(self, id):
        return self.repo.delete_message(id)

    def get_messages_by_chat(self, chat_uuid):
        return self.repo.get_messages_by_chat_uuid(chat_uuid, n=10)