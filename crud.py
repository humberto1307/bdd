import sqlite3
from db_connection import DBConnection
from datetime import datetime  
from typing import List, Dict, Optional 



class Manejador_unidad_medida():
    def __init__(self, db_connection: DBConnection):
         self.db_connection = db_connection
        
    def mostrar_todas_unidades(self):
        print("\n--- Unidades de Medida Actuales ---")
        try:
            with self.db_connection as db:
                db.cursor.execute("SELECT id_unidad_medida, nombre_unidad_medida, abreviatura FROM unidad_medida ORDER BY nombre_unidad_medida")
                unidades = db.cursor.fetchall()
                if unidades:
                    for unidad in unidades:
                        print(f"ID: {unidad['id_unidad_medida']}, Nombre: {unidad['nombre_unidad_medida']}, Abreviatura: {unidad['abreviatura']}")
                else:
                    print("No hay unidades de medida registradas.")
        except Exception as e:
            print(f"[MOSTRAR ERROR] Error al mostrar unidades de medida: {e}")
   
    def crear_unidad_medida(self, nombre: str, abreviatura: str):
        try:
            with self.db_connection as db:
                db.cursor.execute("INSERT INTO unidad_medida (nombre_unidad_medida, abreviatura) VALUES (?, ?)", (nombre, abreviatura))
                nuevo_id = db.cursor.lastrowid
                print(f"Unidad de medida {nombre} (ID: {nuevo_id}) creada exitosamente.")
            self.mostrar_todas_unidades()
            return nuevo_id
        except sqlite3.IntegrityError as e:
             if "UNIQUE constraint failed: unidad_medida.abreviatura" in str(e):
                 print(f"Error: La abreviatura {abreviatura} ya existe. No se pudo crear {nombre}.")
             elif "UNIQUE constraint failed: unidad_medida.nombre_unidad_medida" in str(e):
                 print(f"El nombre '{nombre}' ya existe. No se pudo crear.")
             else:
                 print(f"Error de integridad al crear unidad de medida: {e}")
                 return None
        except Exception as e:
             print(f"Error inesperado al crear unidad de medida: {e}")
             return None

    def leer_unidades_medida(self) -> List[Dict]:
        try:
             with self.db_connection as db:
                 db.cursor.execute("SELECT * FROM unidad_medida")
                 return [dict(row) for row in db.cursor.fetchall()]
        except Exception as e:
            print(f'Error al leer todas las unidades de medida: {e}')
            return []
        
    def leer_unidades_medida_id(self, id_unidad: int) -> Optional[Dict]:
        try:
             with self.db_connection as db:
                 db.cursor.execute("SELECT id_unidad_medida, nombre_unidad_medida, abreviatura FROM unidad_medida WHERE id_unidad_medida = ?", (id_unidad,))
                 row = db.cursor.fetchone()
                 return dict(row) if row else None
        except Exception as e:
             print(f"Error al leer unidad de medida por ID {id_unidad}: {e}")
             return None
        
    def leer_unidades_medida_nombre(self, nombre: str) -> Optional[Dict]:
        try:
             with self.db_connection as db:
                 db.cursor.execute("SELECT id_unidad_medida, nombre_unidad_medida, abreviatura FROM unidad_medida WHERE nombre_unidad_medida = ?", (nombre,))
                 row = db.cursor.fetchone()
                 return dict(row) if row else None
        except Exception as e:
             print(f"Error al leer unidad de medida por nombre {nombre}: {e}")
             return None
        
    def leer_unidades_medida_abreviatura(self, abreviatura: str) -> Optional[Dict]:
        try:
             with self.db_connection as db:
                 db.cursor.execute("SELECT id_unidad_medida, nombre_unidad_medida, abreviatura FROM unidad_medida WHERE abreviatura = ?", (abreviatura,))
                 row = db.cursor.fetchone()
                 return dict(row) if row else None
        except Exception as e:
             print(f"Error al leer unidad de medida por abreviatura {abreviatura}: {e}")
             return None
        
             
    def actualizar_unidad_medida(self, identificador, tipo_identificador: str = 'id', nuevo_nombre: str = None, nueva_abreviatura: str = None) -> bool:
        if not (nuevo_nombre or nueva_abreviatura):
            print("Se debe proporcionar al menos un nuevo nombre o una nueva abreviatura.")
            return False
        if tipo_identificador not in ['id','nombre','abreviatura']:
            print(f"Tipo de identificador '{tipo_identificador}' no valido. Use 'id','nombre' o 'abreviatura'.")
            return False
        try:
            with self.db_connection as db:
                set_clauses = []
                params = []

                if nuevo_nombre:
                    set_clauses.append("nombre_unidad_medida = ?")
                    params.append(nuevo_nombre)
                if nueva_abreviatura:
                    set_clauses.append("abreviatura = ?")
                    params.append(nueva_abreviatura)

                sql = f"UPDATE unidad_medida SET {', '.join(set_clauses)} WHERE "
                if tipo_identificador == 'id':
                    sql += "id_unidad_medida = ?"
                    params.append(identificador)
                elif tipo_identificador == 'nombre':
                    sql += "nombre_unidad_medida = ?"
                    params.append(identificador)
                elif tipo_identificador == 'abreviatura':
                    sql += "abreviatura = ?"
                    params.append(identificador)

                db.cursor.execute(sql, tuple(params))
                if db.cursor.rowcount > 0:
                    print(f"[ACTUALIZAR] Unidad de medida identificada por '{tipo_identificador}'='{identificador}' actualizada exitosamente.")
                    return True
                else:
                    print(f"[ACTUALIZAR] No se encontró unidad de medida con '{tipo_identificador}'='{identificador}' para actualizar.")
                    return False
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed: unidad_medida.abreviatura" in str(e):
                print(f"[ACTUALIZAR ERROR] La nueva abreviatura '{nueva_abreviatura}' ya existe para otra unidad.")
            elif "UNIQUE constraint failed: unidad_medida.nombre_unidad_medida" in str(e):
                print(f"[ACTUALIZAR ERROR] El nuevo nombre '{nuevo_nombre}' ya existe para otra unidad.")
            else:
                print(f"[ACTUALIZAR ERROR] Error de integridad al actualizar unidad de medida: {e}")
            return False
        except Exception as e:
            print(f"[ACTUALIZAR ERROR] Error inesperado al actualizar unidad de medida: {e}")
            return False
                 

    def eliminar_unidad_medida(self, identificador, tipo_identificador: str = "id") -> bool:
        if tipo_identificador not in ['id', 'nombre', 'abreviatura']:
            print(f"[BORRAR ERROR] Tipo de identificador '{tipo_identificador}' no válido. Use 'id', 'nombre' o 'abreviatura'.")
            return False
        try:
            with self.db_connection as db:
                sql = "DELETE FROM unidad_medida WHERE "
                if tipo_identificador == 'id':
                    sql += "id_unidad_medida = ?"
                elif tipo_identificador == 'nombre':
                    sql += "nombre_unidad_medida = ?"
                elif tipo_identificador == 'abreviatura':
                    sql += "abreviatura = ?"

                db.cursor.execute(sql, (identificador,))

                if db.cursor.rowcount > 0:
                    print(f"[BORRAR] Unidad de medida identificada por '{tipo_identificador}'='{identificador}' eliminada exitosamente.")
                    return True
                else:
                    print(f"[BORRAR] No se encontró unidad de medida con '{tipo_identificador}'='{identificador}' para eliminar.")
                    return False
        except Exception as e:
            print(f"[BORRAR ERROR] Error inesperado al borrar unidad de medida: {e}")
            return False

