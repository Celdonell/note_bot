import asyncio
from datetime import datetime

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import config
from database.models import async_main
from database.requests.select import select_events
from database.requests.delete import delete_event_by_id_and_name
from handlers import main_handlers, new_table, saved_tables

bot = Bot(token=config.BOT_TOKEN.get_secret_value(), 
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))
async def check_time_every_minute():
    while True:
        await asyncio.sleep(60)
        data = await select_events()
        for item in data:
            item_date = item.date.split(' ')[0]
            item_time = item.date.split(' ')[1].split(':')
            if f'{item_date} {item_time[0]}:{str(int(item_time[1]) - 15)}' == datetime.now().strftime("%d.%m.%Y %H:%M"):
                await bot.send_message(chat_id=item.tg_id, text=f'До вашего события осталось 15 минут!\n\n<b>{item.name} {item.date}</b>\n\n{item.body}\nадрес: {item.adress}')

async def check_time_every_hour():
    while True:
        await asyncio.sleep(2000)
        data = await select_events()
        for item in data:
            item_date = item.date.split(' ')[0]
            item_time = item.date.split(' ')[1].split(':')
            if f'{item_date} {str(int(item_time[0]) - 1)}:{item_time[1]}' == datetime.now().strftime("%d.%m.%Y %H:%M"):
                await bot.send_message(chat_id=item.tg_id, text=f'До вашего события осталось меньше часа!\n\n<b>{item.name} {item.date}</b>\n\n{item.body}\nадрес: {item.adress}')

async def check_time_every_day():
    while True:
        await asyncio.sleep(44000)
        data = await select_events()
        for item in data:
            item_date = item.date.split(' ')[0].split('.')
            item_time = item.date.split(' ')[1]
            if f'{str(int(item_date[0]) - 1)}.{item_date[1]}.{item_date[2]} {item_time}' == datetime.now().strftime("%d.%m.%Y %H:%M"):
                await bot.send_message(chat_id=item.tg_id, text=f'До вашего события осталось меньше часа!\n\n<b>{item.name} {item.date}</b>\n\n{item.body}\nадрес: {item.adress}')

async def check_time():
    while True:
        await asyncio.sleep(10)
        data = await select_events()
        for item in data:
            if item.date == datetime.now().strftime("%d.%m.%Y %H:%M"):
                await delete_event_by_id_and_name(item.tg_id, item.name)

async def main():
    await async_main()
    dp = Dispatcher()
    dp.include_routers(main_handlers.router, new_table.router, saved_tables.router)
    dp["datetime_now"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    print(f'Started at {dp["datetime_now"]}')
    asyncio.get_event_loop().create_task(check_time())
    asyncio.get_event_loop().create_task(check_time_every_hour())
    asyncio.get_event_loop().create_task(check_time_every_minute())
    asyncio.get_event_loop().create_task(check_time_every_day())
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print ('Exit')
    except asyncio.exceptions.CancelledError:
        print ('Session canceled by force')