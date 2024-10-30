from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message

import app.keyboards as kb

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Привет это твой бот-блокнот🗓. Здесь ты можешь создать расписание, список дел, назначить мероприятие или просто сделать заметку\n\nНажмите кнопку ниже, чтобы создать', reply_markup=kb.main)
    
@router.message(F.text == 'Создать➕')
async def create_new_timetable(message: Message):
    await message.answer('Выберите, что будем создавать', 
                         reply_markup=await kb.create_inline_keyboard(['Расписание-timetable', 'Список дел-takelist', 'Мероприятие-event', 'Заметку-note'], 'create'))
    
@router.message(F.text == 'Мои записи📋')
async def show_my_timetables(message: Message):
    await message.answer('Что вы хотите увидеть?',
                         reply_markup=await kb.create_inline_keyboard(['Расписания-timetable', 'Списки дел-takelist', 'Мероприятия-event', 'Заметки-note'], 'saved'))
    
# @router.message(F.text == 'Настройки⚙️')
# async def settings(message: Message):
#     await message.answer('Функция в разработке')
    
