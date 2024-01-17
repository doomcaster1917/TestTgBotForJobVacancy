from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


builder = InlineKeyboardBuilder()

picture = builder.button(text='Отправить картинку', callback_data='menu')
movie = builder.button(text='Отправить видео', callback_data='menu')
builder.adjust(2, 2)

