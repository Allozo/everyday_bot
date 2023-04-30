import abc
import datetime
import logging
import logging.config
import sys
from typing import Callable, Type

from src.config import LOGGER_CONFIG

logging.config.dictConfig(LOGGER_CONFIG)
logger = logging.getLogger(__name__)


class BaseCache(abc.ABC):
    _REGISTRY: dict[str, Type['BaseCache']] = {}

    @abc.abstractmethod
    def get(self, key: str) -> str | None:
        ...

    @abc.abstractmethod
    def set(self, key: str, value: str) -> None:
        ...

    @abc.abstractmethod
    def expire(self, key: str, time: int | datetime.timedelta) -> None:
        ...

    @classmethod
    def register(cls, name: str) -> Callable[[Type['BaseCache']], Type['BaseCache']]:
        def decorator(klass: Type['BaseCache']) -> Type['BaseCache']:
            # breakpoint()
            logger.info(
                "Зарегистрируем Cache '%s' под именем '%s'", klass.__name__, name
            )
            cls._REGISTRY[name] = klass
            return klass

        return decorator

    @classmethod
    def create_cache(cls, type_cache: str, **kwargs: dict[str, str]) -> 'BaseCache':
        klass = cls._REGISTRY.get(type_cache)

        if klass is None:
            logger.exception('Кэш %s не зарегистрирован\n', type_cache)
            sys.exit(f'Кэш {type_cache=} не зарегистрирован')

        return klass(**kwargs)
