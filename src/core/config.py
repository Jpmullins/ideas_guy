from functools import lru_cache
from pydantic import BaseModel
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_provider: str = "huggingface"  # or "stub"
    hf_model_name: str = "distilgpt2"
    max_new_tokens: int = 128
    temperature: float = 0.9
    enable_cors: bool = True
    frontend_mount_path: str = "/"
    assets_dir: str = "assets"

    class Config:
        env_file = ".env"


class AppInfo(BaseModel):
    name: str = "Ideas Guy Chatbot"
    version: str = "0.1.0"
    description: str = "Satirical 'ideas guy' personality chatbot"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()  # reads env

