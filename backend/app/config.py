import os

class Config:
    SECRET_KEY = "dev-secret"
    JWT_SECRET_KEY = "jwt-secret"
    SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

