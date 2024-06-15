from aiogram.types import ReplyKeyboardMarkup

main_menu = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)\
    .add("👥Задать вопрос")
    
cancel_menu = ReplyKeyboardMarkup(resize_keyboard=True).add('↪️Назад')