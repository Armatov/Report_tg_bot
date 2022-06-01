import sqlite3 as sq
from create_bot import bot
from time import localtime

def sql_start():
    global base, cur
    base = sq.connect('base.db')  # создаёт или подключается к базе данных
    cur = base.cursor()
    if base:
        print('Я подключена к базе')
    base.execute('CREATE TABLE IF NOT EXISTS report(user_name TEXT, text1 TEXT, text2 TEXT, text3 TEXT, year INEGER, mon INTEGER, day INTEGER)') #создаем нужные нам столбыцы для таблицы
    base.execute('CREATE TABLE IF NOT EXISTS admin(admin_id INTEGER, group_id INTEGER)')
    base.execute('CREATE TABLE IF NOT EXISTS client(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER UNIQUE, active INTEGER DEFAULT (1), send_true INTEGER DEFAULT (1))') #создаем нужные нам столбыцы для таблицы
    base.execute('CREATE TABLE IF NOT EXISTS omission(user_name TEXT, year INEGER, mon INTEGER, day INTEGER)')
    base.commit()



# Данные зарегистрироанных админов
async def sql_add_admin(id):
    cur.execute('INSERT INTO admin VALUES (?, ?)', id)  # заполняем таблицу
    base.commit()

# На случай добавки новых админов
def sgl_admin_and_group_data():
    ad = sq.connect('base.db').cursor()
    return list(ad.execute('SELECT admin_id, group_id FROM admin').fetchall())

def sgl_admin_data():
    ad = sq.connect('base.db').cursor()
    return list(ad.execute('SELECT admin_id FROM admin').fetchall())

async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO report VALUES (?, ?, ?, ?, ?, ?, ?)', tuple(data.values()))  # заполняем таблицу
        base.commit()

# отправляем все содержимое базы данных
async def sql_read(message):
    time = cur.execute('SELECT yaer, mon FROM report').fetchall 
    time_now = (localtime().tm_year, localtime().tm_mon)
    for ret in cur.execute('SELECT user_name, text1, text2, text3, year, mon, day  FROM report').fetchall():
            if time_now in time:
                await bot.send_document(message.from_user.id, f"От пользователя: {ret[0]} \nЯ занимался:\n{ret[1]}\n---------\nУ меня были проблемы с:\n{ret[2]}\n---------\nСегодня я буду заниматься:\n{ret[3]}\n---------\nдата:{ret[4]}.{ret[5]}.{ret[6]}")


def user_exists(user_id):
    with base: 
        result = cur.execute('SELECT * FROM client WHERE user_id = (?)', (user_id,)).fetchmany(1)
        return bool(len(result))

def add_user(user_id):
    with base:
        return cur.execute('INSERT INTO client (user_id) VALUES (?)', (user_id,))

def set_active(user_id, active):
    with base:
        return cur.execute('UPDATE client SET active = ? WHERE user_id = ?', (active, user_id,))

def get_users():
    with base:
        return cur.execute('SELECT user_id, active FROM client').fetchall()

def add_omission(user_name, year, mon, day):
    with base:
        return cur.execute('INSERT INTO omission VALUES (?, ?, ?, ?)', (user_name, year, mon, day,))