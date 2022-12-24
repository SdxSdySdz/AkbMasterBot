from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hcode

from PyPDF2 import PdfReader
from io import BytesIO



async def bot_echo(message: types.Message):
    await message.answer(message.text)


async def bot_echo_all(message: types.Message, state: FSMContext):
    save_to_io = BytesIO()
    await message.document.download(destination=save_to_io)

    reader = PdfReader(save_to_io)
    number_of_pages = len(reader.pages)
    page = reader.pages[0]
    text = page.extract_text()

    lines = text.split('\n')
    for i in range(len(lines)):
        if lines[i].startswith('00-'):
            await message.answer(lines[i])
    # state_name = await state.get_state()
    # print(message.document.file_id)
    #
    # text = [
    #     f'Эхо в состоянии {hcode(state_name)}',
    #     'Содержание сообщения:',
    #     hcode(message.text)
    # ]
    # await message.answer('\n'.join(text))


def register_echo(dp: Dispatcher):
    dp.register_message_handler(bot_echo)
    dp.register_message_handler(bot_echo_all, state="*", content_types=types.ContentTypes.ANY)
