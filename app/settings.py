from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_token: str = ""  # API token for authentication
    rate_limit: int = 10  # Example rate limit, adjust as needed
    rate_period: int = 60  # Rate limit period in seconds


# Lazily initialize Settings instance and expose as variable
class _SettingsSingleton:
    _instance = None

    def __getattr__(self, name):
        if self._instance is None:
            self._instance = Settings()
        return getattr(self._instance, name)


settings = _SettingsSingleton()
