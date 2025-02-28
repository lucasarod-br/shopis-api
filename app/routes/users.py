from app.schemas.user import UserResponse, UserUpdate
from app.auth.auth import get_current_user, get_password_hash
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from app.models.user import User
from app.database import SessionDep
from datetime import datetime
from uuid import UUID
from app.auth.auth import oauth2_scheme

router = APIRouter(
    dependencies=[Depends(oauth2_scheme)]
)

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user

@router.get("/{user_id}", response_model=UserResponse)
async def read_user_by_id(user_id: UUID, session: SessionDep):
    user = session.query(User).filter(User.id == user_id).filter(User.is_deleted == False).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@router.get("/", response_model=list[UserResponse])
async def read_users(session: SessionDep):  
    users = session.query(User).all()
    return users

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: UUID, user: UserUpdate, session: SessionDep):
    db_user = session.query(User).filter(User.id == user_id).filter(User.is_deleted == False).first()
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    update_data = user.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    db_user.updated_at = datetime.now()
    session.commit()
    session.refresh(db_user)
    return db_user

@router.delete("/{user_id}", response_model=UserResponse)
async def delete_user(user_id: UUID, session: SessionDep):
    db_user = session.query(User).filter(User.id == user_id).filter(User.is_deleted == False).first()
    db_user.soft_delete()
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    db_user.is_active = False

    session.commit()
    return db_user

@router.put("/{user_id}/activate", response_model=UserResponse)
async def activate_user(user_id: UUID, session: SessionDep):
    db_user = session.query(User).filter(User.id == user_id).filter(User.is_deleted == False).first()
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    db_user.is_active = True
    db_user.restore()

    session.commit()
    return db_user

@router.put("/{user_id}/deactivate", response_model=UserResponse)
async def deactivate_user(user_id: UUID, session: SessionDep):
    db_user = session.query(User).filter(User.id == user_id).filter(User.is_deleted == False).first()
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    db_user.is_active = False
    db_user.soft_delete()
    session.commit()
    return db_user
