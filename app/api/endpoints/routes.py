from fastapi import APIRouter
from fastapi import Body

from typing import Annotated

router = APIRouter()


@router.post("/")
async def get_none(x: Annotated[dict, Body()]):
    result = {
        "data": "data super 123",
        "data2": 123,
    }
    return result
