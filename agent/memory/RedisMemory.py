import redis
import json
from dotenv import load_dotenv
import os
load_dotenv(".env")
redis_port = int(os.getenv("REDIS_PORT"))
class RedisChatMemory:
    # caso a api esteja rodando localmente, mude o host para localhost
    def __init__(self, host="redis", port= redis_port, ttl=3600):
        self.redis = redis.Redis(
            host=host,
            port=port,
            decode_responses=True
        )
        self.ttl = ttl

    def _key(self, session_id):
        return f"chat:{session_id}"

    def load(self, session_id):
        data = self.redis.get(self._key(session_id))
        return json.loads(data) if data else []

    def save(self, session_id, history):
        self.redis.set(
            self._key(session_id),
            json.dumps(history),
            ex=self.ttl
        )