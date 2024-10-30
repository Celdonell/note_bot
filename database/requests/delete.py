from sqlalchemy import select, update, delete

from database.models import Takelists, Timetables, Events, Notes, async_session

async def delete_takelist_by_id_and_name(tg_id, name):
    async with async_session() as session:
        query = delete(Takelists).where(Takelists.tg_id == tg_id, Takelists.name == name)
        await session.execute(query)
        return await session.commit()
    
async def delete_timetable_by_id_and_name(tg_id, name):
    async with async_session() as session:
        query = delete(Timetables).where(Timetables.tg_id == tg_id, Timetables.name == name)
        await session.execute(query)
        return await session.commit()
    
async def delete_event_by_id_and_name(tg_id, name):
    async with async_session() as session:
        query = delete(Events).where(Events.tg_id == tg_id, Events.name == name)
        await session.execute(query)
        return await session.commit()
    
async def delete_note_by_id_and_name(tg_id, name):
    async with async_session() as session:
        query = delete(Notes).where(Notes.tg_id == tg_id, Notes.name == name)
        await session.execute(query)
        return await session.commit()