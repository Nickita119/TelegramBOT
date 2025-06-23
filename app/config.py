import os
from dotenv import load_dotenv

load_dotenv()  # Загружает переменные из .env в окружение

TOKEN = os.getenv("TOKEN")
