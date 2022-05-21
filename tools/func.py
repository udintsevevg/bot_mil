from main import bot
from random import randint
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton,\
                          ReplyKeyboardMarkup, KeyboardButton

class UserGame:
    def __init__(self, user_id):
        self.user_id = user_id
        self.balance = 0
        self.step = 1
        self.answer = []
        self.fifth = True
        self.help_bot = True
        self.cur_quest = {}
        self.cur_msg = 0
        self.finish = False
        self.user_quest = []
        self.stages = {1:1000,2:5000,3:15000,4:50000,5:75000,6:100000,7:125000,8:150000,9:200000,10:280000}

    def change_bal(self):
        self.balance += self.stages.get(self.step)
    
    def get_price_quest(self):
        return str(self.stages.get(self.step))
        

def get_quests(user_obj: UserGame):
    for i in user_obj.user_quest:
        if not i.get('question') in user_obj.answer:
            user_obj.answer.append(i.get('question'))
            return i


def render_answer(quesi, step):
    kb1 = InlineKeyboardMarkup(row_width=2)
    kb1.add(*[InlineKeyboardButton(i, callback_data = 'quest:'+ str(step) +':' + i) for i in quesi.get('answer')])
    return kb1


def render_fifth(quesi, step):
    questions = ['(. ❛ ᴗ ❛.)','(. ❛ ᴗ ❛.)','(. ❛ ᴗ ❛.)','(. ❛ ᴗ ❛.)']
    tmp_list = [0,1,2,3]
    for i,v in enumerate(quesi.get('answer')):
        if v == quesi.get('rigth_answer'):
            questions[i] = v
            tmp_list.remove(i)
    tmp = randint(0,2)                   
    questions[tmp_list[tmp]] = quesi.get('answer')[tmp]
    kb2 = InlineKeyboardMarkup(row_width=2)
    kb2.add(*[InlineKeyboardButton(i, callback_data = 'quest:'+ str(step) +':' + i) for i in questions])
    return kb2


def render_help_bot(user_obj: UserGame):
    questions = ['(. ❛ ᴗ ❛.)','(. ❛ ᴗ ❛.)','(. ❛ ᴗ ❛.)','(. ❛ ᴗ ❛.)']
    for i,v in enumerate(user_obj.cur_quest.get('answer')):
        if v == user_obj.cur_quest.get('rigth_answer'):
            questions[i] = v
    kb2 = InlineKeyboardMarkup(row_width=2)
    kb2.add(*[InlineKeyboardButton(i, callback_data = 'quest:'+ str(user_obj.step) +':' + i) for i in questions])
    return kb2


def check_answer(user_obj ,questiona,answer):
    for i in user_obj.user_quest:
        if i.get('question') == questiona:
            if i.get('rigth_answer') == answer:
                return True
            else:
                return False


def render_keyboard(user_obj: UserGame):
    btn1 = KeyboardButton('50 на 50' if user_obj.fifth else '(ﾉ ﾟｰﾟ)ﾉ')
    btn2 = KeyboardButton('Помощь бота' if user_obj.help_bot else '＼(ﾟｰﾟ＼)')
    btn3 = KeyboardButton('Выход')
    btn4 = KeyboardButton('Банк: '+ str(user_obj.balance) + ' 💲')
    games = ReplyKeyboardMarkup(resize_keyboard=True).row(btn1, btn2, btn3).row(btn4)
    return games


async def push_message(user_obj: UserGame, chat_id):
        user_obj.step += 1
        answer_cool = 'Вопрос на ' + str(user_obj.get_price_quest())+ ' 💲'
        quest = get_quests(user_obj)
        user_obj.cur_quest = quest 

        await bot.send_message(chat_id=chat_id, text= ''.join('—' for i in range(25)))
        await bot.send_message(chat_id=chat_id, text= answer_cool, reply_markup= render_keyboard(user_obj))

        msg = await bot.send_message(chat_id = chat_id, text= quest.get('question'), \
            reply_markup= render_answer(quest, user_obj.step))
        user_obj.cur_msg = msg.message_id