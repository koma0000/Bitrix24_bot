import asyncio
import os
from celery import Celery
from app.bitrix import Bitrix, BitrixAPIException
from app.telegram_bot import send_file_to_telegram, send_failure_message
from dotenv import load_dotenv

load_dotenv()
celery_app = Celery("tasks", broker=os.getenv("CELERY_BROKER_URL"))


@celery_app.task
def process_deal(deal_id: int):
    bitrix = Bitrix(os.getenv("BITRIX_WEBHOOK_URL"))
    try:
        file_url = bitrix.get_file_url(deal_id)
        print(file_url)

        if file_url:
            file_content = bitrix.download_file(file_url)
            if file_content:
                message = f"Файл по сделке {deal_id}"
                asyncio.run(send_file_to_telegram(file_content, message, file_content.name))
            else:
                raise BitrixAPIException(f"Не удалось скачать файл по сделке {deal_id}")
        else:
            raise BitrixAPIException(f"У сделки {deal_id} не обнаружен файл")
    except BitrixAPIException as e:
        message = str(e)
        asyncio.run(send_failure_message(message))
