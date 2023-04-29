import os
import sys

from dotenv import load_dotenv

load_dotenv()
load_dotenv('.env.test')


class Production:
    VK_BOT_TOKEN = os.environ.get('VK_BOT_TOKEN')

    TYPE_CACHE = os.environ.get('TYPE_CACHE')

    REDIS_HOST = os.environ.get('REDIS_HOST')
    REDIS_PORT = os.environ.get('REDIS_PORT')

    if TYPE_CACHE is None:
        sys.exit('Не указан TYPE_CACHE, который отвечает за выбор кэша')

    if TYPE_CACHE == 'REDIS':
        if REDIS_HOST is None or REDIS_PORT is None:
            sys.exit(
                'В качестве кэша выбран REDIS, но не переданы REDIS_HOST и REDIS_PORT для него'
            )


class Test:
    TYPE_CACHE = os.environ.get('TEST_TYPE_CACHE')
    REDIS_HOST = os.environ.get('TEST_REDIS_HOST')
    REDIS_PORT = os.environ.get('TEST_REDIS_PORT')

    if TYPE_CACHE is None:
        sys.exit('Не указан TEST_TYPE_CACHE, который отвечает за выбор кэша')

    if TYPE_CACHE == 'REDIS':
        if REDIS_HOST is None or REDIS_PORT is None:
            sys.exit(
                'В качестве кэша выбран REDIS, но не переданы REDIS_HOST и REDIS_PORT для него'
            )
