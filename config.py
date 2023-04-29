import os

from dotenv import load_dotenv

load_dotenv()
load_dotenv('.env.test')


class Production:
    VK_BOT_TOKEN = os.environ.get('VK_BOT_TOKEN')

    TYPE_CACHE = os.environ.get('TYPE_CACHE')

    REDIS_HOST = os.environ.get('REDIS_HOST')
    REDIS_PORT = os.environ.get('REDIS_PORT')


class Test:
    TYPE_CACHE = os.environ.get('TEST_TYPE_CACHE')
    REDIS_HOST = os.environ.get('TEST_REDIS_HOST')
    REDIS_PORT = os.environ.get('TEST_REDIS_PORT')
