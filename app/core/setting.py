from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel

class ServerConfig(BaseModel):
    port: int
    host: str
    is_reload: bool
    

class AppSettings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=('.env'),
        
    ) 

    server: ServerConfig
