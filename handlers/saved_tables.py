from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest

import app.keyboards as kb
from database.requests.select import select_takelist_by_id_and_name, select_timetable_by_id_and_name, select_event_by_id_and_name, select_note_by_id_and_name, select_takelist_by_id, select_timetable_by_id, select_event_by_id, select_note_by_id
from database.requests.delete import delete_takelist_by_id_and_name, delete_timetable_by_id_and_name, delete_event_by_id_and_name, delete_note_by_id_and_name
from database.requests.update import update_didornot

router = Router()

@router.callback_query(F.data.startswith('saved_'))
async def cb_saved(callback: CallbackQuery):
    result = callback.data.split('_')[1]
    if result == 'takelist':
        await callback.answer('Вы выбрали: Списки дел')
        data = await select_takelist_by_id(callback.from_user.id)
        string = ''
        for item in data:
            string += item.name
        if string == '':
            await callback.message.answer('У вас нет списков дел. Нажмите \'Создать➕\' чтобы создать новый список')
        else:
            await callback.message.answer('Выберите список дел', reply_markup=await kb.get_takelists_by_id(callback.from_user.id))
    if result == 'timetable':
        await callback.answer('Вы выбрали: Расписания')
        data = await select_timetable_by_id(callback.from_user.id)
        string = ''
        for item in data:
            string += item.name
        if string == '':
            await callback.message.answer('У вас нет расписаний. Нажмите \'Создать➕\' чтобы создать новое расписание')
        else:
            await callback.message.answer('Выберите расписание', reply_markup=await kb.get_timetables_by_id(callback.from_user.id))
    if result == 'event':
        await callback.answer('Вы выбрали: Мероприятия')
        data = await select_event_by_id(callback.from_user.id)
        string = ''
        for item in data:
            string += item.name
        if string == '':
            await callback.message.answer('У вас нет мероприятий. Нажмите \'Создать➕\' чтобы создать новое мероприятие')
        else:
            await callback.message.answer('Выберите мероприятие', reply_markup=await kb.get_events_by_id(callback.from_user.id))
    if result == 'note':
        await callback.answer('Вы выбрали: Заметки')
        data = await select_note_by_id(callback.from_user.id)
        string = ''
        for item in data:
            string += item.name
        if string == '':
            await callback.message.answer('У вас нет заметок. Нажмите \'Создать➕\' чтобы создать новую заметку')
        else:
            await callback.message.answer('Выберите заметку', reply_markup=await kb.get_notes_by_id(callback.from_user.id))

@router.callback_query(F.data.startswith('takelistname_'))
async def cb_takelistname(callback: CallbackQuery):
    await callback.answer('')
    cb = callback.data.split('_')[1]
    result = cb.split('-')
    data = await select_takelist_by_id_and_name(int(result[1]),str(result[0]))
    string = ''
    for item in data:
        if item.didornot == False:
            string += f'❌{item.body}\n'
        else: string += f'✅{item.body}\n'
    
    try:
        await callback.message.edit_text(string, reply_markup=await kb.create_inline_keyboard(['Назад-back', f'Отметить сделанное-edit-{str(result[0])}', f'Удалить-delete-{str(result[0])}'], 'takelistshown'))
    except TelegramBadRequest:
        await callback.message.answer('Bad request')

@router.callback_query(F.data.startswith('timetablename_'))
async def cb_timetablename(callback: CallbackQuery):
    await callback.answer('')
    cb = callback.data.split('_')[1]
    result = cb.split('-')
    data = await select_timetable_by_id_and_name(int(result[1]), str(result[0]))
    string = ''
    for item in data:
        string += f'<b>{item.body} {item.date}</b>\n'
    try:
        await callback.message.edit_text(string, reply_markup=await kb.create_inline_keyboard(['Назад-back', f'Удалить-delete-{str(result[0])}'], 'timetableshown'))
    except TelegramBadRequest:
        await callback.message.answer('Bad request')

@router.callback_query(F.data.startswith('eventname_'))
async def cb_eventname(callback: CallbackQuery):
    await callback.answer('')
    cb = callback.data.split('_')[1]
    result = cb.split('-')
    data = await select_event_by_id_and_name(int(result[1]), str(result[0]))
    await callback.message.edit_text(f'<b>{data.name} {data.date}</b>\n{data.body}\nадрес: {data.adress}', reply_markup=await kb.create_inline_keyboard(['Назад-back', f'Удалить-delete-{result[0]}'], 'eventshown'))

