from fastapi import APIRouter, Depends, status, HTTPException
# Сессия БД
from sqlalchemy.orm import Session
# Функция подключения к БД
from app.backend.db_depends import get_db
# Аннотации, Модели БД и Pydantic.
from typing import Annotated
from app.models import User
from app.schemas import CreateUser, UpdateUser
# Функции работы с записями.
from sqlalchemy import insert, select, update, delete
# Функция создания slug-строки
from slugify import slugify


router = APIRouter(prefix="/task", tags=["task"])


@router.get("/all_task")
async def get_all_task():
    pass


@router.get("/task_id")
async def task_by_id():
    pass


@router.post("/create")
async def create_task():
    pass


@router.put("/update")
async def update_task():
    pass


@router.delete("/delete")
async def delete_task():
    pass
