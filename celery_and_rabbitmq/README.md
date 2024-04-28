# Celery, RabbitMQ and Redis
透過Docker 設計一個服務包含Web API 使用Celery 進行任務管理，並由RabbitMQ進行任務排程、由Redis 提供資料暫存。
1. 設計一個簡單的API能接收資料並寫入資料庫
2. API接到之後會把任務指定到RabbitMQ其中的某個Queue
3. Celery透過RabbitMQ 執行任務排程依序處理
4. 如:寫入資料庫、自動執行Script...
6. 任務完成後Redis 會把任務相關的資料暫存供使用
7. 另外使用Celery Beat 定期執行某項script
## Celery 任務管理
* **Worker** - 在docker-compose中啟動
```bash!
#基本啟動worker方法
celery -A tasks worker --loglevel=info
#同時有四個工作線程
celery -A tasks worker --loglevel=info --concurrency=4
#監聽high_priority 和default 這兩個Queue
celery -A tasks worker --loglevel=info -Q high_priority,default
```
* 在task.py中定義Celery的應用
    * Broker - 接收client傳來的任務，並傳給RabbitMQ或其他工作排程工具。
    * Backend - 儲存task的結果，常用於監控。通常使用Redis或其他DB。
```python!
app = Celery('myapp',
             broker='amqp://guest:guest@localhost//',
             backend='redis://localhost:6379/0')
```
* **Task** - 使用'@app.task'標記，Celery就可透過Worker 異步執行。
    * API、I/O...
* **Beat** - 用於定期執行任務，週期性，可自由設計循環週期。
* 指定傳送任務到RabbitMQ的Queue
### 多個Queue
* 如果同時有多個Queue，且需要視情況發送任務到指定的Queue。
* 會使用到Exchange、Routing_key、Binding_key
    * Exchange：交換機，指定消息的發送方式，Direct、Topic、Fanout、Headers。
    * Routing_key：消息收到後會根據其Routing_key 選擇發送到指定的Queue。
    * Binding_key：在Exchange 和Queue中綁定使用的，用來指定帶有特定Routing_key的消息會被傳送到指定的Queue。
```python!
#task.py
from celery import Celery
from kombu import Exchange, Queue

app = Celery('tasks', broker='amqp://guest:guest@rabbitmq//')

# Exchange
default_exchange = Exchange('default', type='direct')
custom_exchange = Exchange('custom', type='direct')

# Queue
default_queue = Queue('default', exchange=default_exchange, routing_key='default')
high_priority_queue = Queue('high_priority', exchange=custom_exchange, routing_key='high_priority')
# 
app.conf.task_queues = (default_queue, high_priority_queue)

@app.task
def add(x, y):
    return x + y

# default
app.conf.task_default_exchange = 'default'
app.conf.task_default_exchange_type = 'direct'
app.conf.task_default_routing_key = 'default'
```
```python!
# main.py
add.apply_async(args=[10, 20], queue='high_priority', exchange='custom', routing_key='high_priority')
```

## RabbitMQ 任務排程
* 提供任務Queue
* 進行任務排程
## Redis 資料暫存
* 儲存任務ID，供後續查詢任務完成狀態
* 其他暫存資料
* 速度快
## 架構圖
![image](https://hackmd.io/_uploads/Sy80wi3lC.png)

## 詳細說明
### docker-compose.yml
在docker-compose.yml中，worker 的container 如果要指定Queue進行列隊的話需要在輸入指令celery 時就使用 -Q 宣告需要監聽的Queue，可以視情況增加。
```yaml!
  worker:
    container_name: worker
    build: .
    depends_on:
      - rabbitmq
      - mongodb
    networks:
      - app-network
    command: celery -A tasks worker --loglevel=info -Q mongo_queue
```
