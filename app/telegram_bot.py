import os
from aiogram import Bot, types

#Отправка сообщения с файлом
async def send_file_to_telegram(file_content: bytes, message: str, file_name: str):
    bot = Bot(token=os.getenv("TELEGRAM_TOKEN"))
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    # message_template = os.getenv("SUCCESS_MESSAGE_TEMPLATE") + " {deal_id}"
    # message = message_template.format(deal_id=deal_id)

    await bot.send_document(chat_id=chat_id, document=types.InputFile(file_content, file_name), caption=message)
    await bot.close()

#Отправка сообщения в случае отсуст файла
async def send_failure_message(message: str):
    bot = Bot(token=os.getenv("TELEGRAM_TOKEN"))
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    # message_template = os.getenv("FAILURE_MESSAGE_TEMPLATE") + " {deal_id}"
    # message = message_template.format(deal_id=deal_id)

    await bot.send_message(chat_id=chat_id, text=message)
    await bot.close()
