from pydantic_settings import BaseSettings, SettingsConfigDict

class _Settings(BaseSettings):
    db_username: str = 'postgres'
    db_password: str = 'postgres'
    db_ip: str = 'localhost'
    db_port: str = '5432'
    db_name: str = 'postgres'
    model_config = SettingsConfigDict(env_file='.env')

settings = _Settings()