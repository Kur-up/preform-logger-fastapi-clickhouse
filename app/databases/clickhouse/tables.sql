CREATE TABLE IF NOT EXISTS requests
(
    id String,
    partition_datetime DateTime,
    req_datetime DateTime,
    req_ip IPv4,
    req_url String,
    req_method String,
    req_path_params Map(String, String),
    req_query_params Map(String, String),
    req_header_params Map(String, String),
    req_cookie_params Map(String, String),
    res_datetime DateTime,
    res_status_code String,
    res_header_params Map(String, String)
)
ENGINE = MergeTree()
PARTITION BY toYYYYMM(partition_datetime)
ORDER BY partition_datetime

