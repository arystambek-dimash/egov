from configparser import ConfigParser
from pydantic_settings import BaseSettings, SettingsConfigDict


def config(filename="../database.ini", section="postgresql"):
    parser = ConfigParser()
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section is not found')

    return db


class JWTConfig(BaseSettings):
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # 30 minutes
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    ALGORITHM: str = "HS256"
    JWT_SECRET_KEY: str = "egov"
    JWT_REFRESH_SECRET_KEY: str = "egovegov"

    # model_config = SettingsConfigDict(env_file="../.env")


class Config(JWTConfig):
    """Application configuration settings."""


env = Config()
