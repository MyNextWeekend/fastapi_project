"""
任务相关
"""
from typing import List

from fastapi import APIRouter
from sqlmodel import select

from app.dependencies import SessionDep
from app.models.first_model import Task
from app.models.resp import Resp
from app.utils.log_utils import Log

logger = Log().get_logger()

router = APIRouter(prefix="/task", tags=["任务操作"])


@router.get("/", summary="查询所有")
async def get_tasks(session: SessionDep, skip: int = 0, limit: int = 100) -> Resp[List[Task]]:
    statement = select(Task).offset(skip).limit(limit)
    return Resp.success(session.exec(statement).all())


@router.get("/{item_id}", summary="查询单个")
async def get_task(item_id: int, session: SessionDep) -> Resp[Task]:
    return Resp.success(session.get(Task, item_id))