class Manejador_centros_costos():
    def __init__(self, db_connection: DBConnection):
         self.db_connection = db_connection

    def crear_centro_costos(self, nombre: str, descripcion: str = None, gerente: str = None, activo: int = True) -> Optional[int]:
        try:
            with self.db_connection as db:
                db.cursor.execute("INSERT INTO centro_costos (nombre_centro, descripcion, gerente, activo) VALUES (?, ?, ?, ?)" , (nombre, descripcion, gerente, 1 if activo else 0))
                db.conn.commit()
                nuevo_id = db.cursor.lastrowid
                print(f"[CREAR] Centro de costo '{nombre}' (ID: {nuevo_id}) creado exitosamente.")
            self.mostrar_todos_centros_costos()
            return nuevo_id
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed: centro_costos.nombre_centro" in str(e):
                print(f"[CREAR ERROR] El nombre '{nombre}' ya existe. No se pudo crear el centro de costo.")
            else:
                print(f"[CREAR ERROR] Error de integridad al crear centro de costo: {e}")
            return None
        except Exception as e:
            print(f"[CREAR ERROR] Error inesperado al crear centro de costo: {e}")
            return None
        
    def leer_todos_centros_costo(self, solo_activos: int = False) -> List[Dict]:
        try:
            with self.db_connection as db:
                if solo_activos:
                    db.cursor.execute("SELECT id_centro_costos, nombre_centro, descripcion, " \
                                            "gerente, activo, fecha_creacion FROM centro_costos WHERE activo = 1 ORDER BY nombre_centro")
                else:
                    db.cursor.execute("SELECT id_centro_costos, nombre_centro, descripcion, " \
                                            "gerente, activo, fecha_creacion FROM centro_costos ORDER BY nombre_centro")
                return [dict(row) for row in db.cursor.fetchall()]
        except Exception as e:
            print(f"[LEER ERROR] Error al obtener centros de costo: {e}")
            return []

    def leer_centro_costo_por_id(self, id_centro: int) -> Optional[Dict]:
        try:
            with self.db_connection as db:
                db.cursor.execute("SELECT * FROM centro_costos WHERE id_centro_costos = ?", (id_centro,))
                db.conn.commit()
                row = db.cursor.fetchone()
                return dict(row) if row else None
        except Exception as e:
            print(f"[LEER ERROR] Error al obtener centro de costo por ID {id_centro}: {e}")
            return None

    def leer_centro_costo_por_nombre(self, nombre: str) -> Optional[Dict]:
        try:
            with self.db_connection as db:
                db.cursor.execute("SELECT id_centro_costos, nombre_centro, codigo_centro, descripcion, gerente, activo FROM centro_costos WHERE nombre_centro = ?", (nombre,))
                db.conn.commit()
                row = db.cursor.fetchone()
                return dict(row) if row else None
        except Exception as e:
            print(f"[LEER ERROR] Error al obtener centro de costo por nombre '{nombre}': {e}")
            return None
        
    def actualizar_centro_costo(self, identificador, tipo_identificador: str,
                                nuevo_nombre: str = None, nueva_descripcion: str = None, nuevo_gerente: str = None,
                                nuevo_estado_activo: bool = None) -> bool:
        if not (nuevo_nombre or nueva_descripcion is not None or nuevo_gerente is not None or nuevo_estado_activo is not None):
            print("[ACTUALIZAR ERROR] Se debe proporcionar al menos un campo para actualizar.")
            return False

        if tipo_identificador not in ['id', 'nombre']:
            print(f"[ACTUALIZAR ERROR] Tipo de identificador '{tipo_identificador}' no válido. Use 'id', 'nombre'.")
            return False
        try:
            with self.db_connection as db:
                set_clauses = []
                params = []

                if nuevo_nombre:
                    set_clauses.append("nombre_centro = ?")
                    params.append(nuevo_nombre)
                if nueva_descripcion is not None:
                    set_clauses.append("descripcion = ?")
                    params.append(nueva_descripcion)
                if nuevo_gerente is not None:
                    set_clauses.append("gerente = ?")
                    params.append(nuevo_gerente)
                if nuevo_estado_activo is not None:
                    set_clauses.append("activo = ?")
                    params.append(1 if nuevo_estado_activo else 0)

                sql_update_parts = f"UPDATE centro_costos SET {', '.join(set_clauses)} WHERE "
                db.conn.commit()

                if tipo_identificador == 'id':
                    sql_update_parts += "id_centro_costos = ?"
                elif tipo_identificador == 'nombre':
                    sql_update_parts += "nombre_centro = ?"
                elif tipo_identificador == 'codigo':
                    sql_update_parts += "codigo_centro = ?"

                params.append(identificador)

                db.cursor.execute(sql_update_parts, tuple(params))
                actualizado = db.cursor.rowcount > 0
            if actualizado:
                print(f"[ACTUALIZAR] Centro de costo identificado por '{tipo_identificador}'='{identificador}' actualizado exitosamente.")
                self.mostrar_todos_centros_costos()
                return True
            else:
                print(f"[ACTUALIZAR] No se encontró centro de costo con '{tipo_identificador}'='{identificador}' para actualizar.")
                return False
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed: centro_costos.nombre_centro" in str(e):
                print(f"[ACTUALIZAR ERROR] El nuevo nombre '{nuevo_nombre}' ya existe para otro centro de costo.")
            else:
                print(f"[ACTUALIZAR ERROR] Error de integridad al actualizar centro de costo: {e}")
            return False
        except Exception as e:
            print(f"[ACTUALIZAR ERROR] Error inesperado al actualizar centro de costo: {e}")
            return False
        
    def eliminar_centro_costo(self, identificador, tipo_identificador: str) -> bool:
        if tipo_identificador not in ['id', 'nombre', 'codigo']:
            print(f"[BORRAR ERROR] Tipo de identificador '{tipo_identificador}' no válido. Use 'id', 'nombre'.")
            return False
        try:
            with self.db_connection as db:
                sql_delete_parts = "DELETE FROM centro_costos WHERE "
                db.conn.commit()
                if tipo_identificador == 'id':
                    sql_delete_parts += "id_centro_costos = ?"
                elif tipo_identificador == 'nombre':
                    sql_delete_parts += "nombre_centro = ?"

                db.cursor.execute(sql_delete_parts, (identificador,)) 

                if db.cursor.rowcount > 0:
                    print(f"[BORRAR] Centro de costo identificado por '{tipo_identificador}'='{identificador}' eliminada exitosamente.")
                    mostrar = True
                else:
                    print(f"[BORRAR] No se encontró centro de costo con '{tipo_identificador}'='{identificador}' para eliminar.")
                    mostrar = False
            if mostrar:
                self.mostrar_todos_centros_costos()
            return mostrar
        except Exception as e:
            print(f"[BORRAR ERROR] Error inesperado al borrar centro de costo: {e}")
            return False
        
    def mostrar_todos_centros_costos(self):
        print("\n--- Centros de Costo Actuales ---")
        try:
            with self.db_connection as db:
                db.cursor.execute("SELECT id_centro_costos, nombre_centro, descripcion, gerente, activo FROM centro_costos ORDER BY nombre_centro")
                db.conn.commit()
                centros = db.cursor.fetchall()
                if centros:
                    for centro in centros:
                        estado = "Activo" if centro['activo'] == 1 else "Inactivo"
                        print(f"ID: {centro['id_centro_costos']}, Nombre: {centro['nombre_centro']}, "
                              f"Descripción: {centro['descripcion'] if centro['descripcion'] else 'N/A'}, "
                              f"Gerente: {centro['gerente'] if centro['gerente'] else 'N/A'}, Estado: {estado}")
                else:
                    print("No hay centros de costo registrados.")
        except Exception as e:
            print(f"[MOSTRAR ERROR] Error al mostrar centros de costo: {e}")

class Manejador_categorias():
    def __init__(self, db_connection: DBConnection):
         self.db_connection = db_connection

    def crear_categoria(self, nombre: str, descripcion: str = None) -> Optional[int]:
        try:
            with self.db_connection as db:
                db.cursor.execute("INSERT INTO categorias (nombre_categoria, descripcion) VALUES (?, ?)",
                                  (nombre, descripcion))
                nuevo_id = db.cursor.lastrowid
                print(f"[CREAR] Categoría '{nombre}' (ID: {nuevo_id}) creada exitosamente.")
            self.mostrar_todas_categorias() # Muestra todas después de crear
            return nuevo_id
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed: categorias.nombre_categoria" in str(e):
                print(f"[CREAR ERROR] El nombre de categoría '{nombre}' ya existe. No se pudo crear.")
            else:
                print(f"[CREAR ERROR] Error de integridad al crear categoría: {e}")
            return None
        except Exception as e:
            print(f"[CREAR ERROR] Error inesperado al crear categoría: {e}")
            return None
        
    def leer_todas_categorias(self) -> List[Dict]:
        try:
            with self.db_connection as db:
                db.cursor.execute("SELECT id_categorias, nombre_categoria, descripcion FROM categorias ORDER BY nombre_categoria")
                return [dict(row) for row in db.cursor.fetchall()]
        except Exception as e:
            print(f"[LEER ERROR] Error al obtener todas las categorías: {e}")
            return []

    def leer_categoria_por_id(self, id_categorias: int) -> Optional[Dict]:
        try:
            with self.db_connection as db:
                db.cursor.execute("SELECT id_categorias, nombre_categoria, descripcion FROM categorias WHERE id_categorias = ?", (id_categorias,))
                row = db.cursor.fetchone()
                return dict(row) if row else None
        except Exception as e:
            print(f"[LEER ERROR] Error al obtener categoría por ID {id_categorias}: {e}")
            return None

    def leer_categoria_por_nombre(self, nombre: str) -> Optional[Dict]:
        try:
            with self.db_connection as db:
                db.cursor.execute("SELECT id_categorias, nombre_categoria, descripcion FROM categorias WHERE nombre_categoria = ?", (nombre,))
                row = db.cursor.fetchone()
                return dict(row) if row else None
        except Exception as e:
            print(f"[LEER ERROR] Error al obtener categoría por nombre '{nombre}': {e}")
            return None
        
    def actualizar_categoria(self, identificador, tipo_identificador: str,
                             nuevo_nombre: str = None, nueva_descripcion: str = None) -> bool:
        if not (nuevo_nombre or nueva_descripcion is not None):
            print("[ACTUALIZAR ERROR] Se debe proporcionar al menos un nuevo nombre o una nueva descripción.")
            return False

        if tipo_identificador not in ['id', 'nombre']:
            print(f"[ACTUALIZAR ERROR] Tipo de identificador '{tipo_identificador}' no válido. Use 'id' o 'nombre'.")
            return False

        try:
            with self.db_connection as db:
                set_clauses = []
                params = []

                if nuevo_nombre:
                    set_clauses.append("nombre_categoria = ?")
                    params.append(nuevo_nombre)
                if nueva_descripcion is not None: 
                    set_clauses.append("descripcion = ?")
                    params.append(nueva_descripcion)

                sql_update_parts = f"UPDATE categorias SET {', '.join(set_clauses)} WHERE "

                if tipo_identificador == 'id':
                    sql_update_parts += "id_categorias = ?"
                elif tipo_identificador == 'nombre':
                    sql_update_parts += "nombre_categoria = ?"

                params.append(identificador)

                db.cursor.execute(sql_update_parts, tuple(params))
                actualizado = db.cursor.rowcount > 0
            if actualizado:
                print(f"[ACTUALIZAR] Categoría identificada por '{tipo_identificador}'='{identificador}' actualizada exitosamente.")
                self.mostrar_todas_categorias()
                return True
            else:
                print(f"[ACTUALIZAR] No se encontró categoría con '{tipo_identificador}'='{identificador}' para actualizar.")
                return False
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed: categorias.nombre_categoria" in str(e):
                print(f"[ACTUALIZAR ERROR] El nuevo nombre '{nuevo_nombre}' ya existe para otra categoría.")
            else:
                print(f"[ACTUALIZAR ERROR] Error de integridad al actualizar categoría: {e}")
            return False
        except Exception as e:
            print(f"[ACTUALIZAR ERROR] Error inesperado al actualizar categoría: {e}")
            return False
        
    def eliminar_categoria(self, identificador, tipo_identificador: str) -> bool:
        if tipo_identificador not in ['id', 'nombre']:
            print(f"[BORRAR ERROR] Tipo de identificador '{tipo_identificador}' no válido. Use 'id' o 'nombre'.")
            return False

        try:
            with self.db_connection as db:
                sql_delete_parts = "DELETE FROM categorias WHERE "
                if tipo_identificador == 'id':
                    sql_delete_parts += "id_categorias = ?"
                elif tipo_identificador == 'nombre':
                    sql_delete_parts += "nombre_categoria = ?"

                db.cursor.execute(sql_delete_parts, (identificador,))
                eliminado = db.cursor.rowcount
            if eliminado:
                print(f"[BORRAR] Categoría identificada por '{tipo_identificador}'='{identificador}' eliminada exitosamente.")
                self.mostrar_todas_categorias()
                return True
            else:
                print(f"[BORRAR] No se encontró categoría con '{tipo_identificador}'='{identificador}' para eliminar.")
                return False
        except Exception as e:
            print(f"[BORRAR ERROR] Error inesperado al borrar categoría: {e}")
            return False

    def mostrar_todas_categorias(self):
        print("\n--- Categorías Actuales ---")
        categorias = self.leer_todas_categorias()
        if categorias:
            for categoria in categorias:
                print(f"ID: {categoria['id_categorias']}, Nombre: {categoria['nombre_categoria']}, "
                      f"Descripción: {categoria['descripcion'] if categoria['descripcion'] else 'N/A'}")
        else:
            print("No hay categorías registradas.")

