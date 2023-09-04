CREATE TABLE IF NOT EXISTS requests
(
    id String,
    partition_datetime DateTime,
    req_datetime DateTime,
    req_ip String,
    req_method String,
    req_url String,
    req_path String,
    req_query String,
    req_body String,
    req_headers String,
    req_cookies String,
    res_datetime DateTime,
    res_code String,
    res_body String,
    res_headers String
)
ENGINE = MergeTree()
PARTITION BY toYYYYMMDD(partition_datetime)
ORDER BY partition_datetime