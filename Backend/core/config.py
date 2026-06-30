# BaseSettings is a special Pydantic class that loads configuration values from:
# Environment variables (OS)
# .env file (if configured) and validates their data types.

from pydantic_settings import BaseSettings, SettingsConfigDict

# Centralized application settings loaded from .env
class Settings(BaseSettings):

    DATABASE_URL: str                 # PostgreSQL connection string
    SECRET_KEY: str                   # JWT signing key
    ALGORITHM: str                    # JWT algorithm (e.g. HS256)
    ACCESS_TOKEN_EXPIRE_TIME: int     # Token expiry in minutes

    # Configure how BaseSettings loads values
    model_config = SettingsConfigDict(
        env_file=".env",              # Load variables from .env
        extra="ignore"                # Ignore undeclared variables
    )

# Create a single settings object for the whole project
settings = Settings()