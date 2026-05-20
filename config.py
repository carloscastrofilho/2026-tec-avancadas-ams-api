import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'chave_fraca')
    TOKEN_LIFETIME_MINUTES = int(os.getenv('TOKEN_LIFETIME_MINUTES', 30))
    DB_CONFIG = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'user': os.getenv('DB_USER', 'root'),
        'port': int(os.getenv('DB_PORT', 3306)),
        'password': os.getenv('DB_PASSWORD', ''),
        'database': os.getenv('DB_NAME', 'fatecteste')
    }
    
    PORT_API = int(os.getenv('PORT_API', 3000))

    EMPRESA_NAME = "FATEC TAQUARITINGA"
