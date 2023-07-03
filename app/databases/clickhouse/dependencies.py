async def generate_json_string(params):
    result = "{"
    for key in params.keys():
        result += "'" + str(key).replace("'", "\\'") + "': "
        result += "'" + str(params.get(key)).replace("'", "\\'") + "', "
    result += "}"
    return result