class Manejador_proveedor():
    def __init__(self, db_connection: DBConnection):
          self.db_connection = db_connection

    def crear_proveedor(self, nombre: str, telefono: str = None, email: str = None, direccion: str = None) -> Optional[int]:
        try:
            with self.db_connection as db:
                db.cursor.execute("INSERT INTO proveedor (nombre_proveedor, telefono, email, direccion) VALUES (?, ?, ?, ?)",
                                  (nombre, telefono, email, direccion))
                nuevo_id = db.cursor.lastrowid
                print(f"[CREAR] Proveedor '{nombre}' (ID: {nuevo_id}) creado exitosamente.")
            self.mostrar_todos_proveedores() # Muestra todos después de crear
            return nuevo_id
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed: proveedores.nombre_proveedor" in str(e):
                print(f"[CREAR ERROR] El nombre de proveedor '{nombre}' ya existe. No se pudo crear.")
            else:
                print(f"[CREAR ERROR] Error de integridad al crear proveedor: {e}")
            return None
        except Exception as e:
            print(f"[CREAR ERROR] Error inesperado al crear proveedor: {e}")
            return None

    def leer_todos_proveedores(self) -> List[Dict]:
        try:
            with self.db_connection as db:
                db.cursor.execute("SELECT id_proveedor, nombre_proveedor, telefono, email, direccion FROM proveedor ORDER BY nombre_proveedor")
                return [dict(row) for row in db.cursor.fetchall()]
        except Exception as e:
            print(f"[LEER ERROR] Error al obtener todos los proveedores: {e}")
            return []
        
    def leer_proveedor_por_id(self, id_proveedor: int) -> Optional[Dict]:
        try:
            with self.db_connection as db:
                db.cursor.execute("SELECT id_proveedor, nombre_proveedor, telefono, email, direccion FROM proveedor WHERE id_proveedor = ?", (id_proveedor,))
                row = db.cursor.fetchone()
                return dict(row) if row else None
        except Exception as e:
            print(f"[LEER ERROR] Error al obtener proveedor por ID {id_proveedor}: {e}")
            return None

    def leer_proveedor_por_nombre(self, nombre: str) -> Optional[Dict]:
        try:
            with self.db_connection as db:
                db.cursor.execute("SELECT id_proveedor, nombre_proveedor, telefono, email, direccion FROM proveedor WHERE nombre_proveedor = ?", (nombre,))
                row = db.cursor.fetchone()
                return dict(row) if row else None
        except Exception as e:
            print(f"[LEER ERROR] Error al obtener proveedor por nombre '{nombre}': {e}")
            return None

    def actualizar_proveedor(self, identificador, tipo_identificador: str,
                             nuevo_nombre: str = None, nuevo_telefono: str = None,
                             nuevo_email: str = None, nueva_direccion: str = None) -> bool:
        if not (nuevo_nombre or nuevo_telefono is not None or nuevo_email is not None or nueva_direccion is not None):
            print("[ACTUALIZAR ERROR] Se debe proporcionar al menos un campo para actualizar.")
            return False

        if tipo_identificador not in ['id', 'nombre']:
            print(f"[ACTUALIZAR ERROR] Tipo de identificador '{tipo_identificador}' no válido. Use 'id' o 'nombre'.")
            return False

        try:
            with self.db_connection as db:
                set_clauses = []
                params = []

                if nuevo_nombre:
                    set_clauses.append("nombre_proveedor = ?")
                    params.append(nuevo_nombre)
                if nuevo_telefono is not None:
                    set_clauses.append("telefono = ?")
                    params.append(nuevo_telefono)
                if nuevo_email is not None:
                    set_clauses.append("email = ?")
                    params.append(nuevo_email)
                if nueva_direccion is not None:
                    set_clauses.append("direccion = ?")
                    params.append(nueva_direccion)

                sql_update_parts = f"UPDATE proveedor SET {', '.join(set_clauses)} WHERE "

                if tipo_identificador == 'id':
                    sql_update_parts += "id_proveedor = ?"
                elif tipo_identificador == 'nombre':
                    sql_update_parts += "nombre_proveedor = ?"

                params.append(identificador)
                db.cursor.execute(sql_update_parts, tuple(params))
                actualizado = db.cursor.rowcount > 0
            if actualizado:
                print(f"[ACTUALIZAR] Proveedor identificado por '{tipo_identificador}'='{identificador}' actualizado exitosamente.")
                self.mostrar_todos_proveedores() 
                return True
            else:
                print(f"[ACTUALIZAR] No se encontró proveedor con '{tipo_identificador}'='{identificador}' para actualizar.")
                return False
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed: proveedor.nombre_proveedor" in str(e):
                print(f"[ACTUALIZAR ERROR] El nuevo nombre '{nuevo_nombre}' ya existe para otro proveedor.")
            else:
                print(f"[ACTUALIZAR ERROR] Error de integridad al actualizar proveedor: {e}")
            return False
        except Exception as e:
            print(f"[ACTUALIZAR ERROR] Error inesperado al actualizar proveedor: {e}")
            return False

    def eliminar_proveedor(self, identificador, tipo_identificador: str) -> bool:
        if tipo_identificador not in ['id', 'nombre']:
            print(f"[BORRAR ERROR] Tipo de identificador '{tipo_identificador}' no válido. Use 'id' o 'nombre'.")
            return False
        try:
            with self.db_connection as db:
                sql_delete_parts = "DELETE FROM proveedor WHERE "
                if tipo_identificador == 'id':
                    sql_delete_parts += "id_proveedor = ?"
                elif tipo_identificador == 'nombre':
                    sql_delete_parts += "nombre_proveedor = ?"

                db.cursor.execute(sql_delete_parts, (identificador,))
                eliminado = db.cursor.rowcount
            if eliminado:
                print(f"[BORRAR] Proveedor identificado por '{tipo_identificador}'='{identificador}' eliminado exitosamente.")
                self.mostrar_todos_proveedores() 
                return True
            else:
                print(f"[BORRAR] No se encontró proveedor con '{tipo_identificador}'='{identificador}' para eliminar.")
                return False
        except Exception as e:
            print(f"[BORRAR ERROR] Error inesperado al borrar proveedor: {e}")
            return False

    def mostrar_todos_proveedores(self):
        print("\n--- Proveedores Actuales ---")
        proveedores = self.leer_todos_proveedores()
        if proveedores:
            for proveedor in proveedores:
                print(f"ID: {proveedor['id_proveedor']}, Nombre: {proveedor['nombre_proveedor']}, "
                      f"Teléfono: {proveedor['telefono'] if proveedor['telefono'] else 'N/A'}, "
                      f"Email: {proveedor['email'] if proveedor['email'] else 'N/A'}, "
                      f"Dirección: {proveedor['direccion'] if proveedor['direccion'] else 'N/A'}")
        else:
            print("No hay proveedores registrados.")

