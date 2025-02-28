from app.database import get_session
from app.utils.logger import logger

# Create a function to open the database session
def get_db():
    db = get_session()
    try:
        logger.info("Database connection established")
        yield db
    finally:
        logger.info("Database connection closed")
        db.close()
