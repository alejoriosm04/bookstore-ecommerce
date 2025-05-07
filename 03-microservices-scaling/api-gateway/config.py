import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    AUTH_SERVICE_URL = os.getenv('AUTH_SERVICE_URL')
    CATALOG_SERVICE_URL = os.getenv('CATALOG_SERVICE_URL')
    ORDER_SERVICE_URL = os.getenv('ORDER_SERVICE_URL')
    JWT_SECRET = os.getenv('JWT_SECRET')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')