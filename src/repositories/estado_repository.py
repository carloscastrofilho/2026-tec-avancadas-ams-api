from src.databases.connection import Database
from src.models.estados_model import Estado
from typing import List, Optional

class EstadoRepository:
    def __init__(self):
        self.db = Database()

    def get_all(self) -> List[Estado]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id, estado, uf FROM estados")
            rows = cursor.fetchall()
            cursor.close()
            return [Estado.from_dict(row) for row in rows]

    def get_by_id(self, id_estado: int) -> Optional[Estado]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id, estado, uf FROM estados WHERE id = %s", (id_estado,))
            row = cursor.fetchone()
            cursor.close()
            return Estado.from_dict(row) if row else None

    def create(self, estado: Estado) -> int:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            query = "INSERT INTO estados (estado, uf) VALUES (%s, %s)"
            cursor.execute(query, (estado.estado, estado.uf))
            conn.commit()
            new_id = cursor.lastrowid
            cursor.close()
            return new_id

    def update(self, id_estado: int, estado: Estado) -> bool:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            query = "UPDATE estados SET estado = %s, uf = %s WHERE id = %s"
            cursor.execute(query, (estado.estado, estado.uf, id_estado))
            conn.commit()
            affected = cursor.rowcount
            cursor.close()
            return affected > 0

    def delete(self, id_estado: int) -> bool:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM estados WHERE id = %s", (id_estado,))
            conn.commit()
            affected = cursor.rowcount
            cursor.close()
            return affected > 0
