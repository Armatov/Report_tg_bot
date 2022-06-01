import sqlite3
from aiogram import Dispatcher, types
from create_bot import bot
from data_base import sqlite_db


# команда определеия администратора
async def make_changes_command(message: types.Message):
    ID = message.from_user.id
    sqlite_db.cur.execute(f'SELECT admin_id FROM admin WHERE admin_id = {ID}')
    data = sqlite_db.cur.fetchone()
    if data is None:
        admin_and_group_id = [ID, message.chat.id]
        await sqlite_db.sql_add_admin(admin_and_group_id)
        try:
            await bot.send_message(message.from_user.id, 'Что вам угодно?')
            await message.delete()
        except:
            await message.reply('Пожалуйста напишите мне в ЛС:\n@Job_Reports_bot')


# команда принятия отчетов
async def report_command(message: types.Message):
    ad = sqlite3.connect('base.db').cursor()
    admin_and_group_ID = list(ad.execute('SELECT admin_id, group_id FROM admin').fetchall())
    i = (message.from_user.id, message.chat.id)
    if i in admin_and_group_ID:
        try:
            await sqlite_db.sql_read(message)
        except:
            await message.reply('Пожалуйста напишите мне в ЛС:\n@Job_Reports_bot')
        

def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(make_changes_command, commands=['moderator'], is_chat_admin=True)
    dp.register_message_handler(report_command, commands=['report'])