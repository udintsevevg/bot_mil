from main import dp, bot
from aiogram.types import Message
from tools.states import User_state
from tools.keyboards import new_game


@dp.message_handler(commands=['menu'])
async def view_menu(message: Message):
    text = 'Выберите пункт меню:'
    await User_state.menu.set()
    return await message.answer(text, reply_markup= new_game)

