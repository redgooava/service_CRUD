"""
Подключение переменных окружения
"""

from dotenv import load_dotenv
import os


load_dotenv()

DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5433')
DB_NAME = os.getenv('DB_NAME', 'postgres')

API_URL = os.getenv('API_URL', 'http://localhost:8000')
