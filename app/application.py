import uuid
import datetime
import json
import queue

from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.concurrency import iterate_in_threadpool
from fastapi_utils.tasks import repeat_every

from .api import *
from .databases.clickhouse.core import clickhouse_init_tables
from .databases.clickhouse.core import execute_requests

ch_queue = queue.Queue()

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


@app.on_event("startup")
@repeat_every(seconds=10)
async def startup_10secs():
    await execute_requests(ch_queue)


@app.middleware("http")
async def add_requests_data_middleware(request: Request, call_next):
    req_datetime = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    await set_body(request, await request.body())
    req_body = await get_body(request)

    response = await call_next(request)
    res_datetime = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    response_body = [chunk async for chunk in response.body_iterator]
    response.body_iterator = iterate_in_threadpool(iter(response_body))
    res_body = response_body[0].decode()

    row_data = {
        "id": str(uuid.uuid4()).replace("'", "\\'"),
        "partition_datetime": req_datetime,
        "req_datetime": req_datetime,
        "req_ip": str(request.client.host).replace("'", "\\'"),
        "req_method": str(request.method).replace("'", "\\'"),
        "req_url": str(request.url).replace("'", "\\'"),
        "req_path": str(request.url.path).replace("'", "\\'"),
        "req_query": str(request.url.query).replace("'", "\\'"),
        "req_body": str(req_body.decode()).replace("'", "\\'"),
        "req_headers": str(request.headers).replace("'", "\\'"),
        "req_cookies": str(request.cookies).replace("'", "\\'"),
        "res_datetime": res_datetime,
        "res_code": str(response.status_code).replace("'", "\\'"),
        "res_body": str(res_body).replace("'", "\\'"),
        "res_headers": str(response.headers).replace("'", "\\'"),
    }
    ch_queue.put(row_data)
    return response


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
