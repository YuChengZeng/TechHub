# Docker Healthy Check And Monitor
## Portainer
用來查看container情況
Docker Desktop 有extension可以裝
https://docs.portainer.io/start/install-ce/server/docker/linux

## Healthy Check
用於檢查container 執行狀態，在docker-compose中預先定義healthycheck，並針對每個container設定檢查條件，如call api或db 指令...
```yml!
#docker-compose.yml
version: '3.8'
services:
  fastapi:
    build: .
    volumes:
      - ./app:/app
      - ./static:/static
    ports:
      - "8000:80"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:80/health"]
      interval: 5s
      timeout: 3s
      retries: 3
      start_period: 5s
    command: uvicorn main:app --host 0.0.0.0 --port 80 --reload
    depends_on:
      - mongodb

  mongodb:
    image: mongo
    volumes:
      - mongodb_data:/data/db
    ports:
      - "27017:27017"
    healthcheck:
      test: ["CMD", "mongosh", "--eval", "db.adminCommand('ping')", "localhost"]
      interval: 5s
      timeout: 3s
      retries: 3
      start_period: 5s

volumes:
  mongodb_data:

```
```python!
# health_check.py
from fastapi import APIRouter, HTTPException, FastAPI
from db_config import MongoDBManager
from common import get_logger
import asyncio

logger = get_logger()
router = APIRouter() 

@router.get("/health")
async def health_check():
    db_ok = await check_database_connection_async()

    if not db_ok:
        logger.error("Database connection failed")
        raise HTTPException(status_code=503, detail="Database connection failed")

    return {"status": "ok"}

async def check_database_connection_async():
    loop = asyncio.get_running_loop()
    db_status = await loop.run_in_executor(None, MongoDBManager.get_status)
    return db_status == "connected"
```

## Monitor
透過設計container的healthcheck，進而判斷服務是否達到運行標準。再結合Grafana和Prometheus，實現健康狀態的追蹤和圖形化介面的呈現，另外也有alert manager (SMTP)能在錯誤發生時發出警告通知。

1. 定義什麼叫服務正常
    * 針對FsatAPI：API正常運作
    * 並且與MongoDB、Redis、MySQL等等能夠正常連線
3. 定義什麼叫服務異常
    * API服務異常
    * DB連線異常
    * 與其他服務連線異常
5. 通知的時機
    * 使用Grafana將服務的即時健康狀態(healthcheck)顯示在畫面上，確保能即時監看。如出現異常可進一步發送通知，如Email或Chat
7. 服務狀態定義的實踐 (正常/異常)
    * 具有API端口的服務能直接打開一個/health路徑並讓docker compose自動在設定的時間背景持續執行與檢查。
    * 通常會檢查FastAPI本身與其他服務的連線狀態。
9. 中間件(Middleware)狀態定義的實踐與資訊的提供
    * 要查看沒有API功能的服務健康狀態可使用專門Exporter實現傳遞服務本身詳細資訊到Prometheus，能夠提供詳細的資訊並便於紀錄和故障排除。