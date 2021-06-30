from aiogram import Dispatcher, types


async def cmd_start(message: types.Message):
    await message.answer(
        "Этот бот создан для поиска белых медведей на снимках с самолета. "
        "Для работы с ним присылайте изображения.",
        reply_markup=types.ReplyKeyboardRemove()
    )


async def cmd_help(message: types.Message):
    await message.answer("Пришлите нам фото, которое вы хотите проверить на наличие белых медведей",
                         reply_markup=types.ReplyKeyboardRemove())


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start", state="*")
    dp.register_message_handler(cmd_help, commands="help", state="*")
