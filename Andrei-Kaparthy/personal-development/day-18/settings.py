import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

class Settings(BaseSettings):
    """
    Application settings.
    Reads configuration from environment variables.
    """
    LLM_API_KEY: str = os.getenv("LLM_API_KEY", "sk-your-openai-api-key-here")
    LLM_MODEL_NAME: str = "gpt-4-turbo-preview"

    class Config:
        # This allows pydantic to look for a .env file
        env_file = ".env"
        env_file_encoding = "utf-8"

# Instantiate the settings
settings = Settings()