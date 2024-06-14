from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

main_menu_inline = InlineKeyboardMarkup(row_width=2)\
    .add(
        InlineKeyboardButton(text="1", callback_data=""),
        InlineKeyboardButton(text="2", callback_data=""),
        )


async def cancel_inline_menu(callback_data):
    return InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text="↪️Назад", callback_data=callback_data))



