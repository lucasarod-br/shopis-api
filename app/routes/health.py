from fastapi import APIRouter, HTTPException
from app.utils.logger import logger
from app.database import check_database_health, SessionDep
router = APIRouter()

# Health check route
@router.get("/health")
def health_check(session: SessionDep):
    # Check if the application is responding
    app_status = {"status": "up"}

    # Check if the database is responding
    try:
       check_database_health(session)
    except Exception as e:
        logger.error(f"Database is down: {e}")
        raise HTTPException(status_code=500, detail="Database is down")
    return {"app": app_status, "database": "up"}
