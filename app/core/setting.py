from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel

class ServerConfig(BaseModel):
    port: int
    host: str
    is_reload: bool
    
class JWTConfig(BaseModel):
    access_secret_key: str
    refresh_secret_key: str
    access_token_expire: str
    refresh_token_expire: str
    algorithm: str


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )

    server: ServerConfig
    jwt: JWTConfig



settings = AppSettings()