from aiogram.types import InlineKeyboardMarkup, KeyboardButton, KeyboardButtonRequestChat, TelegramObject
from aiogram.utils.keyboard import InlineKeyboardBuilder, KeyboardBuilder
import uuid

# Кастомные билдеры использовать только при малом количестве клавиатур.
# При большом количестве писать клавиатуры отдельно, чтобы не запутывать код.
class KbInleneBuilderWrapper(InlineKeyboardBuilder):
    def __init__(self, keyboards_arr: list, num_lines: int=None):
        super().__init__()

        for kb in keyboards_arr:
                self.button(text=kb['text'], callback_data=kb['callback_data'])
        num_buttons = len(keyboards_arr)
        self.adjust(num_buttons, num_lines if num_lines else num_buttons, num_buttons)


class KbBuilderWrapper(KeyboardBuilder):
    def __init__(self, keyboards_arr: list, num_lines: int = None):
        super().__init__(button_type=KeyboardButton)
        for kb in keyboards_arr:
            if 'kb_type' in kb:
                builder = KeyboardBuilder(button_type=KeyboardButton)
                kb_class = self._get_keyboard_class(kb['kb_type'])
                req_id = int(str(uuid.uuid1(clock_seq=6).int)[:6])
                if 'chat_is_channel' in kb:
                    obj = kb_class(request_id = req_id, chat_is_channel = True)
                else:
                    obj = kb_class(request_id = req_id, chat_is_channel=False)
                builder.button(text=kb['text'], request_chat=obj, resize_keyboard=True)
                self.attach(builder)
            else:
                self.button(text=kb['text'])
        num_buttons = len(keyboards_arr)
        self.adjust(num_buttons, num_lines if num_lines else num_buttons, num_buttons)

    def _get_keyboard_class(self, keyboard_type) -> TelegramObject:
        keyboard_types = {'KeyboardButtonRequestChat': KeyboardButtonRequestChat}

        return keyboard_types[keyboard_type]



