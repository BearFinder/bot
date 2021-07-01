from PIL import Image
from aiogram import types, Dispatcher
import requests


SERVER_ADDR = ""


async def download_document(message: types.InputFile):
    filepath = f'input/{message.document.file_name}'
    savepath = f'output/{message.document.file_name}'
    await message.document.download(filepath)
    with open(filepath, "rb") as f:
        encoded = f.read()
    encoded = str(encoded)
    json = {"upload_file": open(filepath, "rb")}
    response = requests.post(SERVER_ADDR, files=json)
    print(response)
    if not response:
        await message.answer('Произошла ошибка. Попробуйте снова')
        return
    elif response.status_code == 200:
        with open(savepath, 'wb') as f:
            f.write(response.content)
        await message.answer_document(open(savepath, "rb"))
    else:
        await message.answer("Произошла ошибка")


async def download_photo(message: types.Message):
    filepath = f'input/{message.from_user.id}.jpg'
    savepath = f'output/{message.from_user.id}.jpg'
    await message.photo[-1].download(filepath)
    with open(filepath, "rb") as f:
        encoded = f.read()
    encoded = str(encoded)
    json = {"upload_file": open(filepath, "rb")}
    response = requests.post(SERVER_ADDR, files=json)
    print(response)
    if not response:
        await message.answer('Произошла ошибка. Попробуйте снова')
        return
    elif response.status_code == 200:
        with open(savepath, 'wb') as f:
            f.write(response.content)
        await message.answer_document(open(savepath, "rb"))
    else:
        await message.answer("Произошла ошибка")

def register_handlers_bear(dp: Dispatcher, server_address: str):
    global SERVER_ADDR
    dp.register_message_handler(download_document, state="*",
                                content_types=[types.ContentType.DOCUMENT])
    dp.register_message_handler(download_photo, state="*", content_types=[types.ContentType.PHOTO])
    SERVER_ADDR = server_address
