import sqlite3

class DBConnection:
    def __init__(self, db_nombre = 'database.db'):
        self.db_nombre = db_nombre
        self.conn = None
        self.cursor = None

    def __enter__(self):
        try:
            self.conn = sqlite3.connect(self.db_nombre)
            self.conn.execute("PRAGMA foreign_keys = ON;")
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()
            print(f"[DBConnection] Conexion a '{self.db_nombre}' establecida")
            return self
        except sqlite3.Error as e:
            print(f"[DBConnection ERROR] Error al conectar a la base de datos '{self.db_nombre}': {e}")
            raise

    def __exit__(self, exc_type, exc_val,exc_tb):
        if self.conn:
            if exc_type:
                self.conn.rollback()
                print("[DBConnection] Transaccion revertida por un error.")
            else:
                self.conn.commit()
                print("[DBConnection] Transacion confirmada.")
                self.conn.close()
                print("[DBConnection] Conexion a la base de datos cerrada.")