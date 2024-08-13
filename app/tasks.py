import os

from celery import Celery
from app.bitrix import Bitrix
from app.telegram_bot import send_file_to_telegram

celery_app = Celery("tasks", broker=os.getenv("CELERY_BROKER_URL"))

@celery_app.task
def process_deal(deal_id: int):
    bitrix = Bitrix(os.getenv("BITRIX_WEBHOOK_URL"))
    deal = bitrix.get_deal(deal_id)

    file_info = deal.get("UF_CRM_<YOUR_FIELD_NAME>")
    if not file_info:
        message = f"У сделки {deal_id} не обнаружен файл"
    else:
        file_content = bitrix.download_file(file_info)
        message = f"Файл по сделке {deal_id}"
        send_file_to_telegram(file_content, "file_name.ext", message)
