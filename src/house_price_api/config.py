from pydantic import BaseModel
import os

class Settings(BaseModel):
    model_version: str = os.getenv("MODEL_VERSION", "v1")
    artifacts_dir: str = os.getenv("ARTIFACTS_DIR", "artifacts")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()
