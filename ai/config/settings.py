from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class AgentConfig(BaseModel):
    model: str = "ollama:qwen3:8b"


class RedisConfig(BaseModel):
    host: str = "localhost"
    port: int = 6379


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    agent_config: AgentConfig = AgentConfig()
    redis_config: RedisConfig = RedisConfig()



settings = Settings()