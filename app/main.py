from fastapi import FastAPI
from app.routes import health
from app.utils.logger import logger

# Create an instance of FastAPI
app = FastAPI()

@app.get("/")
def read_root():
    logger.info("Accessing the root route")
    return {"message": "Welcome to the e-commerce API!"}

# Registra o router de health check
app.include_router(health.router, prefix="/api")