class Manejador_productos():
    def __init__(self, db_connection: DBConnection,
                 unidad_medida_manejador: Manejador_unidad_medida,
                 categoria_manejador: Manejador_categorias,
                 proveedor_manejador: Manejador_proveedor):
        
        self.db_connection = db_connection
        self.unidad_medida_manejador = unidad_medida_manejador
        self.categoria_manejador = categoria_manejador
        self.proveedor_manejador = proveedor_manejador
        

    def _validar_claves_foraneas(self, id_unidad_medida: int, id_categorias: int, id_proveedor: int) -> bool:
        """
        Valida que los IDs de las claves foráneas existan en sus respectivas tablas.
        :return: True si todos los IDs son válidos, False en caso contrario.
        """
        if not self.unidad_medida_manejador.leer_unidades_medida_id(id_unidad_medida):
            print(f"[VALIDACIÓN ERROR] ID de Unidad de Medida {id_unidad_medida} no existe.")
            return False
        if not self.categoria_manejador.leer_categoria_por_id(id_categorias):
            print(f"[VALIDACIÓN ERROR] ID de Categoría {id_categorias} no existe.")
            return False
        if not self.proveedor_manejador.leer_proveedor_por_id(id_proveedor):
            print(f"[VALIDACIÓN ERROR] ID de Proveedor {id_proveedor} no existe.")
            return False
        return True

    def crear_producto(self, nombre: str, descripcion: str, costo_unitario: float,
                       id_unidad_medida: int, id_categorias: int, id_proveedor: int,
                       fecha_caducidad: str = None, cantidad: int = 0) -> Optional[int]:

        if not self._validar_claves_foraneas(id_unidad_medida, id_categorias, id_proveedor):
            print("[CREAR ERROR] No se pudo crear el producto debido a IDs de referencia inválidos.")
            return None
        
        if fecha_caducidad:
            try:
                datetime.strptime(fecha_caducidad, '%Y-%m-%d')
            except ValueError:
                print(f"[CREAR ERROR] Formato de fecha de caducidad '{fecha_caducidad}' inválido. Use YYYY-MM-DD.")
                return None

        try:
            with self.db_connection as db:
                db.cursor.execute("INSERT INTO productos (nombre_producto, descripcion, costo_unitario, \
                                  fecha_caducidad, cantidad, id_unidad_medida, id_categorias, id_proveedor) \
                                  VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (nombre, descripcion, costo_unitario, fecha_caducidad, cantidad,
                                                                      id_unidad_medida, id_categorias, id_proveedor))
                nuevo_id = db.cursor.lastrowid
                print(f"[CREAR] Producto '{nombre}' (ID: {nuevo_id}) creado exitosamente.")
            self.mostrar_todos_productos()
            return nuevo_id
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed: productos.nombre_producto" in str(e):
                print(f"[CREAR ERROR] El nombre de producto '{nombre}' ya existe. No se pudo crear.")
            elif "FOREIGN KEY constraint failed" in str(e):
                print(f"[CREAR ERROR] Error de clave foránea al crear producto. Verifique los IDs de UM, Categoría o Proveedor. Detalle: {e}")
            else:
                print(f"[CREAR ERROR] Error de integridad al crear producto: {e}")
            return None
        except Exception as e:
            print(f"[CREAR ERROR] Error inesperado al crear producto: {e}")
            return None
        
    def leer_todos_productos(self) -> List[Dict]:
        try:
            with self.db_connection as db:
                db.cursor.execute("""
                SELECT p.id_productos, p.nombre_producto, p.descripcion,
                       p.costo_unitario, p.fecha_caducidad, p.cantidad, p.activo,
                       um.nombre_unidad_medida AS unidad_medida,
                       um.abreviatura AS unidad_abreviatura,
                       c.nombre_categoria AS categoria,
                       pr.nombre_proveedor AS proveedor
                FROM productos p
                JOIN unidad_medida um ON p.id_unidad_medida = um.id_unidad_medida
                JOIN categorias c ON p.id_categorias = c.id_categorias
                JOIN proveedor pr ON p.id_proveedor = pr.id_proveedor
                ORDER BY p.nombre_producto
            """)
                return [dict(row) for row in db.cursor.fetchall()]
        except Exception as e:
            print(f"[LEER ERROR] Error al obtener todos los productos: {e}")
            return []

    def leer_producto_por_id(self, id_productos: int) -> Optional[Dict]:
        try:
            with self.db_connection as db:
                db.cursor.execute("""
                    SELECT
                        p.id_productos,
                        p.nombre_producto,
                        p.descripcion,
                        p.costo_unitario,
                        p.fecha_caducidad,
                        p.cantidad,
                        um.nombre_unidad_medida AS unidad_medida,
                        um.abreviatura AS unidad_abreviatura,
                        c.nombre_categoria AS categoria,
                        pr.nombre_proveedor AS proveedor,
                        p.id_unidad_medida, 
                        p.id_categorias,
                        p.id_proveedor
                    FROM
                        productos p
                    JOIN
                        unidad_medida um ON p.id_unidad_medida = um.id_unidad_medida
                    JOIN
                        categorias c ON p.id_categorias = c.id_categorias
                    JOIN
                        proveedor pr ON p.id_proveedor = pr.id_proveedor
                    WHERE
                        p.id_productos = ?
                """, (id_productos,))
                row = db.cursor.fetchone()
                return dict(row) if row else None
        except Exception as e:
            print(f"[LEER ERROR] Error al obtener producto por ID {id_productos}: {e}")
            return None

    def leer_producto_por_nombre(self, nombre: str) -> Optional[Dict]:
        try:
            with self.db_connection as db:
                db.cursor.execute("""
                    SELECT
                        p.id_productos,
                        p.nombre_producto,
                        p.descripcion,
                        p.costo_unitario,
                        p.fecha_caducidad,
                        p.cantidad,
                        um.nombre_unidad_medida AS unidad_medida,
                        um.abreviatura AS unidad_abreviatura,
                        c.nombre_categoria AS categoria,
                        pr.nombre_proveedor AS proveedor,
                        p.id_unidad_medida,
                        p.id_categorias,
                        p.id_proveedor
                    FROM
                        productos p
                    JOIN
                        unidad_medida um ON p.id_unidad_medida = um.id_unidad_medida
                    JOIN
                        categorias c ON p.id_categorias = c.id_categorias
                    JOIN
                        proveedor pr ON p.id_proveedor = pr.id_proveedor
                    WHERE
                        p.nombre_producto = ?
                """, (nombre,))
                row = db.cursor.fetchone()
                return dict(row) if row else None
        except Exception as e:
            print(f"[LEER ERROR] Error al obtener producto por nombre '{nombre}': {e}")
            return None

    def actualizar_producto(self, identificador, tipo_identificador: str,
                            nuevo_nombre: str = None, nueva_descripcion: str = None,
                            nueva_fecha_caducidad: str = None, nuevo_costo_unitario: float = None,
                            nuevo_id_unidad_medida: int = None, nuevo_id_categorias: int = None,
                            nuevo_id_proveedor: int = None) -> bool:

        update_fields = {
            'nombre_producto': nuevo_nombre,
            'descripcion': nueva_descripcion,
            'fecha_caducidad': nueva_fecha_caducidad,
            'costo_unitario': nuevo_costo_unitario,
            'id_unidad_medida': nuevo_id_unidad_medida,
            'id_categorias': nuevo_id_categorias,
            'id_proveedor': nuevo_id_proveedor,
        }

        update_fields = {k: v for k, v in update_fields.items() if v is not None or (k in ['descripcion', 'fecha_caducidad'] and v is None)}


        if not update_fields:
            print("[ACTUALIZAR ERROR] Se debe proporcionar al menos un campo para actualizar.")
            return False

        if tipo_identificador not in ['id', 'nombre']:
            print(f"[ACTUALIZAR ERROR] Tipo de identificador '{tipo_identificador}' no válido. Use 'id' o 'nombre'.")
            return False

        if 'fecha_caducidad' in update_fields and update_fields['fecha_caducidad'] is not None:
            try:
                datetime.strptime(update_fields['fecha_caducidad'], '%Y-%m-%d')
            except ValueError:
                print(f"[ACTUALIZAR ERROR] Formato de fecha de caducidad '{update_fields['fecha_caducidad']}' inválido. Use YYYY-MM-DD.")
                return False
            
        current_product_data = None
        if tipo_identificador == 'id':
            current_product_data = self.leer_producto_por_id(identificador)
        elif tipo_identificador == 'nombre':
            current_product_data = self.leer_producto_por_nombre(identificador)

        if not current_product_data:
            print(f"[ACTUALIZAR ERROR] No se encontró producto con '{tipo_identificador}'='{identificador}' para actualizar.")
            return False
        
        id_um_to_validate = update_fields.get('id_unidad_medida', current_product_data['id_unidad_medida'])
        id_cat_to_validate = update_fields.get('id_categorias', current_product_data['id_categorias'])
        id_prov_to_validate = update_fields.get('id_proveedor', current_product_data['id_proveedor'])

        if not self._validar_claves_foraneas(id_um_to_validate, id_cat_to_validate, id_prov_to_validate):
            print("[ACTUALIZAR ERROR] No se pudo actualizar el producto debido a IDs de referencia inválidos.")
            return False

        try:
            with self.db_connection as db:
                set_clauses = []
                params = []

                for field, value in update_fields.items():
                    set_clauses.append(f"{field} = ?")
                    params.append(value)

                sql_update_parts = f"UPDATE productos SET {', '.join(set_clauses)} WHERE "

                if tipo_identificador == 'id':
                    sql_update_parts += "id_productos = ?"
                elif tipo_identificador == 'nombre':
                    sql_update_parts += "nombre_producto = ?"

                params.append(identificador)

                db.cursor.execute(sql_update_parts, tuple(params))
                actualizado = db.cursor.rowcount > 0
            if actualizado:
                print(f"[ACTUALIZAR] Producto identificado por '{tipo_identificador}'='{identificador}' actualizado exitosamente.")
                self.mostrar_todos_productos()
                return True
            else:
                print(f"[ACTUALIZAR] No se encontró producto con '{tipo_identificador}'='{identificador}' para actualizar.")
                return False
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed: productos.nombre_producto" in str(e):
                print(f"[ACTUALIZAR ERROR] El nuevo nombre '{nuevo_nombre}' ya existe para otro producto.")
            elif "FOREIGN KEY constraint failed" in str(e):
                print(f"[ACTUALIZAR ERROR] Error de clave foránea al actualizar producto. Verifique los IDs de UM, Categoría o Proveedor. Detalle: {e}")
            else:
                print(f"[ACTUALIZAR ERROR] Error de integridad al actualizar producto: {e}")
            return False
        except Exception as e:
            print(f"[ACTUALIZAR ERROR] Error inesperado al actualizar producto: {e}")
            return False

    def eliminar_producto(self, identificador, tipo_identificador: str) -> bool:
        if tipo_identificador not in ['id', 'nombre']:
            print(f"[BORRAR ERROR] Tipo de identificador '{tipo_identificador}' no válido. Use 'id' o 'nombre'.")
            return False

        try:
            with self.db_connection as db:
                sql_delete_parts = "DELETE FROM productos WHERE "
                if tipo_identificador == 'id':
                    sql_delete_parts += "id_productos = ?"
                elif tipo_identificador == 'nombre':
                    sql_delete_parts += "nombre_producto = ?"

                db.cursor.execute(sql_delete_parts, (identificador,))
                eliminado = db.cursor.rowcount
            if eliminado:
                print(f"[BORRAR] Producto identificado por '{tipo_identificador}'='{identificador}' eliminado exitosamente.")
                self.mostrar_todos_productos()
                return True
            else:
                print(f"[BORRAR] No se encontró producto con '{tipo_identificador}'='{identificador}' para eliminar.")
                return False
        except Exception as e:
            print(f"[BORRAR ERROR] Error inesperado al borrar producto: {e}")
            return False

    def mostrar_todos_productos(self):
        print("\n--- Productos Actuales ---")
        productos = self.leer_todos_productos()
        if productos:
            for p in productos:
                print(f"ID: {p['id_productos']}, Nombre: {p['nombre_producto']}, Descripción: {p['descripcion'] if p['descripcion'] else 'N/A'}, "
                      f"Costo: {p['costo_unitario']:.2f}, F. Cad.: {p['fecha_caducidad'] if p['fecha_caducidad'] else 'N/A'}, "
                      f"Unidad: {p['unidad_medida']} ({p['unidad_abreviatura']}), Categoría: {p['categoria']}, Proveedor: {p['proveedor']}")
        else:
            print("No hay productos registrados.")
        print("------------------------------------\n")

