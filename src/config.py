import json
from typing import Any

from pydantic import BaseSettings


class ModelVkBot(BaseSettings):
    VK_BOT_TOKEN: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


class ModelBaseCache(BaseSettings):
    CACHE_TYPE: str
    CACHE_HOST: str | None
    CACHE_PORT: int | None


class ModelProdCache(ModelBaseCache):
    CACHE_TYPE: str
    CACHE_HOST: str | None
    CACHE_PORT: int | None

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


class ModelTestsCache(ModelBaseCache):
    CACHE_TYPE: str
    CACHE_HOST: str | None
    CACHE_PORT: int | None

    class Config:
        env_file = './config/.env.test'
        env_file_encoding = 'utf-8'


with open('logger_config.json', 'r', encoding='utf-8') as file:
    LOGGER_CONFIG: dict[str, Any] = json.load(file)
