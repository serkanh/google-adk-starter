import os

# Database configuration
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "agent_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

# Construct the database URL
DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# API Keys (add your required keys here)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
# Add more API keys as needed:
# ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# Application settings
APP_NAME = "my_agent"  # TODO: Change this to your agent's name
DEFAULT_USER_ID = "default_user"

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")