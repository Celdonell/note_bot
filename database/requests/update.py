from sqlalchemy import select, update, delete

from database.models import Takelists, Timetables, Events, Notes, async_session

async def update_didornot(body, tg_id, name):
    async with async_session() as session:
        query = update(Takelists).where(Takelists.name == name, Takelists.body == body, Takelists.tg_id == tg_id).values(didornot = True)
        await session.execute(query)
        return await session.commit()



