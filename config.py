import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    db_path: str = os.getenv("DB_PATH", "data.db")
    host: str = os.getenv("API_HOST", "0.0.0.0")
    port: int = int(os.getenv("API_PORT", "2006"))
    api_token: str = os.getenv("API_TOKEN", "")
    api_url: str = os.getenv("API_URL", "http://localhost:2006/api/measurements")
    ping_target: str = os.getenv("PING_TARGET", "google.com")


settings = Settings()
