import sqlite3

def inspect_database(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Obtener todas las tablas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    print(f"Tablas en la base de datos '{db_path}':\n")
    for (table_name,) in tables:
        print(f"Tabla: {table_name}")

        # Obtener información de columnas (incluye PK)
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        print("Columnas:")
        for col in columns:
            # col es una tupla: (cid, name, type, notnull, dflt_value, pk)
            cid, name, col_type, notnull, dflt_value, pk = col
            pk_str = "PRIMARY KEY" if pk else ""
            notnull_str = "NOT NULL" if notnull else ""
            default_str = f"Default: {dflt_value}" if dflt_value else ""
            print(f"  - {name} ({col_type}) {notnull_str} {pk_str} {default_str}".strip())

        # Obtener claves foráneas (FK)
        cursor.execute(f"PRAGMA foreign_key_list({table_name});")
        foreign_keys = cursor.fetchall()
        if foreign_keys:
            print("\nClaves Foráneas (FK):")
            for fk in foreign_keys:
                # fk es una tupla: (id, seq, table, from, to, on_update, on_delete, match)
                fk_id, seq, ref_table, from_col, to_col, on_update, on_delete, match = fk
                print(f"  - ID: {fk_id}, From: {from_col} -- To: {ref_table}.{to_col}")
                print(f"    On Update: {on_update}, On Delete: {on_delete}, Match: {match}")
        else:
            print("\nClaves Foráneas (FK): Ninguna")

        print("-" * 40)

    conn.close()

if __name__ == "__main__":
    db_path = "database.db"  # Cambia si tu archivo tiene otro nombre o ruta
    inspect_database(db_path)
