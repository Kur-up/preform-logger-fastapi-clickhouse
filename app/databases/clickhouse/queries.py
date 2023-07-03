import uuid

from fastapi import Request
from fastapi import Response

from .core import insert_to_file_requests
from .dependencies import generate_json_string


async def clickhouse_add_request(
    request: Request, response: Response, res_datetime: str
):
    req_path_params = await generate_json_string(request.path_params)
    req_query_params = await generate_json_string(request.query_params)
    req_header_params = await generate_json_string(request.headers)
    req_cookie_params = await generate_json_string(request.cookies)
    res_header_params = await generate_json_string(response.headers)

    res_status_code = str(response.status_code).replace("'", "\\'")

    req_id = str(request.state.id).replace("'", "\\'")
    req_url = str(request.url).replace("'", "\\'")
    req_ip = str(request.client.host).replace("'", "\\'")
    req_method = str(request.method).replace("'", "\\'")

    query = f"('{req_id}', toDateTime('{request.state.datetime}'), "
    query += f"toDateTime('{request.state.datetime}'), '{req_ip}',  '{req_url}', "
    query += f"'{req_method}', {req_path_params}, {req_query_params}, "
    query += f"{req_header_params}, {req_cookie_params}, "
    query += f"toDateTime('{res_datetime}'), '{res_status_code}', "
    query += f"{res_header_params}"
    query += "),\n"
    await insert_to_file_requests(query)
