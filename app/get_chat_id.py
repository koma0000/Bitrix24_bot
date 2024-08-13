from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import os

bot = Bot(token=os.getenv("TELEGRAM_TOKEN"))

dp = Dispatcher(bot)

@dp.message_handler(content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def on_new_chat_member(message: types.Message):
    for member in message.new_chat_members:
        if member.id == (await bot.me).id:
            chat_id = message.chat.id
            chat_title = message.chat.title
            print(f'Бот добавлен в канал: {chat_title} (ID: {chat_id})')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
