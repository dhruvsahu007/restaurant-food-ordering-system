from pydantic import BaseSettings

class Settings(BaseSettings):
    # Application settings
    APP_NAME: str = "Restaurant Food Ordering System"
    APP_VERSION: str = "1.0.0"
    DATABASE_URL: str = "sqlite:///./test.db"  # Example for SQLite, change as needed

    class Config:
        env_file = ".env"

settings = Settings()