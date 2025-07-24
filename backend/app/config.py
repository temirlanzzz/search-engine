from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    # Database Configuration
    database_url: str = "postgresql://user:password@localhost:5432/search_engine"
    redis_url: str = "redis://localhost:6379/0"
    
    # Application Configuration
    debug: bool = False
    environment: str = "development"
    secret_key: str = "your-secret-key-here"
    allowed_hosts: str = "localhost,127.0.0.1"
    
    @property
    def allowed_hosts_list(self) -> List[str]:
        """Convert comma-separated allowed hosts to list"""
        return [host.strip() for host in self.allowed_hosts.split(",")]
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    cors_origins: str = "http://localhost:3000,http://localhost:5173"
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Convert comma-separated CORS origins to list"""
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    # Celery Configuration
    celery_broker_url: str = "redis://localhost:6379/0"
    celery_result_backend: str = "redis://localhost:6379/1"
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "json"
    
    # Crawler Configuration
    crawler_delay: int = 1
    crawler_timeout: int = 30
    max_pages_per_site: int = 100
    
    # Data Storage
    data_dir: str = "/app/data"
    index_dir: str = "/app/index"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings() 