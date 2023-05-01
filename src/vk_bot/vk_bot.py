import logging
import sys

import vk_api
from vk_api.exceptions import ApiError
from vk_api.longpoll import VkEventType, VkLongPoll

from src.config import LOGGER_CONFIG
from src.vk_bot.handlers import MessageHandler

logging.config.dictConfig(LOGGER_CONFIG)
logger = logging.getLogger(__name__)


class VkBot:
    def __init__(self, _token: str):
        # Авторизуемся как сообщество
        try:
            self.vk_session = vk_api.VkApi(token=_token)
            self.longpoll = VkLongPoll(self.vk_session)
        except ApiError as e:
            logger.exception(
                'Не удалось подключиться к указанной группе. Код ошибки: \n%s\n', e
            )
            sys.exit(f'Не удалось подключиться к указанной группе. Код ошибки:\n{e}\n')

        # Подключим бота к сессии
        MessageHandler.set_vk_session(self.vk_session)

    def _get_new_message(self, event: VkLongPoll.DEFAULT_EVENT_CLASS) -> None:
        logger.info(
            "Пользователь %d прислал сообщение: '%s'", event.user_id, event.text
        )
        MessageHandler.create(event.text).send_message(event.user_id)

    def start(self) -> None:
        # Основной цикл
        for event in self.longpoll.listen():
            # Если пришло новое сообщение
            if (
                event.type == VkEventType.MESSAGE_NEW
                and event.to_me
                and event.from_user
            ):
                self._get_new_message(event)
