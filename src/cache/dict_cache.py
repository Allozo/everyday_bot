import datetime
import logging
import time as time_lib

from src.cache.base_cache import BaseCache

logger = logging.getLogger(__name__)


@BaseCache.register('DICT')
class DictCache(BaseCache):
    def __init__(self, **kwargs: dict[str, str]) -> None:  # pylint: disable=W0613
        logger.info('Создадим {%s}', self.__class__.__name__)
        self._cache: dict[str, str] = {}
        self._time_expire: dict[str, dict[str, int]] = {}

    def _key_expire(self, key: str) -> None:
        now_time = int(time_lib.time())

        if (
            now_time - self._time_expire[key]['save_time']
            < self._time_expire[key]['delta_time']
        ):
            logger.info('Удалим из {%s} key={%s}', self.__class__.__name__, key)
            del self._cache[key]
            del self._time_expire[key]

    def get(self, key: str) -> str | None:
        logger.info('Получим из {%s} key={%s}', self.__class__.__name__, key)
        val = self._cache.get(key)
        return val if val is not None else None

    def set(self, key: str, value: str) -> None:
        logger.info('Сохраним в {%s} key={%s}', self.__class__.__name__, key)
        self._cache[key] = value

    def expire(self, key: str, time: int | datetime.timedelta) -> None:
        # Преобразуем time к int, чтобы удобнее было работать с ним
        if isinstance(time, datetime.timedelta):
            time = int(time.total_seconds())

        logger.info(
            'Временно сохраним в {%s} key={%s} на time={%s} секунд',
            self.__class__.__name__,
            key,
            time,
        )
        self._time_expire[key] = {
            'save_time': int(time_lib.time()),
            'delta_time': time,
        }