class Manejador_ubicacion_almacen():
    def __init__(self, db_connection: DBConnection):
        self.db_connection = db_connection

    def _actualiza_espacio_ocupado_en_db(self, cursor, id_ubicacion: int, new_espacio_ocupado: float):
        """Actualiza directamente el espacio ocupado de una ubicación (uso interno/MovimientoManager)."""
        cursor.execute("""
            UPDATE Ubicacion_Almacen
            SET espacio_ocupado = ?
            WHERE id_Ubicacion_Almacen = ?
        """, (new_espacio_ocupado, id_ubicacion))

    def crear_ubicacion_almacen(self, nombre: str, capacidad_total: float, espacio_ocupado: float = 0.0) -> Optional[int]:
        if capacidad_total <= 0:
            print("[CREAR ERROR] La capacidad total debe ser mayor que cero.")
            return None
        if espacio_ocupado < 0:
            print("[CREAR ERROR] El espacio ocupado no puede ser negativo.")
            return None
        if espacio_ocupado > capacidad_total:
            print("[CREAR ERROR] El espacio ocupado no puede exceder la capacidad total.")
            return None

        try:
            with self.db_connection as db:
                db.cursor.execute("""
                    INSERT INTO Ubicacion_Almacen (nombre_almacen, capacidad_total, espacio_ocupado)
                    VALUES (?, ?, ?)
                """, (nombre, capacidad_total, espacio_ocupado))
                nuevo_id = db.cursor.lastrowid
                print(f"[CREAR] Ubicación de almacén '{nombre}' (ID: {nuevo_id}, Capacidad: {capacidad_total:.2f}) creada exitosamente.")
                return nuevo_id
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed: Ubicacion_Almacen.nombre_almacen" in str(e):
                print(f"[CREAR ERROR] El nombre de ubicación '{nombre}' ya existe. No se pudo crear.")
            else:
                print(f"[CREAR ERROR] Error de integridad al crear ubicación de almacén: {e}")
            return None
        except Exception as e:
            print(f"[CREAR ERROR] Error inesperado al crear ubicación de almacén: {e}")
            return None

    def leer_ubicacion_por_id(self, id_ubicacion: int) -> Optional[Dict]:
        try:
            with self.db_connection as db:
                db.cursor.execute("SELECT id_Ubicacion_Almacen, nombre_almacen, capacidad_total, espacio_ocupado FROM Ubicacion_Almacen WHERE id_Ubicacion_Almacen = ?", (id_ubicacion,))
                row = db.cursor.fetchone()
                return dict(row) if row else None
        except Exception as e:
            print(f"[LEER ERROR] Error al obtener ubicación por ID {id_ubicacion}: {e}")
            return None
    def leer_ubicacion_por_nombre(self, nombre: str) -> Optional[Dict]:
        try:
            with self.db_connection as db:
                db.cursor.execute("SELECT id_Ubicacion_Almacen, nombre_almacen, capacidad_total, espacio_ocupado FROM Ubicacion_Almacen WHERE nombre_almacen = ?", (nombre,))
                row = db.cursor.fetchone()
                return dict(row) if row else None
        except Exception as e:
            print(f"[LEER ERROR] Error al obtener ubicación por nombre '{nombre}': {e}")
            return None

    def actualizar_ubicacion_almacen(self, id_ubicacion: int, nuevo_nombre: str = None,
                                     nueva_capacidad_total: float = None, nuevo_espacio_ocupado: float = None) -> bool:
        update_fields = {
            'nombre_almacen': nuevo_nombre,
            'capacidad_total': nueva_capacidad_total,
            'espacio_ocupado': nuevo_espacio_ocupado
        }
        update_fields = {k: v for k, v in update_fields.items() if v is not None}

        if not update_fields:
            print("[ACTUALIZAR ERROR] Se debe proporcionar al menos un campo para actualizar.")
            return False

        current_ubicacion = self.leer_ubicacion_por_id(id_ubicacion)
        if not current_ubicacion:
            print(f"[ACTUALIZAR ERROR] No se encontró la ubicación con ID {id_ubicacion}.")
            return False

        final_capacidad = update_fields.get('capacidad_total', current_ubicacion['capacidad_total'])
        final_espacio = update_fields.get('espacio_ocupado', current_ubicacion['espacio_ocupado'])

        if final_capacidad <= 0:
            print("[ACTUALIZAR ERROR] La nueva capacidad total debe ser mayor que cero.")
            return False
        if final_espacio < 0:
            print("[ACTUALIZAR ERROR] El nuevo espacio ocupado no puede ser negativo.")
            return False
        if final_espacio > final_capacidad:
            print("[ACTUALIZAR ERROR] El nuevo espacio ocupado no puede exceder la nueva capacidad total.")
            return False

        try:
            with self.db_connection as db:
                set_clauses = []
                params = []
                for field, value in update_fields.items():
                    set_clauses.append(f"{field} = ?")
                    params.append(value)

                sql_update = f"UPDATE Ubicacion_Almacen SET {', '.join(set_clauses)} WHERE id_Ubicacion_Almacen = ?"
                params.append(id_ubicacion)

                db.cursor.execute(sql_update, tuple(params))
                if db.cursor.rowcount > 0:
                    print(f"[ACTUALIZAR] Ubicación de almacén ID {id_ubicacion} actualizada exitosamente.")
                    return True
                else:
                    print(f"[ACTUALIZAR] No se encontró ubicación de almacén con ID {id_ubicacion} para actualizar.")
                    return False
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed: Ubicacion_Almacen.nombre_almacen" in str(e):
                print(f"[ACTUALIZAR ERROR] El nuevo nombre de ubicación '{nuevo_nombre}' ya existe. No se pudo actualizar.")
            else:
                print(f"[ACTUALIZAR ERROR] Error de integridad al actualizar ubicación de almacén: {e}")
            return False
        except Exception as e:
            print(f"[ACTUALIZAR ERROR] Error inesperado al actualizar ubicación de almacén: {e}")
            return False

    def eliminar_ubicacion_almacen(self, id_ubicacion: int) -> bool:
        try:
            with self.db_connection as db:
                db.cursor.execute("DELETE FROM Ubicacion_Almacen WHERE id_Ubicacion_Almacen = ?", (id_ubicacion,))
                if db.cursor.rowcount > 0:
                    print(f"[BORRAR] Ubicación de almacén ID {id_ubicacion} eliminada exitosamente.")
                    return True
                else:
                    print(f"[BORRAR] No se encontró ubicación de almacén con ID {id_ubicacion} para eliminar.")
                    return False
        except sqlite3.IntegrityError as e:
            print(f"[BORRAR ERROR] No se puede borrar la ubicación de almacén ID {id_ubicacion} porque está referenciada en otras tablas (ej. inventario_ubicacion). {e}")
            return False
        except Exception as e:
            print(f"[BORRAR ERROR] Error inesperado al borrar ubicación de almacén: {e}")
            return False

    def leer_todas_ubicaciones(self) -> List[Dict]:
        try:
            with self.db_connection as db:
                db.cursor.execute("SELECT id_Ubicacion_Almacen, nombre_almacen, capacidad_total, espacio_ocupado FROM Ubicacion_Almacen ORDER BY nombre_almacen")
                return [dict(row) for row in db.cursor.fetchall()]
        except Exception as e:
            print(f"[LEER ERROR] Error al obtener todas las ubicaciones de almacén: {e}")
            return []

    def mostrar_todas_ubicaciones(self):
        print("\n--- Listado de Ubicaciones de Almacén ---")
        ubicaciones = self.leer_todas_ubicaciones()
        if ubicaciones:
            for ub in ubicaciones:
                print(f"ID: {ub['id_Ubicacion_Almacen']}, Nombre: {ub['nombre_almacen']}, Capacidad Total: {ub['capacidad_total']:.2f}, Espacio Ocupado: {ub['espacio_ocupado']:.2f}")
        else:
            print("No hay ubicaciones de almacén registradas.")
        print("-------------------------------------------\n")

