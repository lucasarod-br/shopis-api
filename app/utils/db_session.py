from app.database import SessionLocal
from app.utils.logger import logger

# Create a function to open the database session
def get_db():
    db = SessionLocal()
    try:
        logger.info("Database connection established")
        yield db
    finally:
        logger.info("Database connection closed")
        db.close()
