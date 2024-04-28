from fastapi import FastAPI, HTTPException, Query, Depends
from pymongo import MongoClient
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from model import ItemModel # model
from dal import ItemDAL # DAL
from services import ItemService # BLL
from common import get_logger
from db_config import MongoDBManager

logger = get_logger()

app = FastAPI()
# static files
app.mount("/static", StaticFiles(directory="../static"), name="static")

MongoDBManager.connect()
db = MongoDBManager.get_db()

#DAL
item_dal = ItemDAL(db=db)
#BLL
item_service = ItemService(item_dal=item_dal)

@app.post("/items/")
def api_create_item(item: ItemModel):
    created_item = item_service.create_item(item)
    if created_item:
        return {"message": "Item created successfully.", "item": created_item}
    else:
        raise HTTPException(status_code=400, detail="Item with this ID already exists")

@app.get("/items/")
def api_read_item(item_id: int = Query(...)):
    logger.info(f"API get /items/{item_id}")

    item = item_service.get_item(item_id)
    logger.debug(f"Item: {item}")
    
    if item:
        return item
    else:
        raise HTTPException(status_code=404, detail="Item not found")

@app.get("/items/all")
def api_read_all_items():
    items = item_service.get_all_items()
    return items

@app.get("/db/status")
def db_status():
    status = MongoDBManager.get_status()
    return {f"status: {status}"}

@app.get("/db/connect")
def db_connect():
    """
        測試用，初始化有正常連線即可，不需要另外做
    """
    try:
        if MongoDBManager.connect():
            return {"message": "Successfully connected to MongoDB."}
        else:
            return {"message": "Failed to connect to MongoDB."}
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        raise HTTPException(status_code=500, detail="Internal server error while connecting to MongoDB.")

@app.get("/db/close")
def db_close():
    """
        測試用，MongoDB 不需要主動關閉連線
    """
    closed = MongoDBManager.close_connection()
    if closed:
        return {"message": "MongoDB connection closed successfully"}
    else:
        return {"message": "MongoDB was not connected"}