import sqlite3
from aiogram import Dispatcher, types
from create_bot import bot
from data_base import sqlite_db
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from time import localtime, sleep


class FSMReport(StatesGroup):
    user_name = State()
    text1= State()
    text2= State()
    text3= State()
    year= State()
    mon= State()
    day= State()



async def command_start(message : types.Message):
    if message.chat.type == 'private':
        ad = sqlite3.connect('base.db').cursor()
        admin_ID = list(ad.execute('SELECT admin_id FROM admin').fetchall())
        i = (message.from_user.id)
        if i in admin_ID:
            pass
        else:
            if not sqlite_db.user_exists(message.from_user.id):
                sqlite_db.add_user(message.from_user.id)
            await bot.send_message(message.from_user.id, "Привет")
            while True:
                time_year, time_mon, time_day, time_hour, time_min, time_sec= localtime().tm_year, localtime().tm_mon,localtime().tm_mday, localtime().tm_hour, localtime().tm_min, localtime().tm_sec
                if time_hour == 1 and time_min == 1 and time_sec == 30:
                    sqlite_db.cur('UPDATE client SET send_true = ? WHERE user_id', (1, message.from_user.id))
                send_true = sqlite_db.cur.execute('SELECT send_true FROM client WHERE user_id').fetchall
                if time_hour >= 20 and time_hour < 24 and time_min in [1,2,3,4,5,6, 15, 30, 45, 50, 59] and time_sec == 1 and send_true == 1:
                    users = sqlite_db.get_users()
                    for rel in users:
                        try:
                            await bot.send_message(rel[0], 'Пожалуйста отправте ваш отчёт с помощью команды\n/my_report')
                            
                            if int(rel[1]) != 1:
                                sqlite_db.set_active(rel[0], 1)
                        except:
                            sqlite_db.set_active(rel[0], 0)
                if time_hour == 11 and time_sec == 30:
                    sqlite_db.add_omission(message.from_user, time_year, time_mon, time_day)     
                sleep(1)

async def cm_start(message : types.Message):
    if message.chat.type == 'private':
        await FSMReport.text1.set()
        sqlite_db.cur('UPDATE client SET send_true = ? WHERE user_id', (0, message.from_user.id))
        await message.reply('Что вы делали вчера?\n/cansel - если не хотите отправлять этот отчёт')

async def load_text1(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['text1'] = message.text
        data['user_name'] = message.from_user.full_name
        await message.answer('Какие проблемы были при работе')
    await FSMReport.next()

async def load_text2(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['text2'] = message.text
        await message.answer('Чем вы будете сегодня делать')
    await FSMReport.next()

async def load_text3(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['text3'] = message.text
        data['year'] = localtime().tm_year
        data['mon'] = localtime().tm_mon
        data['day'] = localtime().tm_mday
        await message.answer('Загружено')
    await FSMReport.next()

    await sqlite_db.sql_add_command(state)

    await state.finish()

async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    sqlite_db.cur('UPDATE client SET send_true = ? WHERE user_id', (1, message.from_user.id))
    await state.finish()
    await message.reply('OK')
 



def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(cm_start, commands=['my_report'], state=None)
    dp.register_message_handler(load_text1, state=FSMReport.text1)
    dp.register_message_handler(load_text2, state=FSMReport.text2)
    dp.register_message_handler(load_text3, state=FSMReport.text3)
    dp.register_message_handler(cancel_handler, state="*", commands='cansel')