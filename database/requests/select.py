from sqlalchemy import select, update, delete

from database.models import Takelists, Timetables, Events, Notes, async_session

async def select_timetables():
    async with async_session() as session:
        return await session.scalars(select(Timetables))
    
async def select_events():
    async with async_session() as session:
        return await session.scalars(select(Events))

async def select_takelist_by_id(tg_id):
    async with async_session() as session:
        return await session.scalars(select(Takelists).where(Takelists.tg_id == tg_id))
        
async def select_timetable_by_id(tg_id):
    async with async_session() as session:
        return await session.scalars(select(Timetables).where(Timetables.tg_id == tg_id))
    
async def select_event_by_id(tg_id):
    async with async_session() as session:
        return await session.scalars(select(Events).where(Events.tg_id == tg_id))
    
async def select_note_by_id(tg_id):
    async with async_session() as session:
        return await session.scalars(select(Notes).where(Notes.tg_id == tg_id))
    
async def select_takelist_by_id_and_name(tg_id, name):
    async with async_session() as session:
        return await session.scalars(select(Takelists).where(Takelists.name == name, Takelists.tg_id == tg_id))
    
async def select_timetable_by_id_and_name(tg_id, name):
    async with async_session() as session:
        return await session.scalars(select(Timetables).where(Timetables.name == name, Timetables.tg_id == tg_id))
    
async def select_event_by_id_and_name(tg_id, name):
    async with async_session() as session:
        return await session.scalar(select(Events).where(Events.name == name, Events.tg_id == tg_id))
    
async def select_note_by_id_and_name(tg_id, name):
    async with async_session() as session:
        return await session.scalar(select(Notes).where(Notes.name == name, Notes.tg_id == tg_id))
    
async def select_takelist_body_by_id_and_name(tg_id, name):
    async with async_session() as session:
        return await session.scalars(select(Takelists.body).where(Takelists.name == name, Takelists.tg_id == tg_id))
    
async def select_takelist_didornot_by_id_and_name(tg_id, name, body):
    async with async_session() as session:
        return await session.scalar(select(Takelists.didornot).where(Takelists.name == name, Takelists.tg_id == tg_id, Takelists.body == body))
    
async def show_tables():
    async with async_session() as session:
        a = await session.scalars(select(Takelists))
        b = await session.scalars(select(Timetables))
        c = await session.scalars(select(Events))
        d = await session.scalars(select(Notes))

        print('Takelists')
        for i in a:
            print(str(i.isbn)+' '+str(i.tg_id)+' '+i.name+' '+i.body+' '+str(i.didornot))
        print('Timetables')
        for i in b:
            print(str(i.isbn)+' '+str(i.tg_id)+' '+i.name+' '+i.body+' '+i.date)
        print('Events')
        for i in c:
            print(str(i.isbn)+' '+str(i.tg_id)+' '+i.name+' '+i.body+' '+i.date+' '+i.adress)
        print('Notes')
        for i in d:
            print(str(i.isbn)+' '+str(i.tg_id)+' '+i.name+' '+i.body)
        return