class Manejador_inventario_por_ubicacion():
    def __init__(self, db_connection: DBConnection, centro_costos_manejador: Manejador_centros_costos,
                 ubicacion_almacen_manejador: Manejador_ubicacion_almacen):
        self.db_connection = db_connection
        self.centro_costos_manejador = centro_costos_manejador
        self.ubicacion_almacen_manejador = ubicacion_almacen_manejador

    def _get_inventario_registro(self, cursor, id_producto: int, id_ubicacion: int) -> Optional[Dict]:
        """Obtiene un registro de inventario (solo para uso interno y MovimientoManager)."""
        cursor.execute("""
            SELECT id, stock_actual, id_centro_costos
            FROM inventario_ubicacion
            WHERE id_producto = ? AND id_ubicacion_almacen = ?
        """, (id_producto, id_ubicacion))
        row = cursor.fetchone()
        return dict(row) if row else None

    def _actualiza_stock_en_db(self, cursor, id_producto: int, id_ubicacion: int, nuevo_stock: float, ultima_actualizacion: str, id_centro_costos: int) -> bool:
        """Actualiza el stock de un registro existente o lo crea si no existe (uso interno/MovimientoManager)."""
        record = self._get_inventario_registro(cursor, id_producto, id_ubicacion)
        if record:
            cursor.execute("""
                UPDATE inventario_ubicacion
                SET stock_actual = ?, ultima_actualizacion = ?
                WHERE id = ?
            """, (nuevo_stock, ultima_actualizacion, record['id']))
            return True
        else:
            # Crear un nuevo registro si no existe
            cursor.execute("""
                INSERT INTO inventario_ubicacion (id_producto, id_ubicacion_almacen, stock_actual, ultima_actualizacion, id_centro_costos)
                VALUES (?, ?, ?, ?, ?)
            """, (id_producto, id_ubicacion, nuevo_stock, ultima_actualizacion, id_centro_costos))
            return True

    def _elimina_registro_stock_cero(self, cursor, id_producto: int, id_ubicacion: int) -> bool:
        """Elimina el registro de inventario si el stock llega a cero (uso interno/MovimientoManager)."""

        record = self._get_inventario_registro(self, cursor, id_producto, id_ubicacion)
        if record and record['stock_actual'] <= 0:
            cursor.execute("""
                DELETE FROM inventario_ubicacion
                WHERE id = ?
            """, (record['id'],))
            print(f"  > Registro de inventario para Producto {id_producto} en Ubicación {id_ubicacion} eliminado por stock cero.")
            return True
        return False

    def crear_registro_inventario(self, id_producto: int, id_ubicacion_almacen: int,
                                  stock_inicial: float, id_centro_costos: int) -> Optional[int]:
        """
        Crea un nuevo registro de inventario para un producto en una ubicación.
        Este método es para la creación inicial de un registro, no para movimientos.
        Las validaciones de FKs y espacio deben hacerse ANTES de llamar a este método.
        """
        ultima_actualizacion = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            with self.db_connection as db:
                # Comprobar si ya existe una entrada
                existing_record = self._get_inventario_registro(db.cursor, id_producto, id_ubicacion_almacen)
                if existing_record:
                    print(f"[CREAR ERROR] Ya existe un registro para Producto ID {id_producto} en Ubicación ID {id_ubicacion_almacen}. Use movimientos para actualizar.")
                    return None

                db.cursor.execute("""
                    INSERT INTO inventario_ubicacion (id_producto, id_ubicacion_almacen, stock_actual, ultima_actualizacion, id_centro_costos)
                    VALUES (?, ?, ?, ?, ?)
                """, (id_producto, id_ubicacion_almacen, stock_inicial, ultima_actualizacion, id_centro_costos))
                nuevo_id = db.cursor.lastrowid
                print(f"[CREAR] Registro de inventario (Producto: {id_producto}, Ubicación: {id_ubicacion_almacen}) creado con stock {stock_inicial} (ID: {nuevo_id}).")
                # El espacio en ubicacion_almacen se actualiza desde el MovimientoManager o en la lógica de creación inicial
                return nuevo_id
        except sqlite3.IntegrityError as e:
            print(f"[CREAR ERROR] Error de integridad al crear registro de inventario: {e}")
            return None
        except Exception as e:
            print(f"[CREAR ERROR] Error inesperado al crear registro de inventario: {e}")
            return None

    def leer_stock_por_ubicacion_y_producto(self, id_producto: int, id_ubicacion_almacen: int) -> Optional[Dict]:
        """
        Lee el stock de un producto específico en una ubicación específica.
        :param id_producto: ID del producto.
        :param id_ubicacion_almacen: ID de la ubicación de almacén.
        :return: Diccionario con la información del stock, o None si no se encuentra.
        """
        try:
            with self.db_connection as db:
                db.cursor.execute("""
                    SELECT
                        iu.id,
                        p.nombre_producto,
                        um.abreviatura AS unidad_medida_abreviatura,
                        ua.nombre_ubicacion,
                        iu.stock_actual,
                        iu.ultima_actualizacion,
                        cc.nombre_centro AS centro_costos,
                        iu.id_producto,
                        iu.id_ubicacion_almacen,
                        iu.id_centro_costos
                    FROM
                        inventario_ubicacion iu
                    JOIN
                        productos p ON iu.id_producto = p.id_producto
                    JOIN
                        ubicacion_almacen ua ON iu.id_ubicacion_almacen = ua.id_ubicacion
                    JOIN
                        centros_costos cc ON iu.id_centro_costos = cc.id_centro_costos
                    JOIN
                        unidad_medida um ON p.id_unidad_medida = um.id_unidad_medida
                    WHERE
                        iu.id_producto = ? AND iu.id_ubicacion_almacen = ?
                """, (id_producto, id_ubicacion_almacen))
                row = db.cursor.fetchone()
                if row:
                    print(f"\n[LEER STOCK] Stock para Producto '{row['nombre_producto']}' en Ubicación '{row['nombre_ubicacion']}': {row['stock_actual']} {row['unidad_medida_abreviatura']}")
                    return dict(row)
                else:
                    print(f"[LEER STOCK] No se encontró stock para Producto ID {id_producto} en Ubicación ID {id_ubicacion_almacen}.")
                    return None
        except Exception as e:
            print(f"[LEER ERROR] Error al leer stock por ubicación y producto: {e}")
            return None

    def leer_inventario_por_id(self, id_registro: int) -> Optional[Dict]:
        """
        Obtiene un registro de inventario por su ID, con detalles completos.
        """
        try:
            with self.db_connection as db:
                db.cursor.execute("""
                    SELECT
                        iu.id,
                        p.nombre_producto,
                        um.nombre_unidad_medida AS unidad_medida,
                        um.abreviatura AS unidad_abreviatura,
                        ua.nombre_ubicacion,
                        iu.stock_actual,
                        iu.ultima_actualizacion,
                        cc.nombre_centro AS centro_costos,
                        p.id_producto,
                        iu.id_ubicacion_almacen,
                        iu.id_centro_costos
                    FROM
                        inventario_ubicacion iu
                    JOIN
                        productos p ON iu.id_producto = p.id_producto
                    JOIN
                        ubicacion_almacen ua ON iu.id_ubicacion_almacen = ua.id_ubicacion
                    JOIN
                        centros_costos cc ON iu.id_centro_costos = cc.id_centro_costos
                    JOIN
                        unidad_medida um ON p.id_unidad_medida = um.id_unidad_medida
                    WHERE
                        iu.id = ?
                """, (id_registro,))
                row = db.cursor.fetchone()
                return dict(row) if row else None
        except Exception as e:
            print(f"[LEER ERROR] Error al obtener registro de inventario por ID {id_registro}: {e}")
            return None

    def leer_todo_inventario(self) -> List[Dict]:
        # Recupera todos los registros de inventario con detalles.
      
        try:
            with self.db_connection as db:
                db.cursor.execute("""
                    SELECT
                        iu.id,
                        p.nombre_producto,
                        um.abreviatura AS unidad_medida_abreviatura,
                        ua.nombre_ubicacion,
                        iu.stock_actual,
                        iu.ultima_actualizacion,
                        cc.nombre_centro AS centro_costos
                    FROM
                        inventario_ubicacion iu
                    JOIN
                        productos p ON iu.id_producto = p.id_producto
                    JOIN
                        ubicacion_almacen ua ON iu.id_ubicacion_almacen = ua.id_ubicacion
                    JOIN
                        centros_costos cc ON iu.id_centro_costos = cc.id_centro_costos
                    JOIN
                        unidad_medida um ON p.id_unidad_medida = um.id_unidad_medida
                    ORDER BY
                        p.nombre_producto, ua.nombre_ubicacion
                """)
                return [dict(row) for row in db.cursor.fetchall()]
        except Exception as e:
            print(f"[LEER ERROR] Error al obtener todo el inventario por ubicación: {e}")
            return []

    def actualizar_registro_inventario_completo(self, id_registro: int,
                                                 nuevo_stock_actual: float = None,
                                                 nuevo_id_centro_costos: int = None) -> bool:
       # Actualiza directamente el stock actual y/o el centro de costos de un registro de inventario.
       # NO es para movimientos de entrada/salida normales, es para correcciones directas o cambios de atribución.
        #Asegura que el espacio ocupado en la ubicación se ajuste.
        update_fields = {
            'stock_actual': nuevo_stock_actual,
            'id_centro_costos': nuevo_id_centro_costos,
        }
        update_fields = {k: v for k, v in update_fields.items() if v is not None}

        if not update_fields:
            print("[ACTUALIZAR ERROR] Se debe proporcionar al menos un campo para actualizar.")
            return False

        current_record = self.leer_inventario_por_id(id_registro)
        if not current_record:
            print(f"[ACTUALIZAR ERROR] No se encontró el registro de inventario con ID {id_registro}.")
            return False

        old_stock = current_record['stock_actual']
        final_stock = update_fields.get('stock_actual', old_stock)

        if final_stock < 0:
            print(f"[ACTUALIZAR ERROR] El stock actual no puede ser negativo ({final_stock}).")
            return False

        temp_cc_manager = self.centro_costos_manejador
        if 'id_centro_costos' in update_fields:
            if not temp_cc_manager.leer_centro_costo_por_id(update_fields['id_centro_costos']):
                print(f"[ACTUALIZAR ERROR] Nuevo ID de Centro de Costos {update_fields['id_centro_costos']} no existe.")
                return False

        ultima_actualizacion = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        update_fields['ultima_actualizacion'] = ultima_actualizacion 

        try:
            with self.db_connection as db:
                stock_change = final_stock - old_stock
                id_ubicacion_almacen = current_record['id_ubicacion_almacen']
                
                temp_ua_manager = self.ubicacion_almacen_manejador

                ubicacion_data = temp_ua_manager.leer_ubicacion_por_id(id_ubicacion_almacen)

                if not ubicacion_data:
                    print(f"[ACTUALIZAR ERROR] Ubicación ID {id_ubicacion_almacen} asociada al registro no encontrada.")
                    return False

                new_espacio_ocupado = ubicacion_data['espacio_ocupado'] + stock_change
                if new_espacio_ocupado < 0:
                    new_espacio_ocupado = 0 # Asegurar que no sea negativo

                if new_espacio_ocupado > ubicacion_data['capacidad_total']:
                    print(f"[ACTUALIZAR ERROR] El nuevo stock ({final_stock:.2f}) excedería la capacidad total de la ubicación ({ubicacion_data['capacidad_total']:.2f}).")
                    return False

                set_clauses = []
                params = []

                for field, value in update_fields.items():
                    set_clauses.append(f"{field} = ?")
                    params.append(value)

                sql_update = f"UPDATE inventario_ubicacion SET {', '.join(set_clauses)} WHERE id = ?"
                params.append(id_registro)

                db.cursor.execute(sql_update, tuple(params))

                # Actualizar el espacio ocupado en la tabla ubicacion_almacen
                db.cursor.execute("""
                    UPDATE ubicacion_almacen
                    SET espacio_ocupado = ?
                    WHERE id_ubicacion = ?
                """, (new_espacio_ocupado, id_ubicacion_almacen))

                if db.cursor.rowcount > 0:
                    print(f"[ACTUALIZAR] Registro de inventario ID {id_registro} actualizado exitosamente. Nuevo stock: {final_stock:.2f}. Espacio en ubicación: {new_espacio_ocupado:.2f}.")
                    self.mostrar_todo_inventario()
                    return True
                else:
                    print(f"[ACTUALIZAR] No se encontró registro de inventario con ID {id_registro} para actualizar.")
                    return False
        except sqlite3.IntegrityError as e:
            if "FOREIGN KEY constraint failed" in str(e):
                print(f"[ACTUALIZAR ERROR] Error de clave foránea al actualizar registro de inventario. Verifique el ID de Centro de Costos. Detalle: {e}")
            else:
                print(f"[ACTUALIZAR ERROR] Error de integridad al actualizar registro de inventario: {e}")
            return False
        except Exception as e:
            print(f"[ACTUALIZAR ERROR] Error inesperado al actualizar registro de inventario: {e}")
            return False

    def eliminar_registro_inventario(self, id_registro: int) -> bool:
        #Elimina un registro de inventario por su ID y ajusta el espacio ocupado en la ubicación.
        try:
            with self.db_connection as db:
                # Obtener la información del registro antes de borrarlo
                db.cursor.execute("SELECT id_producto, id_ubicacion_almacen, stock_actual FROM inventario_ubicacion WHERE id = ?", (id_registro,))
                record_to_delete = db.cursor.fetchone()

                if not record_to_delete:
                    print(f"[BORRAR] No se encontró registro de inventario con ID {id_registro} para eliminar.")
                    return False

                id_ubicacion_almacen = record_to_delete['id_ubicacion_almacen']
                stock_a_borrar = record_to_delete['stock_actual']
                # Borrar el registro
                db.cursor.execute("DELETE FROM inventario_ubicacion WHERE id = ?", (id_registro,))

                if db.cursor.rowcount > 0:
                    # Actualizar el espacio ocupado en la ubicación (usando instancia temporal de UbicacionAlmacenManager)
                    temp_ua_manager = self.ubicacion_almacen_manejador

                    ubicacion_data = temp_ua_manager.leer_ubicacion_por_id(id_ubicacion_almacen)
                    if ubicacion_data:
                        new_espacio_ocupado = ubicacion_data['espacio_ocupado'] - stock_a_borrar
                        if new_espacio_ocupado < 0:
                            new_espacio_ocupado = 0
                        db.cursor.execute("""
                            UPDATE ubicacion_almacen
                            SET espacio_ocupado = ?
                            WHERE id_ubicacion = ?
                        """, (new_espacio_ocupado, id_ubicacion_almacen))
                        print(f"  > Espacio ocupado en Ubicación ID {id_ubicacion_almacen} ajustado a {new_espacio_ocupado:.2f} debido a la eliminación del registro.")

                    print(f"[BORRAR] Registro de inventario ID {id_registro} eliminado exitosamente.")
                    self.mostrar_todo_inventario()
                    return True
                else:
                    return False # No debería llegar aquí si record_to_delete existía
        except Exception as e:
            print(f"[BORRAR ERROR] Error inesperado al borrar registro de inventario: {e}")
            return False

    def mostrar_todo_inventario(self):
        """Convenience method to print all inventory records by location."""
        print("\n--- Estado del Inventario por Ubicación ---")
        inventario_data = self.obtener_todo_inventario()
        if inventario_data:
            for item in inventario_data:
                print(f"ID Reg: {item['id']}, Producto: {item['nombre_producto']} ({item['unidad_medida_abreviatura']}), "
                      f"Ubicación: {item['nombre_ubicacion']}, Stock: {item['stock_actual']:.2f}, "
                      f"Última Act.: {item['ultima_actualizacion']}, Centro Costos: {item['centro_costos']}")
        else:
            print("No hay registros de inventario por ubicación.")
        print("------------------------------------------\n")

