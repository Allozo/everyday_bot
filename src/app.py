import logging

from src.config import LOGGER_CONFIG, ModelVkBot
from src.vk_bot.vk_bot import VkBot

logging.config.dictConfig(LOGGER_CONFIG)
logger = logging.getLogger(__name__)


def main() -> None:
    logger.info('Запустим бота для ВК')
    print('Запустим бота для ВК')
    vk_bot_data = ModelVkBot()  # type: ignore
    bot = VkBot(vk_bot_data.VK_BOT_TOKEN)
    logger.info('Бот для ВК готов к работе')
    print('Бот для ВК готов к работе')
    bot.start()


if __name__ == '__main__':
    main()
