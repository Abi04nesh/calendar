import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///events.db'  # You can use PostgreSQL/MySQL for production
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)
