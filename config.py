import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-secret-key')  # Ensures app runs even if .env fails
    SQLALCHEMY_DATABASE_URI = 'sqlite:///fleet.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

print("SECRET_KEY loaded:", Config.SECRET_KEY)  # Debugging print

