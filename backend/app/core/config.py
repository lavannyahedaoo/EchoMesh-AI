from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", "../.env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    APP_NAME: str = "EchoMesh AI"
    APP_ENV: str = "local"
    DEBUG: bool = True

    # Security
    JWT_SECRET: str = "fallback_secret_key_for_local_only"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    # CockroachDB
    COCKROACH_HOST: str = "localhost"
    COCKROACH_PORT: int = 26257
    COCKROACH_USER: str = "root"
    COCKROACH_PASSWORD: str = ""
    COCKROACH_DB: str = "echomesh_dev"
    DATABASE_URL: str = "postgresql+psycopg://root@localhost:26257/echomesh_dev"

    @property
    def SQLALCHEMY_DATABASE_URL(self) -> str:
        url = self.DATABASE_URL
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "cockroachdb+psycopg://", 1)
        elif url.startswith("postgresql://"):
            url = url.replace("postgresql://", "cockroachdb+psycopg://", 1)
        elif url.startswith("postgresql+psycopg://"):
            url = url.replace("postgresql+psycopg://", "cockroachdb+psycopg://", 1)
        return url

    # AWS configuration stubs
    AWS_REGION: str = "us-east-1"
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_S3_BUCKET_NAME: str = "echomesh-memories-dev"

    # Bedrock Models
    BEDROCK_REASONING_MODEL: str = "anthropic.claude-3-5-sonnet-20240620-v1:0"
    BEDROCK_EMBEDDING_MODEL: str = "amazon.titan-embed-text-v2:0"

settings = Settings()
