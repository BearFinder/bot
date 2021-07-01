from PIL import Image
from aiogram import types, Dispatcher
import requests
import io


SERVER_ADDR = ""
BOT = None


async def download_document(message: types.InputFile):
    filepath = f'input/{message.document.file_name}'
    savepath = f'output/{message.document.file_name}'
    await message.document.download(filepath)
    image = Image.open(filepath)
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
        await message.answer_document(savepath)
    await message.answer("Произошла ошибка")


async def download_photo(message: types.Message):
    file_name = f'bot/files/{message.from_user.id}.jpg'
    await message.photo[-1].download(file_name)
    img = Image.open(file_name)
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format=img.format)
    img_byte_arr = img_byte_arr.getvalue()
    data = {
        "src": f"{str(img_byte_arr)}",
        "width": img.width,
        "height": img.height
    }
    response = requests.post(SERVER_ADDR, params=data)
    print(str(response.content, 'utf-8'))


def register_handlers_bear(dp: Dispatcher, server_address: str, bot):
    global SERVER_ADDR, BOT
    BOT = bot
    dp.register_message_handler(download_document, state="*",
                                content_types=[types.ContentType.DOCUMENT])
    dp.register_message_handler(download_photo, state="*", content_types=[types.ContentType.PHOTO])
    SERVER_ADDR = server_address
