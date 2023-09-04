import aiofiles
import aiochclient
import asyncio

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


async def execute_requests(ch_queue) -> None:
    if ch_queue.empty():
        print("EMPTY")
        return

    data_list = []
    while not ch_queue.empty():
        item = ch_queue.get()
        data_list.append(item)

    query = "INSERT INTO requests ("
    query += "id, partition_datetime, req_body"
    query += ") VALUES "
    query = "INSERT INTO requests ("
    query += "id, "
    query += "partition_datetime, "
    query += "req_datetime, "
    query += "req_ip, "
    query += "req_method, "
    query += "req_url, "
    query += "req_path, "
    query += "req_query, "
    query += "req_body, "
    query += "req_headers, "
    query += "req_cookies, "
    query += "res_datetime, "
    query += "res_code, "
    query += "res_body, "
    query += "res_headers"
    query += ") VALUES "
    for data in data_list:
        row = "("
        row += f"'{data['id']}', "
        row += f"toDateTime('{data['partition_datetime']}'), "
        row += f"toDateTime('{data['req_datetime']}'), "
        row += f"'{data['req_ip']}', "
        row += f"'{data['req_method']}', "
        row += f"'{data['req_url']}', "
        row += f"'{data['req_path']}', "
        row += f"'{data['req_query']}', "
        row += f"'{data['req_body']}', "
        row += f"'{data['req_headers']}', "
        row += f"'{data['req_cookies']}', "
        row += f"toDateTime('{data['res_datetime']}'), "
        row += f"'{data['res_code']}', "
        row += f"'{data['res_body']}', "
        row += f"'{data['res_headers']}'"
        row += "), "
        query += row
    connection = await get_connection()
    await connection.execute(query)
    await connection.close()