class Manejador_movimientos():
    MOVIMIENTO_TIPOS = ('ENTRADA', 'SALIDA', 'TRANSFERENCIA', 'AJUSTE POSITIVO', 'AJUSTE NEGATIVO')

    def __init__(self, db_connection: DBConnection,
                 producto_manejador: Manejador_productos,
                 ubicacion_almacen_manejador: Manejador_ubicacion_almacen,
                 centro_costos_manejador: Manejador_centros_costos,
                 inventario_ubicacion_manejador: Manejador_inventario_por_ubicacion):
        self.db_connection = db_connection
        self.producto_manejador = producto_manejador
        self.ubicacion_almacen_manejador = ubicacion_almacen_manejador
        self.centro_costos_manejador = centro_costos_manejador
        self.inventario_ubicacion_manejador = inventario_ubicacion_manejador
        
    def crear_movimiento(self, id_producto: int, cantidad: float, id_centro: int,
                         id_ubicacion_origen: int, tipo_movimiento: str,
                         id_ubicacion_destino: int = None,
                         referencia_documento: str = None, observaciones: str = None) -> Optional[int]:
        # Registra un movimiento de stock y actualiza el inventario por ubicación.


        if cantidad <= 0:
            print("[MOVIMIENTO ERROR] La cantidad del movimiento debe ser positiva.")
            return None
        if tipo_movimiento not in self.MOVIMIENTO_TIPOS:
            print(f"[MOVIMIENTO ERROR] Tipo de movimiento inválido: '{tipo_movimiento}'. Tipos permitidos: {', '.join(self.MOVIMIENTO_TIPOS)}.")
            return None

        # Validaciones de claves foráneas
        if not self.producto_manejador.leer_producto_por_id(id_producto):
            print(f"[MOVIMIENTO ERROR] Producto ID {id_producto} no existe.")
            return None
        if not self.centro_costos_manejador.leer_centro_costo_por_id(id_centro):
            print(f"[MOVIMIENTO ERROR] Centro de Costos ID {id_centro} no existe.")
            return None
        if not self.ubicacion_almacen_manejador.leer_ubicacion_por_id(id_ubicacion_origen):
            print(f"[MOVIMIENTO ERROR] Ubicación Origen ID {id_ubicacion_origen} no existe.")
            return None

        if tipo_movimiento == 'TRANSFERENCIA':
            if not id_ubicacion_destino:
                print("[MOVIMIENTO ERROR] Para 'TRANSFERENCIA', se requiere 'id_ubicacion_destino'.")
                return None
            if id_ubicacion_origen == id_ubicacion_destino:
                print("[MOVIMIENTO ERROR] La ubicación de origen y destino no pueden ser la misma para una transferencia.")
                return None
            if not self.ubicacion_almacen_manejador.leer_ubicacion_por_id(id_ubicacion_destino):
                print(f"[MOVIMIENTO ERROR] Ubicación Destino ID {id_ubicacion_destino} no existe.")
                return None
        elif id_ubicacion_destino is not None:
            print("[MOVIMIENTO ADVERTENCIA] 'id_ubicacion_destino' solo es relevante para TRANSFERENCIA. Será ignorado.")
            id_ubicacion_destino = None

        fecha_movimiento = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        try:
            with self.db_connection as db:
                # --- Lógica de Actualización de Inventario por Ubicación ---
                success = False
                if tipo_movimiento == 'ENTRADA' or tipo_movimiento == 'AJUSTE POSITIVO':
                    success = self._handle_stock_increase(db, id_producto, id_ubicacion_origen, cantidad, id_centro, fecha_movimiento)
                elif tipo_movimiento == 'SALIDA' or tipo_movimiento == 'AJUSTE NEGATIVO':
                    success = self._handle_stock_decrease(db, id_producto, id_ubicacion_origen, cantidad, fecha_movimiento)
                elif tipo_movimiento == 'TRANSFERENCIA':
                    success = self._handle_transfer(db, id_producto, id_ubicacion_origen, id_ubicacion_destino, cantidad, id_centro, fecha_movimiento)

                if not success:
                    print(f"[MOVIMIENTO ERROR] Fallo la actualización de inventario para el movimiento '{tipo_movimiento}'.")
                    return None

                # --- Registrar el Movimiento en la tabla 'movimiento' ---
                db.cursor.execute("""
                    INSERT INTO movimiento (id_producto, cantidad, id_centro, id_ubicacion_origen,
                                          id_ubicacion_destino, fecha_movimiento, referencia_documento,
                                          observaciones, tipo_movimiento)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (id_producto, cantidad, id_centro, id_ubicacion_origen,
                      id_ubicacion_destino, fecha_movimiento, referencia_documento,
                      observaciones, tipo_movimiento))
                nuevo_move_id = db.cursor.lastrowid
                print(f"[MOVIMIENTO CREADO] Movimiento de tipo '{tipo_movimiento}' registrado (ID: {nuevo_move_id}).")
                return nuevo_move_id

        except sqlite3.Error as e:
            print(f"[MOVIMIENTO ERROR] Error de base de datos al crear movimiento: {e}")
            return None
        except Exception as e:
            print(f"[MOVIMIENTO ERROR] Error inesperado al crear movimiento: {e}")
            return None

    def _handle_stock_increase(self, cursor, id_producto: int, id_ubicacion: int, cantidad: float, id_centro: int, ultima_actualizacion: str) -> bool:
        """Lógica para aumentar el stock y espacio ocupado."""
        ubicacion_data = self.ubicacion_almacen_manejador.leer_ubicacion_por_id(id_ubicacion)
        if not ubicacion_data:
            print(f"[MOVIMIENTO ERROR] Ubicación ID {id_ubicacion} no encontrada para aumento de stock.")
            return False

        # Obtener el registro actual de inventario para el producto en la ubicación
        inventario_record = self.inventario_ubicacion_manejador._get_inventario_registro(cursor, id_producto, id_ubicacion)

        current_stock = inventario_record['stock_actual'] if inventario_record else 0.0
        new_stock = current_stock + cantidad
        
        new_espacio_ocupado_ubicacion = ubicacion_data['espacio_ocupado'] + cantidad # Asunción 1:1
        
        if new_espacio_ocupado_ubicacion > ubicacion_data['capacidad_total']:
            print(f"[MOVIMIENTO ERROR] El espacio excedería la capacidad total de la ubicación ({ubicacion_data['capacidad_total']:.2f}). No se pudo realizar el aumento de stock.")
            return False


        id_centro_para_actualizacion = inventario_record['id_centro_costos'] if inventario_record else id_centro

        if not self.inventario_ubicacion_manejador._actualiza_stock_en_db(cursor, id_producto, id_ubicacion, new_stock, ultima_actualizacion, id_centro_para_actualizacion):
            return False 

        self.ubicacion_almacen_manejador._actualiza_espacio_ocupado_en_db(cursor, id_ubicacion, new_espacio_ocupado_ubicacion)
        print(f"  > Stock de Producto ID {id_producto} en Ubicación ID {id_ubicacion} actualizado a {new_stock:.2f}. Espacio en ubicación: {new_espacio_ocupado_ubicacion:.2f}.")
        return True

    def _handle_stock_decrease(self, cursor, id_producto: int, id_ubicacion: int, cantidad: float, ultima_actualizacion: str) -> bool:
        """Lógica para disminuir el stock y espacio ocupado."""
        inventario_record = self.inventario_ubicacion_manejador._get_inventario_registro(cursor, id_producto, id_ubicacion)
        ubicacion_data = self.ubicacion_almacen_manejador.leer_ubicacion_por_id(id_ubicacion)

        if not inventario_record:
            print(f"[MOVIMIENTO ERROR] No se encontró registro de inventario para Producto ID {id_producto} en Ubicación ID {id_ubicacion}. No se puede disminuir stock.")
            return False
        if not ubicacion_data:
            print(f"[MOVIMIENTO ERROR] Ubicación ID {id_ubicacion} no encontrada para disminución de stock.")
            return False

        current_stock = inventario_record['stock_actual']
        if current_stock < cantidad:
            print(f"[MOVIMIENTO ERROR] No hay suficiente stock (actual: {current_stock:.2f}) para una disminución de {cantidad}.")
            return False

        new_stock = current_stock - cantidad
        new_espacio_ocupado_ubicacion = ubicacion_data['espacio_ocupado'] - cantidad
        if new_espacio_ocupado_ubicacion < 0:
            new_espacio_ocupado_ubicacion = 0

        if not self.inventario_ubicacion_manejador._actualiza_stock_en_db(cursor, id_producto, id_ubicacion, new_stock, ultima_actualizacion, inventario_record['id_centro_costos']):
            return False
        self.ubicacion_almacen_manejador._actualiza_espacio_ocupado_en_db(cursor, id_ubicacion, new_espacio_ocupado_ubicacion)
        self.inventario_ubicacion_manejador._elimina_registro_stock_cero(cursor, id_producto, id_ubicacion)
        print(f"  > Stock de Producto ID {id_producto} en Ubicación ID {id_ubicacion} actualizado a {new_stock:.2f}. Espacio en ubicación: {new_espacio_ocupado_ubicacion:.2f}.")
        return True

    def _handle_transfer(self, db, id_producto: int, id_ubicacion_origen: int, id_ubicacion_destino: int, cantidad: float, id_centro: int, ultima_actualizacion: str) -> bool:
        """Lógica para transferencias entre ubicaciones."""
 
        if not self._handle_stock_decrease(db, id_producto, id_ubicacion_origen, cantidad, ultima_actualizacion):
            print(f"[TRANSFERENCIA ERROR] Falló la salida del producto de la ubicación de origen {id_ubicacion_origen}.")
            return False
 
        if not self._handle_stock_increase(db, id_producto, id_ubicacion_destino, cantidad, id_centro, ultima_actualizacion):
            print(f"[TRANSFERENCIA ERROR] Falló la entrada del producto a la ubicación de destino {id_ubicacion_destino}.")
         
            return False
        return True


    def leer_movimiento_por_id(self, id_movimiento: int) -> Optional[Dict]:
        """
        Obtiene los detalles de un movimiento por su ID.
        """
        try:
            with self.db_connection as db:
                db.cursor.execute("""
                    SELECT
                        m.id,
                        p.nombre_producto,
                        m.cantidad,
                        cc.nombre_centro AS centro_costos,
                        ua_origen.nombre_ubicacion AS ubicacion_origen,
                        ua_destino.nombre_ubicacion AS ubicacion_destino,
                        m.fecha_movimiento,
                        m.referencia_documento,
                        m.observaciones,
                        m.tipo_movimiento
                    FROM
                        movimiento m
                    JOIN
                        productos p ON m.id_producto = p.id_producto
                    JOIN
                        centros_costos cc ON m.id_centro = cc.id_centro_costos
                    JOIN
                        ubicacion_almacen ua_origen ON m.id_ubicacion_origen = ua_origen.id_ubicacion
                    LEFT JOIN -- LEFT JOIN porque id_ubicacion_destino puede ser NULL
                        ubicacion_almacen ua_destino ON m.id_ubicacion_destino = ua_destino.id_ubicacion
                    WHERE
                        m.id = ?
                """, (id_movimiento,))
                row = db.cursor.fetchone()
                return dict(row) if row else None
        except Exception as e:
            print(f"[LEER ERROR] Error al obtener movimiento por ID {id_movimiento}: {e}")
            return None

    def leer_todos_los_movimientos(self) -> List[Dict]:
        """
        Obtiene todos los movimientos registrados con detalles completos.
        """
        try:
            with self.db_connection as db:
                db.cursor.execute("""
                    SELECT
                        m.id,
                        p.nombre_producto,
                        m.cantidad,
cc.nombre_centro AS centro_costos,
                        ua_origen.nombre_ubicacion AS ubicacion_origen,
                        ua_destino.nombre_ubicacion AS ubicacion_destino,
                        m.fecha_movimiento,
                        m.referencia_documento,
                        m.observaciones,
                        m.tipo_movimiento
                    FROM
                        movimiento m
                    JOIN
                        productos p ON m.id_producto = p.id_producto
                    JOIN
                        centros_costos cc ON m.id_centro = cc.id_centro_costos
                    JOIN
                        ubicacion_almacen ua_origen ON m.id_ubicacion_origen = ua_origen.id_ubicacion
                    LEFT JOIN -- LEFT JOIN porque id_ubicacion_destino puede ser NULL
                        ubicacion_almacen ua_destino ON m.id_ubicacion_destino = ua_destino.id_ubicacion
                    ORDER BY
                        m.fecha_movimiento DESC
                """)
                return [dict(row) for row in db.cursor.fetchall()]
        except Exception as e:
            print(f"[LEER ERROR] Error al obtener todos los movimientos: {e}")
            return []

    def mostrar_todos_los_movimientos(self):
        """Convenience method to print all movements."""
        print("\n--- Historial de Movimientos ---")
        movimientos_data = self.leer_todos_los_movimientos()
        if movimientos_data:
            for item in movimientos_data:
                ubicacion_destino_str = f" a {item['ubicacion_destino']}" if item['ubicacion_destino'] else ""
                print(f"ID Mov: {item['id']}, Tipo: {item['tipo_movimiento']}, Producto: {item['nombre_producto']} ({item['cantidad']:.2f}), "
                      f"De: {item['ubicacion_origen']}{ubicacion_destino_str}, Fecha: {item['fecha_movimiento']}, "
                      f"Ref: {item['referencia_documento'] if item['referencia_documento'] else 'N/A'}, CC: {item['centro_costos']}")
        else:
            print("No hay movimientos registrados.")
        print("--------------------------------\n")
