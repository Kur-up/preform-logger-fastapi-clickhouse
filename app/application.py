import uuid
import datetime
import json

from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse

from .api import *
from .databases.clickhouse.core import clickhouse_init_tables
from .databases.clickhouse.queries import clickhouse_add_request

title = "preform-logger-fastapi-clickhouse"
description = """# Requests logger for FastAPI #"""

app = FastAPI(
    title=title,
    description=description,
    version="1.0.0",
)

app.include_router(router_routes, tags=["Test routes"])


@app.on_event("startup")
async def startup_event():
    await clickhouse_init_tables()


@app.middleware("http")
async def add_requests_data_middleware(request: Request, call_next):
    datetime_stamp = datetime.datetime.utcnow()
    request.state.id = uuid.uuid4()
    request.state.datetime = datetime_stamp.strftime("%Y-%m-%d %H:%M:%S")

    await set_body(request, await request.body())
    request.state.body = await get_body(request)

    response = await call_next(request)

    datetime_stamp = datetime.datetime.utcnow()
    res_datetime = datetime_stamp.strftime("%Y-%m-%d %H:%M:%S")

    await clickhouse_add_request(request, response, res_datetime)
    return response


@app.get("/health", include_in_schema=False)
async def get_health():
    return JSONResponse(status_code=200, content="OK")


# Thanks, Man!
# https://github.com/tiangolo/fastapi/issues/394?ysclid=ljml3ddfej173493584#issuecomment-883524819
async def set_body(request: Request, body: bytes):
    async def receive():
        return {"type": "http.request", "body": body}

    request._receive = receive


async def get_body(request: Request) -> bytes:
    body = await request.body()
    await set_body(request, body)
    return body
