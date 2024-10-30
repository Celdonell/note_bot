from sqlalchemy import select, update, delete

from database.models import Takelists, Timetables, Events, Notes, async_session

async def insert_into_takelists(tg_id: int, name: str, body: str):
    async with async_session() as session:
        session.add(Takelists(isbn = None, name = name, tg_id = tg_id, body = body, didornot = False))
        return await session.commit()

async def insert_into_timetables(tg_id: int, name: str, body: str, date: str):
    async with async_session() as session:
        session.add(Timetables(isbn = None, name = name, tg_id = tg_id, body = body, date = date))
        return await session.commit()

async def insert_into_events(tg_id: int, name: str, body: str, date: str, adress: str):
    async with async_session() as session:
        session.add(Events(isbn = None, tg_id = tg_id, name = name, body = body, date = date, adress = adress))
        return await session.commit()

async def insert_into_notes(tg_id: int, name: str, body: str):
    async with async_session() as session:
        session.add(Notes(isbn = None, tg_id = tg_id, name = name, body = body))
        return await session.commit()