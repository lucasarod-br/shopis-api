from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..utils.logger import logger
from ..utils.db_session import get_db
from sqlalchemy.sql import text

router = APIRouter()

# Function to check the database connection
def check_db_health(db: Session):
    try:
        db.execute(text("SELECT 1")).fetchone()
        return True
    except Exception as e:
        print(f"Database health check failed: {e}")
        return False

# Health check route
@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    # Check if the application is responding
    app_status = {"status": "up"}

    # Check the health of the database
    if not check_db_health(db):
        logger.error("Database is down")
        raise HTTPException(status_code=500, detail="Database is down")

    return {"app": app_status, "database": "up"}
