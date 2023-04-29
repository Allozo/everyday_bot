import datetime
import logging
import sys

import redis

from src.cache.base_cache import BaseCache

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    filename='logs/app.log',
    filemode='a',
    format='%(name)s - %(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8',
)


@BaseCache.register('REDIS')
class RedisCache(BaseCache):
    def __init__(self, **kwargs: dict[str, str]) -> None:
        """
        Создаёт кэш, который будет связан с Redis.

        Args:
            kwargs (dict): Могут передаваться следующие переменные:
            - host (str): Хост для подключения к Redis. Например,localhost
            - port (int): Порт для подключения к Redis. Например, 6379
        """
        logger.info('Создадим {%s}', self.__class__.__name__)
        self._cache = self._get_redis_cache(
            kwargs['kwargs']['host'], int(kwargs['kwargs']['port'])
        )

    @staticmethod
    def _get_redis_cache(host: str, port: int) -> 'redis.Redis[bytes]':
        r = redis.Redis(host=host, port=int(port), db=0)
        try:
            r.ping()
        except redis.exceptions.ConnectionError:
            text_err = f'Не удалось подключиться к Redis(host={host}, port={port})'
            logger.error(text_err)
            sys.exit(text_err)

        return r

    def get(self, key: str) -> str | None:
        logger.info('Получим из {%s} key={%s}', self.__class__.__name__, key)
        val = self._cache.get(key)
        return val.decode('utf-8') if val is not None else None

    def set(self, key: str, value: str) -> None:
        logger.info('Сохраним в {%s} key={%s}', self.__class__.__name__, key)
        self._cache.set(key, value)

    def expire(self, key: str, time: int | datetime.timedelta) -> None:
        logger.info(
            'Временно сохраним в {%s} key={%s} на time={%s} секунд',
            self.__class__.__name__,
            key,
            time,
        )
        self._cache.expire(key, time)
