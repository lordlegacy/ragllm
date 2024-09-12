import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    POSTGRES_DB = os.getenv('POSTGRES_DB')
    POSTGRES_USER = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_HOST = os.getenv('POSTGRES_HOST')
    POSTGRES_PORT = os.getenv('POSTGRES_PORT')
