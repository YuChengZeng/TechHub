# health_check.py
from fastapi import APIRouter, HTTPException, FastAPI
from db_config import MongoDBManager
from common import get_logger
import asyncio

logger = get_logger()
router = APIRouter()

@router.get("/health")
async def health_check():
    try:
        db_ok = await check_database_connection_async()

        if not db_ok:
            msg = "Database connection failed"
            logger.error(msg)
            raise HTTPException(status_code=503, detail=msg)

        logger.info("Health check passed")
        return {"status": "ok"}

    except Exception as e:
        logger.exception("An unexpected error occurred during health check")
        raise HTTPException(status_code=500, detail=str(e))

async def check_database_connection_async():
    loop = asyncio.get_running_loop()
    db_status = await loop.run_in_executor(None, MongoDBManager.get_status)
    return db_status == "connected"