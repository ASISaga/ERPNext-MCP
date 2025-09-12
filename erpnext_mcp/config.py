"""Configuration management for ERPNext MCP Server."""

from pydantic_settings import BaseSettings
from typing import Optional
import os


class ERPNextConfig(BaseSettings):
    """Configuration for ERPNext connection."""
    
    # ERPNext connection settings
    erpnext_url: str = "http://localhost:8000"
    erpnext_username: Optional[str] = None
    erpnext_password: Optional[str] = None
    erpnext_api_key: Optional[str] = None
    erpnext_api_secret: Optional[str] = None
    
    # SSL verification
    verify_ssl: bool = True
    
    # MCP Server settings
    server_host: str = "localhost"
    server_port: int = 8080
    server_name: str = "ERPNext MCP Server"
    server_version: str = "0.1.0"
    
    # Logging
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        env_prefix = "ERPNEXT_"


# Global config instance
config = ERPNextConfig()