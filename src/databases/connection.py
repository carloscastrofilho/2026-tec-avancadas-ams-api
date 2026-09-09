import mysql.connector.pooling
from contextlib import contextmanager
from src.utils.config import Config

class Database:
    # private
    _instance = None
    _pool = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._init_pool()
        return cls._instance

    def _init_pool(self):
        self._pool = mysql.connector.pooling.MySQLConnectionPool(
            pool_name="mypool",
            pool_size=5,
            pool_reset_session=True,
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )

    @contextmanager
    def get_connection(self):
        """Context Manager para obter e devolver conexoes do pool com seguranca."""
        connection = self._pool.get_connection()
        try:
            yield connection
        finally:
            connection.close()  # Retorna a conexao para o pool