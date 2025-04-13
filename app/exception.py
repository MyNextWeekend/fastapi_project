from enum import Enum

from fastapi import FastAPI, Request
from starlette.responses import JSONResponse

from app.models.resp import Resp
from app.utils.log_utils import Log

logger = Log().get_logger()


class ErrorEnum(Enum):
    BAD_REQUEST = (400, "请求参数错误或不符合要求")
    UNAUTHORIZED = (401, "需要用户认证或认证已失效")
    FORBIDDEN = (403, "没有访问该资源的权限")
    NOT_FOUND = (404, "请求的资源不存在")
    INTERNAL_SERVER_ERROR = (500, "服务器内部出现异常")

    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message


class BusinessException(Exception):
    def __init__(self, error: ErrorEnum):
        self.code = error.status_code
        self.message = error.message


def register_exception_handle(server: FastAPI):
    logger.info("register exception handle...")

    @server.exception_handler(BusinessException)
    async def http_business_exception_handler(_: Request, exc: BusinessException):
        return JSONResponse(
            status_code=200,
            content=Resp(code=exc.code, message=exc.message).model_dump()
        )

    @server.exception_handler(Exception)
    async def http_exception_handler(_request: Request, _exc: Exception):
        return JSONResponse(
            status_code=500,
            content=Resp(message="服务内部异常").model_dump()
        )

    logger.info("register exception handle successfully.")
