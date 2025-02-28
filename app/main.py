from fastapi import FastAPI
from app.routes import health, auth, users
from app.utils.logger import logger
from app.database import create_db_and_tables

app = FastAPI()

@app.get("/api/index")
def read_root():
    logger.info("Accessing the root route")
    return {"message": "Welcome to the e-commerce API!"}

app.include_router(health.router, prefix="/api")
app.include_router(auth.router, prefix="/api/auth")
app.include_router(users.router, prefix="/api/users")

@app.on_event("startup")
async def on_startup():
    logger.info("Creating database tables")
    create_db_and_tables()