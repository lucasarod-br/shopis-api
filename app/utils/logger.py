import logging

# Basic logging configuration
logging.basicConfig(
    level=logging.INFO,  # Log level (INFO, DEBUG, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Message format
    handlers=[
        logging.StreamHandler(),  # Log to console
        logging.FileHandler("app.log"),  # Log to file
    ]
)

# Create a logger for the current module
logger = logging.getLogger(__name__)
__all__ = ["logger"]
