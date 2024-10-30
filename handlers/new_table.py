from aiogram import Router, F
from aiogram.types import CallbackQuery, ReplyKeyboardRemove, Message
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
from app.state_groups import inCreateTakelist, inCreateTimetable, inCreateEvent, inCreateNote
from app.filters import MyEntityFilter, MyLenFilter
from database.requests.insert import insert_into_takelists, insert_into_timetables, insert_into_events, insert_into_notes

router = Router()

my_data = []
# @router.message(F.text , MyEntityFilter(r'\d\d.\d\d.\d\d \d\d:\d\d'))
# async def just_text(message: Message):
#     await message.answer('just_text')
# @router.message(F.text)
# async def nea(message: Message):
#     await message.answer('Неа')

@router.callback_query(F.data.startswith('create_'))
async def cb_create(callback: CallbackQuery, state: FSMContext):
    result = callback.data.split('_')[1]
    if result == 'takelist':
        await callback.answer('Вы выбрали: Список дел')
        await callback.message.answer('Введите название списка дел', reply_markup=ReplyKeyboardRemove())
        await state.set_state(inCreateTakelist.name)
    if result == 'timetable':
        await callback.answer('Вы выбрали: Расписание')
        await callback.message.answer('Введите название расписания', reply_markup=ReplyKeyboardRemove())
        await state.set_state(inCreateTimetable.name)
    if result == 'event':
        await callback.answer('Вы выбрали: Мероприятие')
        await callback.message.answer('Введите название мероприятия', reply_markup=ReplyKeyboardRemove())
        await state.set_state(inCreateEvent.name)
    if result == 'note':
        await callback.answer('Вы выбрали: Заметка')
        await callback.message.answer('Введите название замеки', reply_markup=ReplyKeyboardRemove())
        await state.set_state(inCreateNote.name)    

@router.message(F.text, inCreateTakelist.name)
async def entered_name_for_takelist(message: Message, state: FSMContext):
    await state.update_data(name = message.text)
    await message.answer('Теперь начинайте вводить пункты списка.\nОдин пункт-одно сообщение.\n'
                         'Чтобы закончить писать список дел нажмите \'Стоп⛔️\'', 
                         reply_markup=kb.stop)
    await state.set_state(inCreateTakelist.body)
    
@router.message(F.text, inCreateTimetable.name)
async def entered_name_for_timetable(message: Message, state: FSMContext):
    await state.update_data(name = message.text)
    await message.answer('Теперь начинайте вводить пункты расписания.\n'
                         'Каждый пункт должен иметь следующий формат:\n'
                         'название пункта - время\n'
                         'Например: Пробежка - 08:00'
                         '\n\nЧтобы закончить писать список дел нажмите \'Стоп⛔️\'', 
                         reply_markup=kb.stop)
    await state.set_state(inCreateTimetable.body)

@router.message(F.text, inCreateEvent.name)
async def entered_name_for_event(message: Message, state: FSMContext):
    await state.update_data(name = message.text)
    await message.answer('Теперь напишите описание к мероприятию')
    await state.set_state(inCreateEvent.body)

@router.message(F.text, inCreateNote.name)
async def entered_name_for_note(message: Message, state: FSMContext):
    await state.update_data(name = message.text)
    await message.answer('Начните писать заметку')
    await state.set_state(inCreateNote.body)

@router.message(F.text, inCreateEvent.body)
async def entered_body_for_event(message: Message, state: FSMContext):
    await state.update_data(body = message.text)
    await message.answer('Укажите дату мероприятию формата \'00.00.00 00:00\'')
    await state.set_state(inCreateEvent.date)

@router.message(F.text, inCreateNote.body)
async def entered_body_for_note(message: Message, state: FSMContext):
    await state.update_data(body = message.text)
    data = await state.get_data()
    await insert_into_notes(message.from_user.id, data['name'], data['body'])
    await message.answer('Заметка успешно создана', reply_markup=kb.main)
    await state.clear()

@router.message(F.text, inCreateEvent.date, MyEntityFilter(r'^(0?[1-9]|[12][0-9]|3[01])\.(0?[1-9]|1[012])\.2\d{3} (0?\d|1\d|2[0-3])\:(0?\d|[1-5]\d)$'))
async def entered_date_for_event(message: Message, state: FSMContext):
    await state.update_data(date = message.text)
    await message.answer('Напишите адрес проведения мероприятия')
    await state.set_state(inCreateEvent.adress)
@router.message(inCreateEvent.date)
async def entered_date_for_event_incorrect(message: Message):
    await message.answer('Данные введены некоректно')

@router.message(F.text, inCreateEvent.adress)
async def entered_adress_for_event(message: Message, state: FSMContext):
    await state.update_data(adress = message.text)
    data = await state.get_data()
    await insert_into_events(message.from_user.id, data['name'], data['body'], data['date'], data['adress'])
    await message.answer('Мероприятие создано', reply_markup=kb.main)
    await state.clear()

@router.message(F.text == 'Стоп⛔️', inCreateTakelist.body)
async def stop_for_takelist(message: Message, state: FSMContext):
    try:
        global my_data
        my_data = []
        state_data = await state.get_data()
        # print(state_data)
        for item in state_data['point']:
            await insert_into_takelists(message.from_user.id, state_data['name'], item)
        await message.answer('Список дел создан', 
                             reply_markup=kb.main)
        await state.clear()
    except KeyError:
        await message.answer('Введите хотя бы 1 пункт списка')
@router.message(F.text == 'Стоп⛔️', inCreateTimetable.body)
async def stop_for_timetable(message: Message, state: FSMContext):
    try:
        global my_data
        my_data = []
        state_data = await state.get_data()
        # print(state_data)
        for item in state_data['point']:
            items = str(item).split(' - ')
            if len(items[1]) <= 5:   
                await insert_into_timetables(message.from_user.id, state_data['name'], items[0], items[1])
            else: await message.answer('Что-то пошло не так')
        await message.answer('Расписание создано', 
                             reply_markup=kb.main)
        await state.clear()
    except KeyError:
        await message.answer('Введите хотя бы 1 пункт расписания')
@router.message(F.text == 'Стоп⛔️')
async def incorrect_stop(message: Message):
    await message.answer('Что-то пошло не так. Попробуйте позже')
@router.message(inCreateTimetable.body, 
                MyEntityFilter(r'(0?\d|1\d|2[0-3])\:(0?\d$|[1-5]\d$)'), 
                MyLenFilter(len=2, separator=' - '))
async def entered_body_for_timetable(message: Message, state: FSMContext):
    my_data.append(str(message.text))
    await state.update_data(point = my_data)
    # await message.answer('Данные введены корректно')
@router.message(F.text, inCreateTakelist.body)
async def entered_body_for_takelist(message: Message, state: FSMContext):
    my_data.append(str(message.text))
    await state.update_data(point = my_data)
    # await message.answer('Данные введены корректно')
@router.message(inCreateTimetable.body)
async def entered_body_for_timetable_incorrect(message: Message):
    await message.answer('Данные введены некоректно')

    


    
