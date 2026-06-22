from redis import Redis
from langgraph.checkpoint.redis import AsyncRedisSaver

from ai.config.settings import settings

client = Redis(
    host=settings.redis_config.host,
    port=settings.redis_config.port,  
)

saver = AsyncRedisSaver(redis_client=client)
saver.setup()