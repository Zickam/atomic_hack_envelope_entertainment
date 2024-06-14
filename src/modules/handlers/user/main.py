import datetime
from aiogram.types import Message
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from modules.misc.states import UserAuthState, UserInputState
from aiogram.types import Message, InlineKeyboardMarkup, CallbackQuery
from modules.misc.throttling import rate_limit
from modules.keyboards import *


async def send_hello_message(message: Message) -> None:
    await message.answer(f'<b>Добро пожаловать,</b> {message.from_user.first_name}!')
    
@rate_limit(2)
async def start_handler(message: Message) -> None:
    await send_hello_message(message)
    

def register_user(dp: Dispatcher) -> None:
    dp.register_message_handler(start_handler, commands=['start'])
    
    