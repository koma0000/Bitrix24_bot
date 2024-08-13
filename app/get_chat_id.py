from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from dotenv import load_dotenv
import os

# Загрузить переменные окружения из .env файла
load_dotenv()

# Инициализация бота
bot = Bot(token=os.getenv("TELEGRAM_TOKEN"))
dp = Dispatcher(bot)


async def send_test_message():
    channel_id = -4204753528  # Укажите ID вашего канала
    message = "Это тестовое сообщение в канал"
    # 4268211030 Сергей
    try:
        await bot.send_message(chat_id=channel_id, text=message)
        print(f"Сообщение успешно отправлено в канал {channel_id}")
    except Exception as e:
        print(f"Не удалось отправить сообщение: {e}")


async def on_startup(dp):
    await send_test_message()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
