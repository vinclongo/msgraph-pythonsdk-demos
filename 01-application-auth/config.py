import os
from dotenv import load_dotenv

# Load .env file from current directory
load_dotenv()

class Config:
    """Application configuration for Microsoft Graph."""

    # Read values from environment variables 
    CLIENT_ID = os.getenv('CLIENT_ID')
    TENANT_ID = os.getenv('TENANT_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')

    @classmethod
    def validate(cls):
        """Validate that required configuration exists."""
        if not cls.CLIENT_ID:
            raise ValueError("CLIENT_ID not set in .env file")
        if not cls.TENANT_ID:
            raise ValueError("TENANT_ID not set in .env file")
        if not cls.CLIENT_SECRET:
            raise ValueError("CLIENT_SECRET not set in .env file")