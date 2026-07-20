from pydantic import computed_field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SUPABASE_URL: str
    SUPABASE_ANON_KEY: str
    PSQL_HOST: str = "localhost"
    PSQL_USER: str = "postgres"
    PSQL_PASS: str = "postgres"
    PSQL_DB_NAME: str = "dbm_nca_ph"
    PIPELINE_API_KEY: str

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.PSQL_USER}:{self.PSQL_PASS}@{self.PSQL_HOST}:5432/{self.PSQL_DB_NAME}"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()  # pyright:  ignore
