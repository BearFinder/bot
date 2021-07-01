from PIL import Image
import base64
from aiogram import types, Dispatcher
import requests
import io


SERVER_ADDR = ""
BOT = None


async def download_document(message: types.InputFile):
    filepath = f'bot/files/{message.document.file_name}'
    await message.document.download(filepath)
    image = Image.open(filepath)
    with open(filepath, "rb") as f:
        encoded = f.read()
    encoded = str(encoded)
    json = {'src': encoded, #base64.b64encode(encoded), 
            'width': image.width, 'height': image.height}
    print("json created") 
    response = requests.post(SERVER_ADDR, json=json)
    print("request finish")
    if not response:
        await message.answer('Произошла ошибка. Попробуйте снова')
        return
    try:
        json_response = response.json()
        save_image = Image.frombytes('RGB', (json_response["width"], json_response["height"]), bytes(json_response["src"], encoding="utf-8"), 'raw')
        save_image.save(filepath)
    except KeyError:
        await message.answer("Произошла ошибка(")
        return 
    await message.answer(filepath)


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
