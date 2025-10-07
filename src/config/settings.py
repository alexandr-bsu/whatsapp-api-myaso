from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    id_instance: str = "YOUR_GREENAPI_ID_INSTANCE"
    api_token_instance: str = "YOUR_GREENAPI_API_TOKEN_INSTANCE"
    api_url: str = "https://api.green-api.com"
    media_url: str = "https://1103.media.green-api.com"

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

settings = Settings() 