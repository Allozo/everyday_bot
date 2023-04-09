from vk_api.keyboard import VkKeyboard, VkKeyboardColor


class KeyboardBot:
    def __call__(self):
        keyboard = VkKeyboard(one_time=True)

        keyboard.add_button("update", color=VkKeyboardColor.POSITIVE)
        keyboard.add_button("start", color=VkKeyboardColor.POSITIVE)

        keyboard.add_line()  # Переход на вторую строку

        keyboard.add_button("exit", color=VkKeyboardColor.SECONDARY)

        return keyboard.get_keyboard()
