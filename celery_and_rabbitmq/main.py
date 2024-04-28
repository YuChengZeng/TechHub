from fastapi import FastAPI, HTTPException
from celery.result import AsyncResult
from tasks import fetch_items, write_to_mongo
from tasks import app as celery

app = FastAPI()

@app.post("/tasks/mongo")
# API接收到資料後傳送到指定的RabbitMQ queue
async def run_mongo_task(data: dict):
    task = write_to_mongo.apply_async(args=[data], queue='mongo_queue')
    return {"task_id": task.id}

@app.get("/tasks/{task_id}")
# API接收到task_id後，透過AsyncResult檢查task的狀態
async def get_task_result(task_id: str):
    task_result = AsyncResult(task_id, app=celery)
    if task_result.ready():
        return {"status": "completed", "result": task_result.get()}
    return {"status": "pending"}

@app.get("/items/")
# API收到請求後，到RabbitMQ queue排隊
async def list_items():
    task = fetch_items.apply_async(queue='mongo_queue')
    try:
        items = task.get(timeout=10)
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))