from sqlalchemy import BigInteger
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

from config import config

engine = create_async_engine(url=config.DATABASE_URL.get_secret_value())
async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class Takelists(Base):
    __tablename__ = 'takelists'

    isbn: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column()
    body: Mapped[str] = mapped_column()
    didornot: Mapped[bool] = mapped_column()

class Timetables(Base):
    __tablename__ = 'timetables'

    isbn: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column()
    body: Mapped[str] = mapped_column()
    date: Mapped[str] = mapped_column()

class Events(Base):
    __tablename__ = 'events'

    isbn: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column()
    body: Mapped[str] = mapped_column()
    date: Mapped[str] = mapped_column()
    adress: Mapped[str] = mapped_column()
    
class Notes(Base):
    __tablename__ = 'notes'

    isbn: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column()
    body: Mapped[str] = mapped_column()

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

