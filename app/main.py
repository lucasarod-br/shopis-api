from fastapi import FastAPI
from .routes import health  # Importe o router de health check

app = FastAPI()

app.include_router(health.router, prefix="/api")