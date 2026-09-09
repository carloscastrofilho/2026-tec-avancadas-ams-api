from src.databases.connection import Database
from src.models.roler_users_model import Roller
from typing import List, Optional

class RollerRepository:
    def __init__(self):
          self.db = Database
          self.tableName = "rollers"
      
    def get_all(self) -> List[Roller]:
          with self.db.get_connection() as conn:
              cursor = conn.cursor(dictionary=True)
              query = f"SELECT * FROM {self.tableName}" 
              cursor.execute(query)
              rows = cursor.fetchall()
              cursor.close()
              return [Roller.from_dict(row) for row in rows]
          
    def get_by_id(self, id: int) -> Optional[Roller]:
          with self.db.get_connection() as conn:
              cursor = conn.cursor(dictionary=True)
              query = f"SELECT * FROM {self.tableName} WHERE id = %s"
              cursor.execute( query, (id,))
              row = cursor.fetchone()
              cursor.close()
              return Roller.from_dict(row) if row else None
          
    def create(self, Roller: Roller) -> int:
          with self.db.get_connection() as conn:
              cursor = conn.cursor()
              query = f"INSERT INTO {self.tableName} (roller) VALUES (%s)"
              cursor.execute(query, (Roller.roller))
              conn.commit()
              new_id = cursor.lastrowid
              cursor.close()
              return new_id
          
    def update(self, id: int, Roller: Roller) -> bool:
          with self.db.get_connection() as conn:
              cursor = conn.cursor()
              query = f"UPDATE {self.tableName} SET roller = %s WHERE id = %s"
              cursor.execute(query, (Roller.roller,  id))
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