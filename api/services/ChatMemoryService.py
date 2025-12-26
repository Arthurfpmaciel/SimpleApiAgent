from api.repositories.ChatMessageRepository import ChatMessageRepository
from agent.memory.RedisMemory import RedisChatMemory
from langchain_core.messages import HumanMessage, AIMessage


class ChatMemoryService:
    def __init__(self):
        self.redis = RedisChatMemory()
        self.repo = ChatMessageRepository()
        self.limit = 10

    def load(self, session_id: str):
        history = self.redis.load(session_id)
        if history:
            return history
        db_history = self.repo.get_messages_by_chat_uuid(session_id, self.limit)
        messages = []
        for i in db_history:
            messages.append(HumanMessage(content=i["user_message"]))
            messages.append(AIMessage(content=i["assistant_message"]))
        self.redis.save(session_id, history)
        return history

    def append(self, session_id: str, messages: list):
        history = self.redis.load(session_id) or []
        history.extend(messages)
        history = history[-self.limit:]
        self.redis.save(session_id, history)