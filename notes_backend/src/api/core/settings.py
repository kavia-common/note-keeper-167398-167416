import os
from typing import List


class AppSettings:
    """Application settings loaded from environment variables."""

    def __init__(self) -> None:
        # In a real environment, these would be provided in .env
        self.environment = os.getenv("ENVIRONMENT", "development")
        self.cors_allow_origins: List[str] = (
            os.getenv("CORS_ALLOW_ORIGINS", "*").split(",")
            if os.getenv("CORS_ALLOW_ORIGINS")
            else ["*"]
        )
        # Placeholder DB configuration to integrate with 'notes_database' container
        # Do not hardcode secrets; these are examples of expected env keys.
        self.db_url = os.getenv("NOTES_DB_URL", "")
        self.db_user = os.getenv("NOTES_DB_USER", "")
        self.db_password = os.getenv("NOTES_DB_PASSWORD", "")
        self.db_name = os.getenv("NOTES_DB_NAME", "")
        self.db_port = os.getenv("NOTES_DB_PORT", "")

    @property
    def is_production(self) -> bool:
        return self.environment.lower() == "production"


_settings_instance: AppSettings | None = None


# PUBLIC_INTERFACE
def get_app_settings() -> AppSettings:
    """Return a cached instance of application settings."""
    global _settings_instance
    if _settings_instance is None:
        _settings_instance = AppSettings()
    return _settings_instance
