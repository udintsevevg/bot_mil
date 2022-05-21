from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

play_game = KeyboardButton('Играть')
cancel_game = KeyboardButton('Выход')
new_game = ReplyKeyboardMarkup(resize_keyboard=True).row(play_game, cancel_game)

