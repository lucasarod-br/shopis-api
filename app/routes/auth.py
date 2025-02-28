from fastapi import APIRouter, Depends, HTTPException, status
from app.database import SessionDep
from app.models.user import User
from app.schemas.user import UserCreate,  UserResponse, UserToken
from app.auth.auth import verify_password, get_password_hash, create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserToken
from typing import Annotated
from uuid import UUID

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, session: SessionDep):
    try:
        hashed_password = get_password_hash(user.password)
        db_user = User(
            name=user.name,
            email=user.email,
            hashed_password=hashed_password,
            phone=user.phone,
            cpf=user.cpf,
            is_active=True,
            role_id=1
        )
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/token", response_model=UserToken)
async def login( session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()],):
    db_user = session.query(User).filter(
        (User.email == form_data.username) |
        (User.cpf == form_data.username) |
        (User.phone == form_data.username)
    ).first()

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if not db_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is not active"
        )
    
    if not verify_password(form_data.password.encode('utf-8'), db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid password"
        )
    access_token = create_access_token(data={"sub": str(db_user.id), "name": db_user.name})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/recover-password")
async def recover_password(username: str, session: SessionDep):
    user = session.query(User).filter(
        (User.email == username) |
        (User.cpf == username) |
        (User.phone == username)
    ).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {"message": "Password recovery email sent"}

@router.put("/reset-password")
async def reset_password(id: str, new_password: str, session: SessionDep
):
    try:
        user_id = UUID(id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )

    user = session.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    print(new_password)
    print(id)

    user.hashed_password = get_password_hash(new_password)
    session.commit()
    return {"message": "Password reset successfully"}

@router.get("/verify-email")
async def verify_email(token: str, session: SessionDep):
    pass

