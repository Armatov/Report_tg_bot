from aiogram import Dispatcher, types
async def command_help(message: types.Message):
    await message.answer('Команды которые можно использовать\n/start - начало работы и регистрация\n/help - вывод всех команд\n/my_report- отправка отчёта\n/cansel или отмена - отмена отправки отчёта\n/report - отправялет месячный отчёт администратору\n/moderator - регистрация админа(использовать в группе)')

def register_handler_other(dp: Dispatcher):
    dp.register_message_handler(command_help, commands=['help'])