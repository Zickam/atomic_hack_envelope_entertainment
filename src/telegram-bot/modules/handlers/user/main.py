
from aiogram.types import Message
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from modules.misc.states import UserInputState
from aiogram.types import Message
from modules.misc.throttling import rate_limit
from modules.keyboards import *
from ...services.mistral_chain import get_response


async def send_hello_message(message: Message) -> None:
    await message.answer(f'<b>Добро пожаловать,</b> {message.from_user.first_name}!', reply_markup=main_menu)
    
@rate_limit(2)
async def start_handler(message: Message) -> None:
    await send_hello_message(message)

async def ask_chat_ai(message: Message) -> None:
    match message.text:
        case '👥Задать вопрос':
            await message.answer('Чем могу помочь?', reply_markup=cancel_menu)
            await UserInputState.get_question.set()
            
            
async def get_question_state(message: Message, state: FSMContext) -> None:
    if message.text == '↪️Назад':
        await message.answer('Диалог завершен!')
        return await state.finish()
    print(message.text)
    await message.answer(await get_response(message.text))

def register_user(dp: Dispatcher) -> None:
    dp.register_message_handler(start_handler, commands=['start'])
    dp.register_message_handler(get_question_state, content_types=['text'], state=UserInputState.get_question)
    dp.register_message_handler(ask_chat_ai, content_types=['text'])
    
    
    