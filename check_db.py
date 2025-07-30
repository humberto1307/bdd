import sqlite3

def check_database():
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        
        # Obtener todas las tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print("Tablas encontradas:")
        for table in tables:
            print(f"- {table[0]}")
            
        # Verificar tabla ubicacion_almacen específicamente
        cursor.execute("PRAGMA table_info(ubicacion_almacen);")
        columns = cursor.fetchall()
        
        print("\nEstructura de tabla ubicacion_almacen:")
        for col in columns:
            print(f"- {col[1]} ({col[2]})")
            
        # Verificar si hay datos
        cursor.execute("SELECT COUNT(*) FROM ubicacion_almacen;")
        count = cursor.fetchone()[0]
        print(f"\nRegistros en ubicacion_almacen: {count}")
        
        if count > 0:
            cursor.execute("SELECT * FROM ubicacion_almacen LIMIT 3;")
            rows = cursor.fetchall()
            print("Primeros registros:")
            for row in rows:
                print(f"- {row}")
        
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_database() 