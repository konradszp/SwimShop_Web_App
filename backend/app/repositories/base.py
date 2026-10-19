from app.database import get_connection

class BaseRepository:
    def execute_query(self, query: str, params: tuple = ()) -> list[dict]:
        conn = get_connection()

        if not conn:
            return []
        
        cursor = conn.cursor(dictionary=True)
        
        try:
            cursor.execute(query, params or ())
            result = cursor.fetchall()
            if result != None:
                return result
            else:
                return []

        finally:
            cursor.close()
            conn.close()

    def execute_statement(self, query: str, params: tuple = ()) -> bool:
        conn = get_connection()

        if not conn:
            return False
        
        cursor = conn.cursor()

        try:
            cursor.execute(query, params or ())
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(f"Database error: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    def execute_insert(self, query: str, params: tuple = ()) -> int | None:
        conn = get_connection()
        if not conn:
            return None

        cursor = conn.cursor()
        try:
            cursor.execute(query, params or ())
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            print(f"Database error: {e}")
            return None
        finally:
            cursor.close()
            conn.close()