from celery import Celery
from mongodb_config import MongoDB
from kombu import Queue
import requests

# Celery
app = Celery('tasks',
             broker='amqp://guest:guest@rabbitmq//',
             backend='redis://redis:6379/0')

# Celery Queue
app.conf.task_queues = (
   Queue('mongo_queue', routing_key='mongo_queue'),
)

# MongoDB
mongodb = MongoDB()
collection = mongodb.get_collection()

@app.task(queue='mongo_queue')
def write_to_mongo(data):
    try:
        result = collection.insert_one(data)
        return str(result.inserted_id)
    except Exception as e:
        print(f"Error inserting data into MongoDB: {e}")
        return None

@app.task(queue='mongo_queue')
def fetch_items():
    try:
        items = list(collection.find({}))
        for item in items:
            item['_id'] = str(item['_id'])
        return items
    except Exception as e:
        return {'error': str(e)}
    
# Celery Beat 
app.conf.beat_schedule = {
    'fetch-items-every-5sec': {
        'task': 'tasks.fetch_items',
        'schedule': 5.0,
        'args': (),
        # 'options': {'queue': 'mongo_queue'}
        # 也可以在Beat中指定queue，不然就使用task中的queue
    }
}