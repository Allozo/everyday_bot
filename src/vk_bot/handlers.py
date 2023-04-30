import abc
import logging
import sys
from datetime import datetime
from typing import Callable, Type

import vk_api

from src.cache.base_cache import BaseCache
from src.config import ModelProdCache
from src.parser.weather.weather import ParseWeather
from src.vk_bot.keyboard import KeyboardBot

logger = logging.getLogger(__name__)

cache_data = ModelProdCache()  # type: ignore
cache = BaseCache.create_cache(
    type_cache=cache_data.CACHE_TYPE,
    kwargs={'host': cache_data.CACHE_HOST, 'port': cache_data.CACHE_PORT},  # type: ignore
)

parse_weather = ParseWeather(cache=cache)


class MessageHandler(abc.ABC):
    _REGISTRY: dict[str, Type['MessageHandler']] = {}
    vk: vk_api.VkApi = None

    @abc.abstractmethod
    def send_message(self, user_id: int) -> None:
        ...

    @classmethod
    def register(
        cls, name: str
    ) -> Callable[[Type['MessageHandler']], Type['MessageHandler']]:
        def decorator(klass: Type['MessageHandler']) -> Type['MessageHandler']:
            logger.info(
                "Зарегистрируем VkHandler '%s' под именем '%s'", klass.__name__, name
            )
            cls._REGISTRY[name] = klass
            return klass

        return decorator

    @classmethod
    def create(cls, message_type: str) -> 'MessageHandler':
        klass = cls._REGISTRY.get(message_type)

        if klass is None:
            klass = cls._REGISTRY['error_message']

        return klass()

    @classmethod
    def set_vk_session(cls, vk_session: vk_api.VkApi) -> None:
        cls.vk = vk_session.get_api()


@MessageHandler.register('start')
class StartHandler(MessageHandler):
    def send_message(self, user_id: int) -> None:
        message = 'Привет!'
        self.vk.messages.send(
            user_id=user_id,
            message=message,
            random_id=hash(str(datetime.now())),
            keyboard=KeyboardBot()(),
        )
        logger.info('Пользователь %d начал работу', user_id)


@MessageHandler.register('exit')
class ExitHandler(MessageHandler):
    def send_message(self, user_id: int) -> None:
        message = 'Отключаюсь'
        self.vk.messages.send(
            user_id=user_id,
            message=message,
            random_id=hash(str(datetime.now())),
            keyboard=KeyboardBot()(),
        )
        logger.info('Пользователь %d завершил работу', user_id)
        sys.exit()


@MessageHandler.register('error_message')
class ErrorHandler(MessageHandler):
    def send_message(self, user_id: int) -> None:
        message = 'Ввели что-то непонятное'
        self.vk.messages.send(
            user_id=user_id,
            message=message,
            random_id=hash(str(datetime.now())),
            keyboard=KeyboardBot()(),
        )
        logger.info('Пользователь %d ввёл неправильное сообщение', user_id)


@MessageHandler.register('mailing')
class MailingHandler(MessageHandler):
    def send_message(self, user_id: int) -> None:
        message = 'Это рассылка'
        self.vk.messages.send(
            user_id=user_id,
            message=message,
            random_id=hash(str(datetime.now())),
            keyboard=KeyboardBot()(),
        )
        logger.info('Сделали рассылку')


@MessageHandler.register('update')
class UpdateHandler(MessageHandler):
    def send_message(self, user_id: int) -> None:
        message = str(parse_weather.get_weather_on_day('Москва'))
        self.vk.messages.send(
            user_id=user_id,
            message=message,
            random_id=hash(str(datetime.now())),
            keyboard=KeyboardBot()(),
        )
        logger.info('Обновил вывод')
