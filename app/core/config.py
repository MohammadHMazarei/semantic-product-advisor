from pydantic_settings import BaseSettings
from functools import lru_cache
from pathlib import Path
from typing import Optional


class Settings(BaseSettings):
    API_TITLE: str
    API_VERSION: str
    API_PREFIX: str
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    CHROMA_PERSIST_DIR: str
    COLLECTION_NAME: str

    EMBEDDING_MODEL_NAME: str

    DATA_ROOT_DIR: str
    PRODUCTS_JSON_FILENAME: str

    DEFAULT_SEARCH_TOP_K: int = 5
    MAX_SEARCH_TOP_K: int = 20
    MIN_RELEVANCE_SCORE: float = 0.3

    LOG_LEVEL: str = "INFO"

    @property
    def products_json_path(self) -> Path:
        """Full path to products JSON file"""
        return Path(self.DATA_ROOT_DIR) / self.PRODUCTS_JSON_FILENAME

    @property
    def chroma_persist_path(self) -> Path:
        """Full path to ChromaDB persistence directory"""
        return Path(self.CHROMA_PERSIST_DIR)

    def validate_paths(self) -> None:
        """Validate that required paths exist"""
        # Create directories if they don't exist
        self.chroma_persist_path.mkdir(parents=True, exist_ok=True)
        Path(self.DATA_ROOT_DIR).mkdir(parents=True, exist_ok=True)

        # Check if products file exists
        if not self.products_json_path.exists():
            raise FileNotFoundError(
                f"Products JSON file not found at: {self.products_json_path}"
            )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"  # Ignore extra fields in .env


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance
    This ensures settings are loaded only once
    """
    settings = Settings()
    settings.validate_paths()
    return settings
