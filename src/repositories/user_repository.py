from src.databases.connection import Database
from src.models.user_model import User
from typing import List, Optional

class UserRepository:
    def __init__(self):
        self.db = Database
        self.tableName = "users"
    
    def get_all(self) -> List[User]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            query = f"SELECT * FROM {self.tableName}" 
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            return [User.from_dict(row) for row in rows]
        
    def get_by_id(self, id: int) -> Optional[User]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            query = f"SELECT * FROM {self.tableName} WHERE id = %s"
            cursor.execute( query, (id,))
            row = cursor.fetchone()
            cursor.close()
            return User.from_dict(row) if row else None
        
    def create(self, user: User) -> int:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            query = f"INSERT INTO {self.tableName} (namefull, login, password, idrolle) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (user.namefull, user.login, user.password, user.idroller))
            conn.commit()
            new_id = cursor.lastrowid
            cursor.close()
            return new_id
        
    def update(self, id: int, user: User) -> bool:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            query = f"UPDATE {self.tableName} SET namefull = %s, login = %s , password = %s , idrolle = %s WHERE id = %s"
            cursor.execute(query, (user.namefull, user.login, user.password, user.idroller, id))
            conn.commit()
            affected = cursor.rowcount
            cursor.close()
            return affected > 0        

    def delete(self, id: int) -> bool:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            query = f"DELETE FROM {self.tableName} WHERE id = %s"
            cursor.execute(query, ( id,))
            conn.commit()
            affected = cursor.rowcount
            cursor.close()
            return affected > 0