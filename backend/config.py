import logging
from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Creates default setting for app, to be used in production
    Overwritten by .env file if exists
    """
    # App settings
    app_name: str = "Audio Transcription App"
    version: str = "1.0.0"
    environment:str = "development"
    
    # Whisper model settings
    whisper_model: str = "base"
    
    # File settings
    max_file_size: int = 2_000_000_000 # 2GB max audio file size
    allowed_extensions: list = [".mp3", ".mp4"]
    data_dir: str = "user_recordings"
    
    # Database
    database_url: str = "sqlite:///./app.db"
    
    # Logging
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        
settings = Settings()

# Setup logging
logging.basicConfig(
    filename ="app.log",
    level = getattr(logging, settings.log_level),
    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)