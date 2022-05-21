from main import dp,bot, question
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from tools.states import User_state
from tools.func import *
from random import randint
    
users_p = {}


@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='Выход', ignore_case=True), state='*')
async def cancel_handler(message: Message, state: FSMContext):
    await state.finish()
    await message.answer(text='Ну ок, как бы', reply_markup= ReplyKeyboardRemove())


@dp.message_handler(state = User_state.menu, content_types= ['text'])
async def get_menu(message: Message, state: FSMContext):
    if message.text == 'Играть':
        new_user = UserGame(message.from_user.id)
        tmp_rand = randint(0, 178)
        new_user.user_quest = question[tmp_rand: tmp_rand + 10]
        users_p[new_user.user_id] = new_user
        await User_state.game.set()
        return await push_message(users_p.get(message.from_user.id), message.chat.id)
    else:
        return await message.answer('Не флуди во время игры 🤐')


@dp.message_handler(state = User_state.game, content_types= ['text'])
async def get_menus(message: Message, state: FSMContext):
    user_obj: UserGame = users_p.get(message.from_user.id)
    if user_obj.finish:
        return await state.finish()
    if message.text == '50 на 50' and user_obj.fifth:
        user_obj.fifth = False
        await bot.edit_message_reply_markup(user_obj.user_id, user_obj.cur_msg, reply_markup= render_fifth(user_obj.cur_quest, user_obj.step))
    elif message.text == 'Помощь бота' and user_obj.help_bot:
        user_obj.help_bot = False
        await bot.edit_message_reply_markup(user_obj.user_id, user_obj.cur_msg, reply_markup= render_help_bot(user_obj))
    else:
        return await message.answer('Не флуди во время игры 🤐')


@dp.callback_query_handler(Text(startswith="quest:"), state='*')
async def blabla(call: CallbackQuery, state: FSMContext):
    user_obj: UserGame = users_p.get(call.from_user.id)

    if user_obj.finish:
        await call.answer('Ты уже проиграл, хренали тыкаешь? 🤨')
        return await state.finish()

    if call.data.split(':')[1] != str(user_obj.step):
        return await call.answer('Промазал, не надо так 😤')
    answer = call.data.split(':')[2]

    if check_answer(user_obj,call.message.text, answer) and user_obj.step == 10:
        user_obj.change_bal()
        bot.send_message(chat_id=call.message.chat.id, text= ''.join('—' for i in range(25)))
        await bot.send_message(chat_id=call.message.chat.id, text='Поздравляем!\nТы выиграл 1 000 000 💲 🎉', reply_markup= ReplyKeyboardRemove())
        user_obj.finish = True
        return await call.answer()
    elif check_answer(user_obj, call.message.text, answer):
        user_obj.change_bal()
        await push_message(user_obj, call.message.chat.id)
        return await call.answer()
    else:
        user_obj.finish = True
        await bot.send_message(chat_id=call.message.chat.id, text= ''.join('—' for i in range(25)))
        await bot.send_message(chat_id=call.message.chat.id, text='Упс, проиграли 😥')
        await bot.send_message(chat_id=call.message.chat.id, text='Ваш выигрыш: ' + str(user_obj.balance), reply_markup= ReplyKeyboardRemove())
        return await call.answer()
