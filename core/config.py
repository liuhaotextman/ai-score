import os
import yaml
from pydantic import BaseModel
from typing import Optional

class RedisConfig(BaseModel):
    Host: str
    Port: int
    Pass: str
    DB: int

class PgSQLConfig(BaseModel):
    Host: str
    Port: int
    User: str
    Pass: str
    DB: str

class GeminiConfig(BaseModel):
    TextModel: str
    EmbeddingModel: str

class Config(BaseModel):
    Redis: RedisConfig
    PgSQL: PgSQLConfig
    Gemini: GeminiConfig
    GeminiAPIKey: str

def load_config() -> Config:
    config_path = os.path.join(os.getcwd(), "config.yaml")
    with open(config_path, "r", encoding="utf-8") as f:
        config_data = yaml.safe_load(f)
    
    config_data["GeminiAPIKey"] = os.environ.get("GEMINI_API_KEY", "")
    
    return Config(**config_data)

settings = load_config()
