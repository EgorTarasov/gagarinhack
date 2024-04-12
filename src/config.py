from pydantic import Field, EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    api_prefix: str = "/api"
    app_name: str = "FastAPI App"
    app_host: str = "http://localhost"
    app_port: int = 8000
    app_desc: str = "FastAPI App Description"
    app_version: str = "0.1.0"
    debug: bool = False

    max_upload_size: int = 5 * 1024 * 1024  # 5MB

    postgres_host: str
    postgres_port: int = 5432
    postgres_db: str
    postgres_user: str
    postgres_password: str

    # celery settings
    rabbitmq_default_user: str
    rabbitmq_default_pass: str
    rabbitmq_host: str = "localhost"
    rabbitmq_port: int = 5672

    # email settings
    mail_user: EmailStr
    mail_password: str
    mail_host: str
    mail_port: int

    # redis settings
    redis_host: str
    redis_port: int = 6379
    redis_password: str

    # telegram settings
    telegram_token: str = ""

    # minio s3 settings
    s3_endpoint: str = "localhost:9000"
    aws_access_key_id: str
    aws_secret_access_key: str

    @property
    def build_postgres_dsn(self) -> str:
        res = (
            "postgresql://"
            f"{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )
        return res

    @property
    def rabbitmq_url(self) -> str:
        url = f"amqp://{self.rabbitmq_default_user}:{self.rabbitmq_default_pass}@{self.rabbitmq_host}:{self.rabbitmq_port}"
        print(url)
        return url


cfg = Config()  # type: ignore
