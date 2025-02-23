from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal, get_db

router = APIRouter()

# Função para verificar a conexão com o banco de dados
def check_db_health(db: Session):
    try:
        # Executa uma query simples para testar a conexão
        db.execute("SELECT 1").fetchone()
        return True
    except Exception as e:
        print(f"Database health check failed: {e}")
        return False

# Rota de health check
@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    # Verifica se a aplicação está respondendo
    app_status = {"status": "up"}

    # Verifica a saúde do banco de dados
    if not check_db_health(db):
        raise HTTPException(status_code=500, detail="Database is down")

    return {"app": app_status, "database": "up"}
