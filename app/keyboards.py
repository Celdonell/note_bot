from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.requests.select import select_takelist_by_id, select_timetable_by_id, select_event_by_id, select_note_by_id, select_takelist_body_by_id_and_name, select_takelist_didornot_by_id_and_name

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Создать➕'), 
                                      KeyboardButton(text='Мои записи📋')]], 
                           resize_keyboard=True)

stop = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Стоп⛔️')]],
                           resize_keyboard=True)

async def create_inline_keyboard(data: list[str]|str, key: str):
    keyboard = InlineKeyboardBuilder()
    for item in data:
        text, callback_data = item.split('-', 1)
        keyboard.add(InlineKeyboardButton(text=text, callback_data=f'{key}_{callback_data}'))
    return keyboard.adjust(2).as_markup()

async def get_takelists_by_id(tg_id):
    already_exist = []
    data = await select_takelist_by_id(tg_id)
    keyboard = InlineKeyboardBuilder()
    for item in data:
        if item.name in already_exist:
            continue
        else:
            keyboard.add(InlineKeyboardButton(text=item.name, callback_data=f'takelistname_{str(item.name)}-{str(item.tg_id)}'))
            already_exist.append(item.name)
    return keyboard.adjust(2).as_markup()

async def get_timetables_by_id(tg_id):
    already_exist = []
    data = await select_timetable_by_id(tg_id)
    keyboard = InlineKeyboardBuilder()
    for item in data:
        if item.name in already_exist:
            continue
        else:
            keyboard.add(InlineKeyboardButton(text=item.name, callback_data=f'timetablename_{str(item.name)}-{str(item.tg_id)}'))
            already_exist.append(item.name)
    return keyboard.adjust(2).as_markup()

async def get_events_by_id(tg_id):
    data = await select_event_by_id(tg_id)
    keyboard = InlineKeyboardBuilder()
    for item in data:
        keyboard.add(InlineKeyboardButton(text=item.name, callback_data=f'eventname_{str(item.name)}-{str(item.tg_id)}'))
    return keyboard.adjust(2).as_markup()

async def get_notes_by_id(tg_id):
    data = await select_note_by_id(tg_id)
    keyboard = InlineKeyboardBuilder()
    for item in data:
        keyboard.add(InlineKeyboardButton(text=item.name, callback_data=f'notename_{str(item.name)}-{str(item.tg_id)}'))
    return keyboard.adjust(2).as_markup()

async def get_takelists_body_by_name(name, tg_id):
    body_data = await select_takelist_body_by_id_and_name(tg_id, name)
    keyboard = InlineKeyboardBuilder()
    for item in body_data:
        if await select_takelist_didornot_by_id_and_name(tg_id, name, item) == True:
            keyboard.add(InlineKeyboardButton(text=f'✅{item}', callback_data=f'edittakelist_{str(item)}-{str(tg_id)}-{str(name)}'))
        else:
            keyboard.add(InlineKeyboardButton(text=f'❌{item}', callback_data=f'edittakelist_{str(item)}-{str(tg_id)}-{str(name)}'))
    keyboard.add(InlineKeyboardButton(text='Назад', callback_data=f'edittakelist_back-{name}'))
    return keyboard.adjust(1).as_markup()




                          

