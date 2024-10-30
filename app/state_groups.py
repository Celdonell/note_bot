from aiogram.fsm.state import StatesGroup, State

class inCreateTimetable(StatesGroup):
    name = State()
    body = State()

class inCreateTakelist(StatesGroup):
    name = State()
    body = State()

class inCreateEvent(StatesGroup):
    name = State()
    body = State()
    adress = State()
    date = State()

class inCreateNote(StatesGroup):
    name = State()
    body = State()