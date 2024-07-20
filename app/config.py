import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENAI_API_KEY: str = os.getenv('OPENAI_API_KEY')
    ALLOWED_DEGREES = {'excellent', 'average', 'good'}

settings = Settings()
