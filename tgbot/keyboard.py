from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types import InlineKeyboardButton, KeyboardButton
def get_menu_keyboard(chat_id):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(
        text="Предложить новость", callback_data=f"sug_{chat_id}")
    )
    return builder


def yes_or_no():
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="Да"), KeyboardButton(text="Нет"))
    return builder