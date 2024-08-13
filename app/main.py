from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from app.tasks import process_deal

app = FastAPI()

# Define a Pydantic model for the request body
class DealRequest(BaseModel):
    deal_id: int

@app.post("/deal")
async def handle_deal(request: DealRequest, background_tasks: BackgroundTasks):
    deal_id = request.deal_id
    background_tasks.add_task(process_deal, deal_id)
    return {"message": "Сделка находится в обработке"}
