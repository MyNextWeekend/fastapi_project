import os.path
from pathlib import Path, PosixPath

from pydantic import PostgresDsn, computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        # 配置文件位置，取决于在什么位置启动服务
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )
    # 项目的根目录
    root_dir: PosixPath = Path(__file__).resolve().parent.parent
    # 日志文件位置
    log_file: str = os.path.join(root_dir, "logs", "system.log")

    # 数据库配置
    db_host: str
    db_port: int
    db_name: str
    db_password: str
    db_database: str

    @computed_field  # type: ignore[prop-decorator]
    @property
    def sqlmodel_database_uri(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="mysql+pymysql",
            username=self.db_name,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
            path=self.db_database,
        )

    # redis配置
    redis_host: str
    redis_port: int
    redis_password: str


settings = Settings()