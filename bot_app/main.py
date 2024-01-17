from aiogram import Bot, Dispatcher
from aiogram.types import Message
from keyboards import builder
from user import *
import asyncio
from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

router1 = Router()
dp.include_router(router1)

@dp.message(commands=['start'])
async def start(message: Message):
    user = User(message.from_user.id)
    await message.answer("Some text here", reply_markup=builder.as_markup())
    # await menu(message)


@dp.callback_query_handler(text='menu')
async def menu(message):
    try:
        if hasattr(message, 'message'):
            _message_id = message.message.message_id
        else:
            _message_id = message.message_id

        await bot.delete_message(message.from_user.id, _message_id)
    except MessageToDeleteNotFound or MessageIdentifierNotSpecified or AttributeError:
        pass

    user = User(message.from_user.id)

    await bot.setext = messageage(user.id, menu_text, reply_markup=menu_markup)


@dp.message_handler()
async def get_text(message: types.message):
    await bot.delete_message(message.chat.id, message.message_id)


async def main():
    await bot.delete_webhook()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())