@router.callback_query(F.data.startswith('notename_'))
async def cb_notename(callback: CallbackQuery):
    await callback.answer('')
    cb = callback.data.split('_')[1]
    result = cb.split('-')
    data = await select_note_by_id_and_name(int(result[1]), str(result[0]))
    await callback.message.edit_text(f'<b>{data.name}</b>\n{data.body}', reply_markup=await kb.create_inline_keyboard(['Назад-back', f'Удалить-delete-{result[0]}'], 'noteshown'))

@router.callback_query(F.data.startswith('edittakelist_'))
async def cb_edittakelist(callback: CallbackQuery):
    await callback.answer('')
    cb = callback.data.split('_')[1]
    if cb.startswith('back'):
        await callback.answer('Вы выбрали: Назад')
        result = cb.split('-')[1]
        data = await select_takelist_by_id_and_name(callback.from_user.id, result)
        string = ''
        for item in data:
            if item.didornot == False:
                string += f'❌{item.body}\n'
            else: string += f'✅{item.body}\n'

        try:
            await callback.message.edit_text(string, reply_markup=await kb.create_inline_keyboard(['Назад-back', f'Отметить сделанное-edit-{str(result)}', f'Удалить-delete-{str(result)}'], 'takelistshown'))
        except TelegramBadRequest:
            await callback.message.answer('Bad request')
    else:
        await callback.answer('')
        result = cb.split('-')
        await update_didornot(str(result[0]), int(result[1]), str(result[2]))
        await callback.message.edit_text('Чтобы отметить нажмите', reply_markup=await kb.get_takelists_body_by_name(result[2], callback.from_user.id))

@router.callback_query(F.data.startswith('takelistshown_'))
async def cb_takelistshowed(callback: CallbackQuery):
    result = callback.data.split('_')[1]
    if result == 'back':
        await callback.answer('Вы выбрали: Назад')
        await callback.message.edit_text('Выберите список дел', reply_markup=await kb.get_takelists_by_id(callback.from_user.id))
    elif result.startswith('edit'):
        await callback.answer('Вы выбрали: Отметить сделанное')
        name_by_cb = result.split('-')[1]
        await callback.message.edit_text('Чтобы отметить нажмите', reply_markup=await kb.get_takelists_body_by_name(name_by_cb, callback.from_user.id))
    elif result.startswith('delete'):
        await callback.answer('Вы выбрали: Удалить')
        name_by_cb = result.split('-')[1]
        await delete_takelist_by_id_and_name(callback.from_user.id, name_by_cb)
        await callback.message.edit_text('Список дел успешно удален', reply_markup=await kb.create_inline_keyboard(['Назад к спискам-back'], 'takelistshown'))

@router.callback_query(F.data.startswith('timetableshown_'))
async def cb_timetableshowed(callback: CallbackQuery):
    result = callback.data.split('_')[1]
    if result == 'back':
        await callback.answer('Вы выбрали: Назад')
        await callback.message.edit_text('Выберите расписание', reply_markup=await kb.get_timetables_by_id(callback.from_user.id))
    elif result.startswith('delete'):
        await callback.answer('Вы выбрали: Удалить')
        name_by_cb = result.split('-')[1]
        await delete_timetable_by_id_and_name(callback.from_user.id, name_by_cb)
        await callback.message.edit_text('Расписание успешно удалено', reply_markup=await kb.create_inline_keyboard(['Назад к расписаниям-back'], 'timetableshown'))

@router.callback_query(F.data.startswith('eventshown_'))
async def cb_eventshown(callback: CallbackQuery):
    result = callback.data.split('_')[1]
    if result == 'back':
        await callback.answer('Вы выбрали: Назад')
        await callback.message.edit_text('Выберите мероприятие', reply_markup=await kb.get_events_by_id(callback.from_user.id))
    elif result.startswith('delete'):
        await callback.answer('Вы выбрали: Удалить')
        name_by_cb = result.split('-')[1]
        await delete_event_by_id_and_name(callback.from_user.id, name_by_cb)
        await callback.message.edit_text('Мероприятие успешно удалено', reply_markup=await kb.create_inline_keyboard(['Назад к мероприятиям-back'], 'eventshown'))

@router.callback_query(F.data.startswith('noteshown_'))
async def cb_noteshown(callback: CallbackQuery):
    result = callback.data.split('_')[1]
    if result == 'back':
        await callback.answer('Вы выбрали: Назад')
        await callback.message.edit_text('Выберите заметку', reply_markup=await kb.get_notes_by_id(callback.from_user.id))
    elif result.startswith('delete'):
        await callback.answer('Вы выбрали: Удалить')
        name_by_cb = result.split('-')[1]
        await delete_note_by_id_and_name(callback.from_user.id, name_by_cb)
        await callback.message.edit_text('Заметка успешно удалена', reply_markup=await kb.create_inline_keyboard(['Назад к заметкам-back'], 'noteshown'))

    
            

