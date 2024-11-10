from fastapi import APIRouter, Depends, status, HTTPException
# Сессия БД
from sqlalchemy.orm import Session
# Функция подключения к БД
from app.backend.db_depends import get_db
# Аннотации, Модели БД и Pydantic.
from typing import Annotated
from app.models import User, Task
from app.schemas import CreateUser, UpdateUser
# Функции работы с записями.
from sqlalchemy import insert, select, update, delete
# Функция создания slug-строки
from slugify import slugify


router = APIRouter(prefix="/user", tags=["user"])


@router.get("/all_user")
async def get_all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.scalars(select(User)).all()
    return users


@router.get("/user_id")
async def user_by_id(user_id: int, db: Annotated[Session, Depends(get_db)]):
    user = db.scalar(select(User).where(User.id == user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    return user


@router.post("/create")
async def create_user(create_user: CreateUser, db: Annotated[Session, Depends(get_db)]):
    user = db.scalar(select(User).where(User.username == create_user.username))
    if user:
        raise HTTPException(
            status_code=status.HTTP_302_FOUND,
            detail='Sorry, User already exists'
        )
    db.execute(insert(User).values(
        username=create_user.username,
        firstname=create_user.firstname,
        lastname=create_user.lastname,
        age=create_user.age,
        slug=slugify(create_user.username)
    ))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }


@router.put("/update")
async def update_user(update_user: UpdateUser, user_id: int, db: Annotated[Session, Depends(get_db)]):
    current_user = db.scalar(select(User).where(User.id == user_id))
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    db.execute(update(User).where(User.id == user_id).values(
        firstname=update_user.firstname,
        lastname=update_user.lastname,
        age=update_user.age
    ))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'User update successful!'
    }


@router.delete("/delete")
async def delete_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    user = db.scalar(select(User).where(User.id == user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    db.execute(delete(User).where(User.id == user_id))
    db.execute(delete(Task).where(Task.user_id == user_id))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'User delete successful!'
    }
