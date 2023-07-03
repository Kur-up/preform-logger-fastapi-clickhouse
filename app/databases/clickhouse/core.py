import aiofiles
import aiochclient

from app.config import config


async def get_connection() -> aiochclient.ChClient:
    connection = aiochclient.ChClient(url=config.CLICKHOUSE_URL)
    return connection


async def clickhouse_init_tables() -> None:
    async with aiofiles.open(config.CLICKHOUSE_CREATE_PATH, "r") as file:
        tables_create_query = await file.read()

    connection = await get_connection()
    await connection.execute(tables_create_query)
    await connection.close()


async def insert_to_file_requests(query: str) -> None:
    async with aiofiles.open(config.CLICKHOUSE_PARTITION_REQUESTS_PATH, "a") as file:
        await file.write(query)

    async with aiofiles.open(config.CLICKHOUSE_PARTITION_REQUESTS_PATH, "r") as file:
        rows = await file.readlines()
        if len(rows) < config.CLICKHOUSE_INSERT_SIZE:
            return

    query = "INSERT INTO requests ("
    query += "id, partition_datetime, req_datetime, req_ip, req_url, "
    query += "req_method, req_path_params, req_query_params, "
    query += "req_header_params, req_cookie_params, res_datetime, "
    query += "res_status_code, res_header_params"
    query += ") VALUES \n"
    for row in rows:
        query += row
    connection = await get_connection()
    await connection.execute(query)
    await connection.close()

    async with aiofiles.open(config.CLICKHOUSE_PARTITION_REQUESTS_PATH, "w") as file:
        await file.write("")
