from datetime import datetime
import logging
import vk_api
import abc

from src.vk_bot.keyboard import KeyboardBot

from src.parser.weather.weather import ParseWeather

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    filename="logs/app.log",
    filemode="a",
    format="%(name)s - %(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8",
)

class MessageHandler(abc.ABC):
    _REGISTRY = {}

    @abc.abstractmethod
    def send_message(self, user_id: int) -> None:
        ...

    @classmethod
    def register(cls, name: str):
        def decorator(klass: 'MessageHandler') -> 'MessageHandler':
            logger.info(f"Зарегистрируем VkHandler '{klass.__name__}' под именем '{name}'")
            cls._REGISTRY[name] = klass
            return klass

        return decorator

    @classmethod
    def create(cls, message_type: str) -> 'MessageHandler':
        klass = cls._REGISTRY.get(message_type)

        if klass is None:
            klass = cls._REGISTRY.get("error_message")

        return klass()

    @classmethod
    def set_vk_session(cls, vk_session: vk_api.VkApi) -> None:
        cls.vk = vk_session.get_api()



@MessageHandler.register("start")
class StartHandler(MessageHandler):
    def send_message(self, user_id: int):
        message = "Привет!"
        self.vk.messages.send(
            user_id=user_id,
            message=message,
            random_id=hash(str(datetime.now())),
            keyboard=KeyboardBot()(),
        )
        logger.info(f"Пользователь {user_id} начал работу")


@MessageHandler.register("exit")
class ExitHandler(MessageHandler):
    def send_message(self, user_id: int):
        message = "Отключаюсь"
        self.vk.messages.send(
            user_id=user_id,
            message=message,
            random_id=hash(str(datetime.now())),
            keyboard=KeyboardBot()(),
        )
        logger.info(f"Пользователь {user_id} завершил работу")
        exit()


@MessageHandler.register("error_message")
class ErrorHandler(MessageHandler):
    def send_message(self, user_id: int):
        message = "Ввели что-то непонятное"
        self.vk.messages.send(
            user_id=user_id,
            message=message,
            random_id=hash(str(datetime.now())),
            keyboard=KeyboardBot()(),
        )
        logger.info(f"Пользователь {user_id} ввёл неправильное сообщение")


@MessageHandler.register("mailing")
class MailingHandler(MessageHandler):
    def send_message(self, user_id: int):
        message = "Это рассылка"
        self.vk.messages.send(
            user_id=user_id,
            message=message,
            random_id=hash(str(datetime.now())),
            keyboard=KeyboardBot()(),
        )
        logger.info(f"Сделали рассылку")


@MessageHandler.register("update")
class UpdateHandler(MessageHandler):
    def send_message(self, user_id: int):
        message = ParseWeather().get_weather_on_day("Москва")
        self.vk.messages.send(
            user_id=user_id,
            message=message,
            random_id=hash(str(datetime.now())),
            keyboard=KeyboardBot()(),
        )
        logger.info(f"Обновил вывод")