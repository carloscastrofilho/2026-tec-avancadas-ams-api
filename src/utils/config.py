import os
from dotenv import load_dotenv

class Config:
    
    load_dotenv()
    
    APP_NAME = os.getenv("APP_NAME")
    APP_PORT = int(os.getenv("APP_PORT", 3000))
    APP_DEBUG = os.getenv("APP_DEBUG") == "True"   
     
    DB_TYPE =  "mysql"
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT", 3306)
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")

    JWT_SECRET = os.getenv("JWT_SECRET",'chave_padrao_teste')
    TOKEN_LIFETIME_MINUTES = int(os.getenv('TOKEN_LIFETIME_MINUTES', 30))
    
    @staticmethod
    def database_url():
        return (
            f"mysql://{Config.DB_USER}:"
            f"{Config.DB_PASSWORD}@"
            f"{Config.DB_HOST}:"
            f"{Config.DB_PORT}/"
            f"{Config.DB_NAME}"
        )
    
