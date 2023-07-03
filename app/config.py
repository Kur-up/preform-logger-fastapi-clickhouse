from pydantic import BaseSettings
from pydantic import Field


class Config(BaseSettings):
    DEBUG: bool = Field(
        default=True,
        env="DEBUG",
    )

    CLICKHOUSE_URL: str = Field(
        default="clickhouse://cscore:cscore@localhost:18123/cscore_db",
        env="CLICKHOUSE_URL",
    )
    CLICKHOUSE_INSERT_SIZE: int = Field(default=5, env="CLICKHOUSE_INSERT_SIZE")
    CLICKHOUSE_CREATE_PATH: str = Field(
        default="./app/databases/clickhouse/tables.sql", env="CLICKHOUSE_CREATE_PATH"
    )
    CLICKHOUSE_PARTITION_REQUESTS_PATH: str = Field(
        default="./app/databases/clickhouse/partitions/requests.txt",
        env="CLICKHOUSE_PARTITION_REQUESTS_PATH",
    )


config = Config()
