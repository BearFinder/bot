from aiogram import types, Dispatcher
import base64
import requests


async def download_document(message: types.Message):
    filepath = f'bot/files/{message.document.file_name}'
    await message.document.download(filepath)
    api_server = "http://127.0.0.1:5000/api/"
    encoded = base64.b64encode(open(filepath, "rb").read())
    params = {'src': base64.b64encode(encoded)}
    response = requests.get(api_server, params=params)
    if not response:
        await message.answer('Произошла ошибка. Попробуйте снова')
    json_response = response.json()
    await message.answer(f'На изображении найдено медведей: {json_response["count"]}')


async def download_photo(message: types.Message):
    await message.photo[-1].download(f'bot/files/{message.from_user.id}.jpg')


def register_handlers_bear(dp: Dispatcher):
    dp.register_message_handler(download_document, state="*",
                                content_types=[types.ContentType.DOCUMENT])
    dp.register_message_handler(download_photo, state="*", content_types=[types.ContentType.PHOTO])
