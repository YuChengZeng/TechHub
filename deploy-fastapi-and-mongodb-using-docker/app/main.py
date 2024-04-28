from fastapi import FastAPI, HTTPException, Query, Depends
from pymongo import MongoClient
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from model import ItemModel # model
from dal import ItemDAL # DAL
from services import ItemService # BLL

app = FastAPI()
# static files
app.mount("/static", StaticFiles(directory="../static"), name="static")

# MongoDB
MONGO_URL = "mongodb://mongodb:27017/"
client = MongoClient(MONGO_URL)
db = client["mydatabase"]

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
    item = item_service.get_item(item_id)
    if item:
        return item
    else:
        raise HTTPException(status_code=404, detail="Item not found")

@app.get("/items/all")
def api_read_all_items():
    items = item_service.get_all_items()
    return items