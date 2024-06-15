from aiogram.dispatcher.filters.state import State, StatesGroup

class UserInputState(StatesGroup):
    get_question = State()
    
