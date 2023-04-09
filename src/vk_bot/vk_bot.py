import logging
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.exceptions import ApiError

from config import VK_BOT_TOKEN
from src.vk_bot.handlers import MessageHandler


logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    filename="logs/app.log",
    filemode="a",
    format="%(name)s - %(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8",
)


class VkBot:
    def __init__(self, _token: str):
        print("Запустили бота")
        logger.info("Запустили бота")

        if _token is None:
            print("Не передан токен группы.")
            logger.info("Не передан токен группы.")
            exit()

        # Авторизуемся как сообщество
        print("Подключаемся к сообществу")
        logger.info("Подключаемся к сообществу")
        try:
            self.vk_session = vk_api.VkApi(token=_token)
            self.longpoll = VkLongPoll(self.vk_session)
        except ApiError as e:
            print(f"Не удалось подключиться к указанной группе. Код ошибки:\n{e}")
            logger.exception("Не удалось подключиться к указанной группе. Код ошибки:")
            logger.exception(e)
            exit(3)

        # Подключим бота к сессии
        MessageHandler.set_vk_session(self.vk_session)

        print("Бот работает")
        logger.info("Бот работает")

    def _get_new_message(self, event: VkLongPoll.DEFAULT_EVENT_CLASS) -> None:
        try:
            logger.info(
                f"Пользователь {event.user_id} прислал сообщение: '{event.text}'"
            )

            MessageHandler.create(event.text).send_message(event.user_id)
        except Exception as e:
            logger.exception(e)
            logger.exception(
                f"""{event.user_id} --- "{event.text}" -- Произошла ошибка:\n  {e}"""
            )

    def main(self):
        # Основной цикл
        for event in self.longpoll.listen():
            # Если пришло новое сообщение
            if (
                event.type == VkEventType.MESSAGE_NEW
                and event.to_me
                and event.from_user
            ):
                self._get_new_message(event)


if __name__ == "__main__":
    bot = VkBot(VK_BOT_TOKEN)
    bot.main()
