# main file handles admin-panel as default
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, PhotoSize, Video
from aiogram.filters import Command
from bot_app.Keyboards.private_menu_keyboards import KbInleneBuilderWrapper, KbBuilderWrapper
from Routers import channel_router, chat_router
from aiogram.exceptions import TelegramForbiddenError
from filters import ChatTypeFilter
import asyncio
from config import BOT_TOKEN
from aiogram.fsm.context import FSMContext
from aiogram.fsm.strategy import FSMStrategy
from FSM.PrivateChatForm import MenuForm
import tools



bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(FSMStrategy = FSMStrategy.USER_IN_TOPIC)

dp.include_router(chat_router)
dp.include_router(channel_router)

@dp.message(ChatTypeFilter(chat_type="private"), Command("start"))
async def start(message: Message, state: FSMContext) -> None:
    markup = KbInleneBuilderWrapper([
        {'text':'Отправить картинку', 'callback_data': 'photo'},
                               {'text':'Отправить видео', 'callback_data': 'video'}
    ])
    await message.answer(f"Выберите опцию", reply_markup=markup.as_markup())
    await state.set_state(MenuForm.action_type_choosen)
    await state.update_data(chat_id = message.from_user.id)


@dp.callback_query(lambda call: call.data=="photo" or call.data=="video")
async def choose_text(callback: CallbackQuery, state: FSMContext):
    chat_id = (await state.get_data())["chat_id"] #callback.from_user.id возвращает id бота, поэтому прокинул id чата через стейт
    await state.update_data(action_type = callback.data)

    if callback.data == "photo":
        await callback.message.answer(f"Введите текст к картинке")
    else:
        await callback.message.answer("Введите текст к видео")
    await bot.delete_message(chat_id, callback.message.message_id)
    await state.set_state(MenuForm.action_type_choosen)

@dp.message(MenuForm.action_type_choosen)
async def choose_media(message: Message, state: FSMContext):
    content_map = {"video": "видео", "photo": "картинку"}
    button_choice = (await state.get_data())['action_type']

    content_name = content_map[button_choice]
    await message.answer(f"Загрузите {content_name}")
    await state.set_state(MenuForm.media_data_downloaded)

    await state.update_data(message_text=message.text)

@dp.message(MenuForm.media_data_downloaded)
async def choose_chat_or_channel(message: Message, state: FSMContext):
    action_type = (await state.get_data())['action_type']
    animation_types = {
        "photo": PhotoSize,
        "video": Video
    }
    media_type=animation_types[action_type]

    # Проверка на тот случай, если не было возврата из следующего стейта.
    # Поскольку стейты не имеют класс Enum, у них нет методов next()/previos()
    if 'media_id' not in (await state.get_data()):

        media_id = await tools.get_attachment_id(message=message, required_type=media_type)
        if media_id:
            await state.update_data(media_id=media_id)
        else:
            await state.set_state(MenuForm.action_type_choosen)
            await message.answer("Медиафал не был добавлен. Пожалуйста, повторите операцию заново")
            await choose_media(message, state)
            return



    if media_type is Video:
        markup = KbBuilderWrapper([{'text':'Выберите канал', 'kb_type': 'KeyboardButtonRequestChat', 'chat_is_channel': True}])
        dialog_type = "канал"
    else:
        markup = KbBuilderWrapper(
            [{'text': 'Выберите чат', 'kb_type': 'KeyboardButtonRequestChat'}])
        dialog_type = "чат"
    await message.answer(f"Выберите {dialog_type}", reply_markup=markup.as_markup())
    await state.set_state(MenuForm.text_received)


@dp.message(MenuForm.text_received)
async def handle_shared(message: Message, state: FSMContext):

    if message.chat_shared:
        chat_id = message.chat_shared.chat_id
    else:
        await state.set_state(MenuForm.media_data_downloaded)
        await message.answer("Чат или канал не был выбран. Пожалуйста, повторите операцию заново")
        await choose_chat_or_channel(message, state)
        return

    action_type = (await state.get_data())['action_type']
    msg_text = (await state.get_data())['message_text']
    media_id = (await state.get_data())['media_id']
    try:
        if action_type == "photo":
            await bot.send_photo(caption=msg_text, chat_id=chat_id, photo=media_id)
        else:
            await bot.send_video(caption=msg_text, chat_id=chat_id, video=media_id)
    except Exception as e:
        if isinstance(e, TelegramForbiddenError):
            await message.answer("Бот не является участником чата или канала, выберите другой канал или чат")
            await state.set_state(MenuForm.media_data_downloaded)
            await choose_chat_or_channel(message, state)
            return
        else:
            await message.answer(f"Непредвиденная ошибка {e}")
    await state.clear()

async def main():
    await bot.delete_webhook()
    await dp.start_polling(bot)


if __name__ == "__main__":
    print("Бот запущен")
    asyncio.run(main())