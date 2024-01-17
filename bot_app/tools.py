from aiogram.types import PhotoSize, Message, Video, TelegramObject
from typing import Optional, Union

async def photo_size_sorter(photo_sizes: list[PhotoSize]):
    width_sizes = []
    for photo in photo_sizes:
        width_sizes.append(photo.width)
    max_size = max(width_sizes)
    index = width_sizes.index(max_size)
    return photo_sizes[index].file_id

async def get_attachment_id(message: Message, required_type: Union[PhotoSize, Video] = None) -> Optional[str]:

    if required_type is None:
        if message.photo:
            media_attachment = await photo_size_sorter(message.photo)
            return media_attachment
        elif message.video:
            media_attachment = message.video
            return media_attachment.file_id
        else:
            return None
    else:
        if message.photo and isinstance(message.photo[0], required_type):
            media_attachment = await photo_size_sorter(message.photo)
            return media_attachment
        elif message.video and isinstance(message.video, required_type):
            media_attachment = message.video
            return media_attachment.file_id
        else:
            return None