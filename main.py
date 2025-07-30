import db_connection as db
import tkinter as tk
import customtkinter as ctk
from crud import (
    Manejador_centros_costos, 
    Manejador_productos, 
    Manejador_unidad_medida, 
    Manejador_proveedor, 
    Manejador_categorias, 
    Manejador_movimientos, 
    Manejador_ubicacion_almacen, 
    Manejador_inventario_por_ubicacion
)
from tkinter import ttk, messagebox
from datetime import datetime

class MainApplication(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configuración de la ventana principal
        self.title("Sistema de Gestión de Inventario")
        self.geometry("1200x700")
        self.configure(bg="#FDFBF6")
        self.resizable(True, True)
        
        # Conexión a la base de datos
        self.db_connection = db.DBConnection("database.db")
        
        # Inicialización de manejadores CRUD
        self._inicializar_manejadores()
        
        # Estilo de la interfaz
        self._configurar_estilos()
        
        # Crear widgets
        self.create_widgets()

    def _inicializar_manejadores(self):
        """Inicializa todos los manejadores de la base de datos"""
        self.unidad_medida_manejador = Manejador_unidad_medida(self.db_connection)
        self.categoria_manejador = Manejador_categorias(self.db_connection)
        self.proveedor_manejador = Manejador_proveedor(self.db_connection)
        self.centros_costos_manejador = Manejador_centros_costos(self.db_connection)
        self.productos_manejador = Manejador_productos(
            self.db_connection,
            self.unidad_medida_manejador,
            self.categoria_manejador,
            self.proveedor_manejador
        )
        self.ubicacion_almacen_manejador = Manejador_ubicacion_almacen(self.db_connection)
        self.inventario_ubicacion_manejador = Manejador_inventario_por_ubicacion(
            self.db_connection,
            self.centros_costos_manejador,
            self.ubicacion_almacen_manejador
        )
        self.movimientos_manejador = Manejador_movimientos(
            self.db_connection,
            self.productos_manejador,
            self.ubicacion_almacen_manejador,
            self.centros_costos_manejador,
            self.inventario_ubicacion_manejador
        )

    def _configurar_estilos(self):
        """Configura los estilos visuales de la aplicación"""
        self.style = ttk.Style()
        self.style.theme_use('clam') # Puedes probar 'default', 'alt', 'clam', 'classic'
        self.style.configure("TFrame", background="#FDFBF6")
        self.style.configure("Treeview", font=("Arial", 11), rowheight=25)
        self.style.configure("Treeview.Heading", font=("Arial", 12, "bold"), background="#4B5563", foreground="white")
        self.style.map("Treeview.Heading", background=[('active', '#374151')])
        ctk.set_appearance_mode("light") # "System", "Dark", "Light"
        ctk.set_default_color_theme("blue") # "blue", "dark-blue", "green"

    def create_widgets(self):
        """Crea la estructura principal de widgets"""
        # Frame principal que contiene sidebar y content area
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Sidebar
        self._crear_sidebar()
        
        # Área de contenido principal
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Espacio para el contenido dinámico
        self.dynamic_content = tk.Frame(
            self.content_frame,
            bg="#FDFBF6",
            bd=0
        )
        self.dynamic_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Mostrar pantalla de inicio por defecto
        self.show_home()

    def _crear_sidebar(self):
        """Crea la barra lateral de navegación"""
        self.sidebar = ctk.CTkFrame(
            self.main_frame,
            width=250,
            height=700,
            corner_radius=0,
            fg_color="#6B7280"
        )
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)
        
        # Título o Logo en la sidebar
        self.sidebar_title = ctk.CTkLabel(
            self.sidebar,
            text="MENÚ PRINCIPAL",
            text_color="#FFFFFF",
            font=("Arial", 16, "bold")
        )
        self.sidebar_title.pack(pady=(20, 30), padx=10, anchor=tk.CENTER)
        
        # Botones de navegación
        nav_buttons = [
            ("INICIO", self.show_home),
            ("PRODUCTOS", self.show_products),
            ("MOVIMIENTOS", self.show_movements),
            ("ALMACEN", self.show_warehouse),
            ("CATALOGOS", self.show_catalogs),
            ("REPORTES", self.show_reports)
        ]
        
        for text, command in nav_buttons:
            btn = ctk.CTkButton(
                self.sidebar,
                text=text,
                command=command,
                fg_color="#4B5563",
                hover_color="#374151",
                text_color="#FFFFFF",
                font=("Arial", 14),
                height=40,
                corner_radius=5
            )
            btn.pack(fill=tk.X, padx=10, pady=5)

    def clear_content(self):
        """Limpia el área de contenido dinámico"""
        for widget in self.dynamic_content.winfo_children():
            widget.destroy()

    # --- PANTALLAS PRINCIPALES ---
    def show_home(self):
        """Muestra la pantalla de inicio"""
        self.clear_content()
        tk.Label(
            self.dynamic_content,
            text="Bienvenido al Sistema de Gestión de Inventario",
            bg="#FDFBF6",
            fg="#1F2937",
            font=("Arial", 20, "bold")
        ).pack(pady=50)
        tk.Label(
            self.dynamic_content,
            text="Utilice el menú lateral para navegar por las diferentes secciones.",
            bg="#FDFBF6",
            fg="#1F2937",
            font=("Arial", 14)
        ).pack(pady=10)

    def show_catalogs(self):
        """Muestra la sección de gestión de catálogos"""
        self.clear_content()
        
        tk.Label(
            self.dynamic_content,
            text="Gestión de Catálogos",
            bg="#FDFBF6",
            fg="#1F2937",
            font=("Arial", 16, "bold")
        ).pack(pady=10)
        
        self._create_catalog_crud_buttons()
        
        self.catalog_message = tk.Label(
            self.dynamic_content,
            text="Seleccione un catálogo para administrar",
            bg="#FDFBF6",
            fg="#1F2937",
            font=("Arial", 16)
        )
        self.catalog_message.pack(pady=50)

    def _create_catalog_crud_buttons(self):
        """Crea los botones CRUD para la sección de catálogos"""
        button_frame = tk.Frame(self.dynamic_content, bg="#FDFBF6")
        button_frame.pack(pady=(10, 20))
        
        self.btn_select_catalog = ctk.CTkButton(
            button_frame,
            text="Seleccionar Catálogo",
            command=lambda: self._show_catalog_menu(button_frame),
            width=200,
            height=40,
            font=("Arial", 16, "bold")
        )
        self.btn_select_catalog.pack(side=tk.LEFT, padx=5)
        
        self.btn_add_catalog = ctk.CTkButton(
            button_frame,
            text="Agregar",
            state="disabled",
            width=200,
            height=40,
            font=("Arial", 16, "bold")
        )
        self.btn_modify_catalog = ctk.CTkButton(
            button_frame,
            text="Modificar",
            state="disabled",
            width=200,
            height=40,
            font=("Arial", 16, "bold")
        )
        self.btn_delete_catalog = ctk.CTkButton(
            button_frame,
            text="Eliminar",
            state="disabled",
            width=200,
            height=40,
            font=("Arial", 16, "bold")
        )
        
        self.btn_add_catalog.pack(side=tk.LEFT, padx=5)
        self.btn_modify_catalog.pack(side=tk.LEFT, padx=5)
        self.btn_delete_catalog.pack(side=tk.LEFT, padx=5)

    def _show_catalog_menu(self, parent):
        """Muestra el menú desplegable para seleccionar un catálogo"""
        menu = tk.Menu(self, tearoff=0)
        
        menu.add_command(label="Centro de Costos", command=self.show_centros_costos)
        menu.add_command(label="Unidades de Medida", command=self.show_unidades_medida)
        menu.add_command(label="Proveedores", command=self.show_proveedores)
        menu.add_command(label="Categorías", command=self.show_categorias)
        
        x = parent.winfo_rootx() + self.btn_select_catalog.winfo_x()
        y = parent.winfo_rooty() + self.btn_select_catalog.winfo_y() + self.btn_select_catalog.winfo_height()
        menu.tk_popup(x, y)

    # --- GESTIÓN DE CENTROS DE COSTOS ---
    def show_centros_costos(self):
        """Muestra la interfaz para gestionar centros de costos"""
        if hasattr(self, 'catalog_message'):
            self.catalog_message.pack_forget()
        
        self.clear_content_except_buttons() # Limpia solo el Treeview y mensajes anteriores
        
        tk.Label(
            self.dynamic_content,
            text="Gestión de Centros de Costos",
            bg="#FDFBF6",
            fg="#1F2937",
            font=("Arial", 14, "bold")
        ).pack(pady=(10, 0))

        self.btn_add_catalog.configure(state="normal", command=self.add_centro_costo)
        self.btn_modify_catalog.configure(state="normal", command=self.modify_centro_costo)
        self.btn_delete_catalog.configure(state="normal", command=self.delete_centro_costo)
        
        columns = ("ID", "Nombre", "Descripción", "Gerente", "Estado", "Fecha Creación")
        self.tree_centros_costos = ttk.Treeview(
            self.dynamic_content,
            columns=columns,
            show='headings',
            selectmode='browse'
        )
        
        for col in columns:
            self.tree_centros_costos.heading(col, text=col)
            self.tree_centros_costos.column(col, anchor=tk.CENTER, width=150)
        
        self.tree_centros_costos.column("Descripción", width=250)
        self.tree_centros_costos.column("Fecha Creación", width=120)
        
        scroll_y = ttk.Scrollbar(self.dynamic_content, orient=tk.VERTICAL, command=self.tree_centros_costos.yview)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_centros_costos.configure(yscrollcommand=scroll_y.set)
        
        self.tree_centros_costos.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        self.load_centros_costos()

    def load_centros_costos(self):
        """Carga los centros de costos en el Treeview"""
        for item in self.tree_centros_costos.get_children():
            self.tree_centros_costos.delete(item)
        
        centros = self.centros_costos_manejador.leer_todos_centros_costo()
        
        for centro in centros:
            estado = "Activo" if centro['activo'] == 1 else "Inactivo"
            self.tree_centros_costos.insert("", tk.END, values=(
                centro['id_centro_costos'],
                centro['nombre_centro'],
                centro['descripcion'] or "N/A",
                centro['gerente'] or "N/A",
                estado,
                centro['fecha_creacion']
            ))

    def add_centro_costo(self):
        """Abre la ventana para agregar un nuevo centro de costo"""
        self.add_window = ctk.CTkToplevel(self)
        self.add_window.title("Agregar Centro de Costo")
        self.add_window.geometry("400x350")
        self.add_window.grab_set()

        campos = [
            ("Nombre*", "entry_nombre"),
            ("Descripción", "entry_desc"),
            ("Gerente", "entry_gerente"),
            ("Activo", "check_activo")
        ]

        for i, (label_text, field_name) in enumerate(campos):
            label = ctk.CTkLabel(self.add_window, text=label_text)
            label.grid(row=i, column=0, padx=10, pady=10, sticky="e")

            if field_name.startswith("entry"):
                entry = ctk.CTkEntry(self.add_window, width=250)
                entry.grid(row=i, column=1, padx=10, pady=10)
                setattr(self, field_name, entry)
            elif field_name.startswith("check"):
                var = tk.IntVar(value=1)
                check = ctk.CTkCheckBox(self.add_window, text="", variable=var)
                check.grid(row=i, column=1, padx=10, pady=10, sticky="w")
                setattr(self, field_name, var)

        btn_frame = ctk.CTkFrame(self.add_window)
        btn_frame.grid(row=len(campos)+1, column=0, columnspan=2, pady=20)

        ctk.CTkButton(btn_frame, text="Guardar", fg_color="green", command=self.save_centro_costo).pack(side=tk.LEFT, padx=10)
        ctk.CTkButton(btn_frame, text="Cancelar", fg_color="red", command=self.add_window.destroy).pack(side=tk.LEFT, padx=10)

    def save_centro_costo(self):
        """Guarda un nuevo centro de costo en la base de datos"""
        nombre = self.entry_nombre.get().strip()
        descripcion = self.entry_desc.get().strip() or None
        gerente = self.entry_gerente.get().strip() or None
        activo = bool(self.check_activo.get())

        if not nombre:
            messagebox.showerror("Error", "El nombre es obligatorio")
            return

        try:
            nuevo_id = self.centros_costos_manejador.crear_centro_costos(nombre, descripcion, gerente, activo)
            if nuevo_id is not None:
                messagebox.showinfo("Éxito", f"Centro de costo creado con ID: {nuevo_id}")
                self.add_window.destroy()
                self.load_centros_costos()
            else:
                messagebox.showerror("Error", "No se pudo crear el centro de costo. Verifique la consola para más detalles.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {str(e)}")

    def modify_centro_costo(self):
        """Abre la ventana para modificar un centro de costo existente"""
        selected = self.tree_centros_costos.focus()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un centro de costo para modificar")
            return

        item_data = self.tree_centros_costos.item(selected)['values']
        
        self.modify_window = ctk.CTkToplevel(self)
        self.modify_window.title("Modificar Centro de Costo")
        self.modify_window.geometry("400x350")
        self.modify_window.grab_set()

        campos = [
            ("ID", "label_id", item_data[0]),
            ("Nombre*", "entry_nombre", item_data[1]),
            ("Descripción", "entry_desc", item_data[2]),
            ("Gerente", "entry_gerente", item_data[3]),
            ("Activo", "check_activo", item_data[4] == "Activo")
        ]

        for i, (label_text, field_name, default_val) in enumerate(campos):
            label = ctk.CTkLabel(self.modify_window, text=label_text)
            label.grid(row=i, column=0, padx=10, pady=10, sticky="e")

            if field_name.startswith("entry"):
                entry = ctk.CTkEntry(self.modify_window, width=250)
                entry.insert(0, default_val)
                entry.grid(row=i, column=1, padx=10, pady=10)
                setattr(self, field_name, entry)
            elif field_name.startswith("label"):
                label = ctk.CTkLabel(self.modify_window, text=str(default_val))
                label.grid(row=i, column=1, padx=10, pady=10, sticky="w")
            elif field_name.startswith("check"):
                var = tk.IntVar(value=1 if default_val else 0)
                check = ctk.CTkCheckBox(self.modify_window, text="", variable=var)
                check.grid(row=i, column=1, padx=10, pady=10, sticky="w")
                setattr(self, field_name, var)

        btn_frame = ctk.CTkFrame(self.modify_window)
        btn_frame.grid(row=len(campos)+1, column=0, columnspan=2, pady=20)

        ctk.CTkButton(btn_frame, text="Guardar", fg_color="green", command=lambda: self.update_centro_costo(item_data[0])).pack(side=tk.LEFT, padx=10)
        ctk.CTkButton(btn_frame, text="Cancelar", fg_color="red", command=self.modify_window.destroy).pack(side=tk.LEFT, padx=10)

    def update_centro_costo(self, id_centro):
        """Actualiza un centro de costo existente en la base de datos"""
        nombre = self.entry_nombre.get().strip()
        descripcion = self.entry_desc.get().strip() or None
        gerente = self.entry_gerente.get().strip() or None
        activo = bool(self.check_activo.get())

        if not nombre:
            messagebox.showerror("Error", "El nombre es obligatorio")
            return

        try:
            success = self.centros_costos_manejador.actualizar_centro_costo(
                id_centro,
                'id', # Tipo de identificador
                nuevo_nombre=nombre,
                nueva_descripcion=descripcion,
                nuevo_gerente=gerente,
                nuevo_estado_activo=activo
            )
            if success:
                messagebox.showinfo("Éxito", "Centro de costo actualizado correctamente")
                self.modify_window.destroy()
                self.load_centros_costos()
            else:
                messagebox.showerror("Error", "No se pudo actualizar el centro de costo. Verifique la consola para más detalles.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {str(e)}")

    def delete_centro_costo(self):
        """Elimina un centro de costo existente"""
        selected = self.tree_centros_costos.focus()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un centro de costo para eliminar")
            return

        item_data = self.tree_centros_costos.item(selected)
        id_centro = item_data['values'][0]
        nombre = item_data['values'][1]

        if not messagebox.askyesno("Confirmar Eliminación", f"¿Está seguro de eliminar el centro de costo:\n{nombre} (ID: {id_centro})?"):
            return

        try:
            success = self.centros_costos_manejador.eliminar_centro_costo(id_centro, 'id')
            if success:
                messagebox.showinfo("Éxito", "Centro de costo eliminado correctamente")
                self.load_centros_costos()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el centro de costo. Verifique si está siendo referenciado en otras tablas (ej. inventario).")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {str(e)}")

    # --- GESTIÓN DE UNIDADES DE MEDIDA ---
    def show_unidades_medida(self):
        """Muestra la interfaz para gestionar unidades de medida"""
        if hasattr(self, 'catalog_message'):
            self.catalog_message.pack_forget()
        
        self.clear_content_except_buttons()
        
        tk.Label(
            self.dynamic_content,
            text="Gestión de Unidades de Medida",
            bg="#FDFBF6",
            fg="#1F2937",
            font=("Arial", 14, "bold")
        ).pack(pady=(10, 0))

        self.btn_add_catalog.configure(state="normal", command=self.add_unidad_medida)
        self.btn_modify_catalog.configure(state="normal", command=self.modify_unidad_medida)
        self.btn_delete_catalog.configure(state="normal", command=self.delete_unidad_medida)
        
        columns = ("ID", "Nombre", "Abreviatura")
        self.tree_unidades_medida = ttk.Treeview(
            self.dynamic_content,
            columns=columns,
            show='headings',
            selectmode='browse'
        )
        
        for col in columns:
            self.tree_unidades_medida.heading(col, text=col)
            self.tree_unidades_medida.column(col, anchor=tk.CENTER, width=150)
        
        self.tree_unidades_medida.column("Nombre", width=250)
        
        scroll_y = ttk.Scrollbar(self.dynamic_content, orient=tk.VERTICAL, command=self.tree_unidades_medida.yview)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_unidades_medida.configure(yscrollcommand=scroll_y.set)
        
        self.tree_unidades_medida.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        self.load_unidades_medida()

    def load_unidades_medida(self):
        """Carga las unidades de medida en el Treeview"""
        for item in self.tree_unidades_medida.get_children():
            self.tree_unidades_medida.delete(item)

        unidades = self.unidad_medida_manejador.leer_unidades_medida()

        for unidad in unidades:
            self.tree_unidades_medida.insert("", tk.END, values=(
                unidad['id_unidad_medida'],
                unidad['nombre_unidad_medida'],
                unidad['abreviatura']
            ))

    def add_unidad_medida(self):
        """Abre la ventana para agregar una nueva unidad de medida"""
        self.add_window = ctk.CTkToplevel(self)
        self.add_window.title("Agregar Unidad de Medida")
        self.add_window.geometry("400x250")
        self.add_window.grab_set()

        campos = [
            ("Nombre*", "entry_nombre"),
            ("Abreviatura*", "entry_abreviatura")
        ]

        for i, (label_text, field_name) in enumerate(campos):
            label = ctk.CTkLabel(self.add_window, text=label_text)
            label.grid(row=i, column=0, padx=10, pady=10, sticky="e")

            entry = ctk.CTkEntry(self.add_window, width=250)
            entry.grid(row=i, column=1, padx=10, pady=10)
            setattr(self, field_name, entry)

        btn_frame = ctk.CTkFrame(self.add_window)
        btn_frame.grid(row=len(campos)+1, column=0, columnspan=2, pady=20)

        ctk.CTkButton(btn_frame, text="Guardar", fg_color="green", command=self.save_unidad_medida).pack(side=tk.LEFT, padx=10)
        ctk.CTkButton(btn_frame, text="Cancelar", fg_color="red", command=self.add_window.destroy).pack(side=tk.LEFT, padx=10)

    def save_unidad_medida(self):
        """Guarda una nueva unidad de medida en la base de datos"""
        nombre = self.entry_nombre.get().strip()
        abreviatura = self.entry_abreviatura.get().strip()

        if not nombre or not abreviatura:
            messagebox.showerror("Error", "Nombre y abreviatura son campos obligatorios")
            return

        try:
            nuevo_id = self.unidad_medida_manejador.crear_unidad_medida(nombre, abreviatura)
            if nuevo_id is not None:
                messagebox.showinfo("Éxito", f"Unidad de medida creada con ID: {nuevo_id}")
                self.add_window.destroy()
                self.load_unidades_medida()
            else:
                messagebox.showerror("Error", "No se pudo crear la unidad de medida. Verifique la consola para más detalles.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {str(e)}")

    def modify_unidad_medida(self):
        """Abre la ventana para modificar una unidad de medida existente"""
        selected = self.tree_unidades_medida.focus()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione una unidad de medida para modificar")
            return

        item_data = self.tree_unidades_medida.item(selected)['values']
        
        self.modify_window = ctk.CTkToplevel(self)
        self.modify_window.title("Modificar Unidad de Medida")
        self.modify_window.geometry("400x250")
        self.modify_window.grab_set()

        campos = [
            ("ID", "label_id", item_data[0]),
            ("Nombre*", "entry_nombre", item_data[1]),
            ("Abreviatura*", "entry_abreviatura", item_data[2])
        ]

        for i, (label_text, field_name, default_val) in enumerate(campos):
            label = ctk.CTkLabel(self.modify_window, text=label_text)
            label.grid(row=i, column=0, padx=10, pady=10, sticky="e")

            if field_name.startswith("entry"):
                entry = ctk.CTkEntry(self.modify_window, width=250)
                entry.insert(0, default_val)
                entry.grid(row=i, column=1, padx=10, pady=10)
                setattr(self, field_name, entry)
            elif field_name.startswith("label"):
                label = ctk.CTkLabel(self.modify_window, text=str(default_val))
                label.grid(row=i, column=1, padx=10, pady=10, sticky="w")

        btn_frame = ctk.CTkFrame(self.modify_window)
        btn_frame.grid(row=len(campos)+1, column=0, columnspan=2, pady=20)

        ctk.CTkButton(btn_frame, text="Guardar", fg_color="green", command=lambda: self.update_unidad_medida(item_data[0])).pack(side=tk.LEFT, padx=10)
        ctk.CTkButton(btn_frame, text="Cancelar", fg_color="red", command=self.modify_window.destroy).pack(side=tk.LEFT, padx=10)

    def update_unidad_medida(self, id_unidad):
        """Actualiza una unidad de medida existente en la base de datos"""
        nombre = self.entry_nombre.get().strip()
        abreviatura = self.entry_abreviatura.get().strip()

        if not nombre or not abreviatura:
            messagebox.showerror("Error", "Nombre y abreviatura son campos obligatorios")
            return

        try:
            success = self.unidad_medida_manejador.actualizar_unidad_medida(
                id_unidad,
                tipo_identificador='id',
                nuevo_nombre=nombre,
                nueva_abreviatura=abreviatura
            )
            if success:
                messagebox.showinfo("Éxito", "Unidad de medida actualizada correctamente")
                self.modify_window.destroy()
                self.load_unidades_medida()
            else:
                messagebox.showerror("Error", "No se pudo actualizar la unidad de medida. Verifique la consola para más detalles.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {str(e)}")

    def delete_unidad_medida(self):
        """Elimina una unidad de medida existente"""
        selected = self.tree_unidades_medida.focus()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione una unidad de medida para eliminar")
            return

        item_data = self.tree_unidades_medida.item(selected)
        id_unidad = item_data['values'][0]
        nombre = item_data['values'][1]

        if not messagebox.askyesno("Confirmar Eliminación", f"¿Está seguro de eliminar la unidad de medida:\n{nombre} (ID: {id_unidad})?"):
            return

        try:
            success = self.unidad_medida_manejador.eliminar_unidad_medida(id_unidad, 'id')
            if success:
                messagebox.showinfo("Éxito", "Unidad de medida eliminada correctamente")
                self.load_unidades_medida()
            else:
                messagebox.showerror("Error", "No se pudo eliminar la unidad de medida. Verifique si está siendo referenciada en otras tablas (ej. productos).")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {str(e)}")

    # --- GESTIÓN DE PROVEEDORES ---
    def show_proveedores(self):
        """Muestra la interfaz para gestionar proveedores"""
        if hasattr(self, 'catalog_message'):
            self.catalog_message.pack_forget()
        
        self.clear_content_except_buttons()
        
        tk.Label(
            self.dynamic_content,
            text="Gestión de Proveedores",
            bg="#FDFBF6",
            fg="#1F2937",
            font=("Arial", 14, "bold")
        ).pack(pady=(10, 0))

        self.btn_add_catalog.configure(state="normal", command=self.add_proveedor)
        self.btn_modify_catalog.configure(state="normal", command=self.modify_proveedor)
        self.btn_delete_catalog.configure(state="normal", command=self.delete_proveedor)
        
        columns = ("ID", "Nombre", "Teléfono", "Email", "Dirección")
        self.tree_proveedores = ttk.Treeview(
            self.dynamic_content,
            columns=columns,
            show='headings',
            selectmode='browse'
        )
        
        for col in columns:
            self.tree_proveedores.heading(col, text=col)
            self.tree_proveedores.column(col, anchor=tk.CENTER, width=150)
        
        self.tree_proveedores.column("Nombre", width=200)
        self.tree_proveedores.column("Dirección", width=250)
        
        scroll_y = ttk.Scrollbar(self.dynamic_content, orient=tk.VERTICAL, command=self.tree_proveedores.yview)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_proveedores.configure(yscrollcommand=scroll_y.set)
        
        self.tree_proveedores.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        self.load_proveedores()

    def load_proveedores(self):
        """Carga los proveedores en el Treeview"""
        for item in self.tree_proveedores.get_children():
            self.tree_proveedores.delete(item)

        proveedores = self.proveedor_manejador.leer_todos_proveedores()

        for proveedor in proveedores:
            self.tree_proveedores.insert("", tk.END, values=(
                proveedor['id_proveedor'],
                proveedor['nombre_proveedor'],
                proveedor['telefono'] or "N/A",
                proveedor['email'] or "N/A",
                proveedor['direccion'] or "N/A"
            ))

    def add_proveedor(self):
        """Abre la ventana para agregar un nuevo proveedor"""
        self.add_window = ctk.CTkToplevel(self)
        self.add_window.title("Agregar Proveedor")
        self.add_window.geometry("400x300")
        self.add_window.grab_set()

        campos = [
            ("Nombre*", "entry_nombre"),
            ("Teléfono", "entry_telefono"),
            ("Email", "entry_email"),
            ("Dirección", "entry_direccion")
        ]

        for i, (label_text, field_name) in enumerate(campos):
            label = ctk.CTkLabel(self.add_window, text=label_text)
            label.grid(row=i, column=0, padx=10, pady=10, sticky="e")

            entry = ctk.CTkEntry(self.add_window, width=250)
            entry.grid(row=i, column=1, padx=10, pady=10)
            setattr(self, field_name, entry)

        btn_frame = ctk.CTkFrame(self.add_window)
        btn_frame.grid(row=len(campos)+1, column=0, columnspan=2, pady=20)

        ctk.CTkButton(btn_frame, text="Guardar", fg_color="green", command=self.save_proveedor).pack(side=tk.LEFT, padx=10)
        ctk.CTkButton(btn_frame, text="Cancelar", fg_color="red", command=self.add_window.destroy).pack(side=tk.LEFT, padx=10)

    def save_proveedor(self):
        """Guarda un nuevo proveedor en la base de datos"""
        nombre = self.entry_nombre.get().strip()
        telefono = self.entry_telefono.get().strip() or None
        email = self.entry_email.get().strip() or None
        direccion = self.entry_direccion.get().strip() or None

        if not nombre:
            messagebox.showerror("Error", "El nombre es obligatorio")
            return

        try:
            nuevo_id = self.proveedor_manejador.crear_proveedor(nombre, telefono, email, direccion)
            if nuevo_id is not None:
                messagebox.showinfo("Éxito", f"Proveedor creado con ID: {nuevo_id}")
                self.add_window.destroy()
                self.load_proveedores()
            else:
                messagebox.showerror("Error", "No se pudo crear el proveedor. Verifique la consola para más detalles.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {str(e)}")

    def modify_proveedor(self):
        """Abre la ventana para modificar un proveedor existente"""
        selected = self.tree_proveedores.focus()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un proveedor para modificar")
            return

        item_data = self.tree_proveedores.item(selected)['values']
        
        self.modify_window = ctk.CTkToplevel(self)
        self.modify_window.title("Modificar Proveedor")
        self.modify_window.geometry("400x300")
        self.modify_window.grab_set()

        campos = [
            ("ID", "label_id", item_data[0]),
            ("Nombre*", "entry_nombre", item_data[1]),
            ("Teléfono", "entry_telefono", item_data[2]),
            ("Email", "entry_email", item_data[3]),
            ("Dirección", "entry_direccion", item_data[4])
        ]

        for i, (label_text, field_name, default_val) in enumerate(campos):
            label = ctk.CTkLabel(self.modify_window, text=label_text)
            label.grid(row=i, column=0, padx=10, pady=10, sticky="e")

            if field_name.startswith("entry"):
                entry = ctk.CTkEntry(self.modify_window, width=250)
                entry.insert(0, default_val)
                entry.grid(row=i, column=1, padx=10, pady=10)
                setattr(self, field_name, entry)
            elif field_name.startswith("label"):
                label = ctk.CTkLabel(self.modify_window, text=str(default_val))
                label.grid(row=i, column=1, padx=10, pady=10, sticky="w")

        btn_frame = ctk.CTkFrame(self.modify_window)
        btn_frame.grid(row=len(campos)+1, column=0, columnspan=2, pady=20)

        ctk.CTkButton(btn_frame, text="Guardar", fg_color="green", command=lambda: self.update_proveedor(item_data[0])).pack(side=tk.LEFT, padx=10)
        ctk.CTkButton(btn_frame, text="Cancelar", fg_color="red", command=self.modify_window.destroy).pack(side=tk.LEFT, padx=10)

    def update_proveedor(self, id_proveedor):
        """Actualiza un proveedor existente en la base de datos"""
        nombre = self.entry_nombre.get().strip()
        telefono = self.entry_telefono.get().strip() or None
        email = self.entry_email.get().strip() or None
        direccion = self.entry_direccion.get().strip() or None

        if not nombre:
            messagebox.showerror("Error", "El nombre es obligatorio")
            return

        try:
            success = self.proveedor_manejador.actualizar_proveedor(
                id_proveedor,
                tipo_identificador='id',
                nuevo_nombre=nombre,
                nuevo_telefono=telefono,
                nuevo_email=email,
                nueva_direccion=direccion
            )
            if success:
                messagebox.showinfo("Éxito", "Proveedor actualizado correctamente")
                self.modify_window.destroy()
                self.load_proveedores()
            else:
                messagebox.showerror("Error", "No se pudo actualizar el proveedor. Verifique la consola para más detalles.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {str(e)}")

    def delete_proveedor(self):
        """Elimina un proveedor existente"""
        selected = self.tree_proveedores.focus()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un proveedor para eliminar")
            return

        item_data = self.tree_proveedores.item(selected)
        id_proveedor = item_data['values'][0]
        nombre = item_data['values'][1]

        if not messagebox.askyesno("Confirmar Eliminación", f"¿Está seguro de eliminar el proveedor:\n{nombre} (ID: {id_proveedor})?"):
            return

        try:
            success = self.proveedor_manejador.eliminar_proveedor(id_proveedor, 'id')
            if success:
                messagebox.showinfo("Éxito", "Proveedor eliminado correctamente")
                self.load_proveedores()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el proveedor. Verifique si está siendo referenciado en otras tablas (ej. productos).")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {str(e)}")

    # --- GESTIÓN DE CATEGORÍAS ---
    def show_categorias(self):
        """Muestra la interfaz para gestionar categorías"""
        if hasattr(self, 'catalog_message'):
            self.catalog_message.pack_forget()
        
        self.clear_content_except_buttons()
        
        tk.Label(
            self.dynamic_content,
            text="Gestión de Categorías",
            bg="#FDFBF6",
            fg="#1F2937",
            font=("Arial", 14, "bold")
        ).pack(pady=(10, 0))

        self.btn_add_catalog.configure(state="normal", command=self.add_categoria)
        self.btn_modify_catalog.configure(state="normal", command=self.modify_categoria)
        self.btn_delete_catalog.configure(state="normal", command=self.delete_categoria)
        
        columns = ("ID", "Nombre", "Descripción")
        self.tree_categorias = ttk.Treeview(
            self.dynamic_content,
            columns=columns,
            show='headings',
            selectmode='browse'
        )
        
        for col in columns:
            self.tree_categorias.heading(col, text=col)
            self.tree_categorias.column(col, anchor=tk.CENTER, width=150)
        
        self.tree_categorias.column("Nombre", width=200)
        self.tree_categorias.column("Descripción", width=300)
        
        scroll_y = ttk.Scrollbar(self.dynamic_content, orient=tk.VERTICAL, command=self.tree_categorias.yview)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_categorias.configure(yscrollcommand=scroll_y.set)
        
        self.tree_categorias.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        self.load_categorias()

    def load_categorias(self):
        """Carga las categorías en el Treeview"""
        for item in self.tree_categorias.get_children():
            self.tree_categorias.delete(item)

        categorias = self.categoria_manejador.leer_todas_categorias()

        for categoria in categorias:
            self.tree_categorias.insert("", tk.END, values=(
                categoria['id_categorias'],
                categoria['nombre_categoria'],
                categoria['descripcion'] or "N/A"
            ))

    def add_categoria(self):
        """Abre la ventana para agregar una nueva categoría"""
        self.add_window = ctk.CTkToplevel(self)
        self.add_window.title("Agregar Categoría")
        self.add_window.geometry("400x250")
        self.add_window.grab_set()

        campos = [
            ("Nombre*", "entry_nombre"),
            ("Descripción", "entry_desc")
        ]

        for i, (label_text, field_name) in enumerate(campos):
            label = ctk.CTkLabel(self.add_window, text=label_text)
            label.grid(row=i, column=0, padx=10, pady=10, sticky="e")

            entry = ctk.CTkEntry(self.add_window, width=250)
            entry.grid(row=i, column=1, padx=10, pady=10)
            setattr(self, field_name, entry)

        btn_frame = ctk.CTkFrame(self.add_window)
        btn_frame.grid(row=len(campos)+1, column=0, columnspan=2, pady=20)

        ctk.CTkButton(btn_frame, text="Guardar", fg_color="green", command=self.save_categoria).pack(side=tk.LEFT, padx=10)
        ctk.CTkButton(btn_frame, text="Cancelar", fg_color="red", command=self.add_window.destroy).pack(side=tk.LEFT, padx=10)

    def save_categoria(self):
        """Guarda una nueva categoría en la base de datos"""
        nombre = self.entry_nombre.get().strip()
        descripcion = self.entry_desc.get().strip() or None

        if not nombre:
            messagebox.showerror("Error", "El nombre es obligatorio")
            return

        try:
            nuevo_id = self.categoria_manejador.crear_categoria(nombre, descripcion)
            if nuevo_id is not None:
                messagebox.showinfo("Éxito", f"Categoría creada con ID: {nuevo_id}")
                self.add_window.destroy()
                self.load_categorias()
            else:
                messagebox.showerror("Error", "No se pudo crear la categoría. Verifique la consola para más detalles.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {str(e)}")

    def modify_categoria(self):
        """Abre la ventana para modificar una categoría existente"""
        selected = self.tree_categorias.focus()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione una categoría para modificar")
            return

        item_data = self.tree_categorias.item(selected)['values']
        
        self.modify_window = ctk.CTkToplevel(self)
        self.modify_window.title("Modificar Categoría")
        self.modify_window.geometry("400x250")
        self.modify_window.grab_set()

        campos = [
            ("ID", "label_id", item_data[0]),
            ("Nombre*", "entry_nombre", item_data[1]),
            ("Descripción", "entry_desc", item_data[2])
        ]

        for i, (label_text, field_name, default_val) in enumerate(campos):
            label = ctk.CTkLabel(self.modify_window, text=label_text)
            label.grid(row=i, column=0, padx=10, pady=10, sticky="e")

            if field_name.startswith("entry"):
                entry = ctk.CTkEntry(self.modify_window, width=250)
                entry.insert(0, default_val)
                entry.grid(row=i, column=1, padx=10, pady=10)
                setattr(self, field_name, entry)
            elif field_name.startswith("label"):
                label = ctk.CTkLabel(self.modify_window, text=str(default_val))
                label.grid(row=i, column=1, padx=10, pady=10, sticky="w")

        btn_frame = ctk.CTkFrame(self.modify_window)
        btn_frame.grid(row=len(campos)+1, column=0, columnspan=2, pady=20)

        ctk.CTkButton(btn_frame, text="Guardar", fg_color="green", command=lambda: self.update_categoria(item_data[0])).pack(side=tk.LEFT, padx=10)
        ctk.CTkButton(btn_frame, text="Cancelar", fg_color="red", command=self.modify_window.destroy).pack(side=tk.LEFT, padx=10)

    def update_categoria(self, id_categoria):
        """Actualiza una categoría existente en la base de datos"""
        nombre = self.entry_nombre.get().strip()
        descripcion = self.entry_desc.get().strip() or None

        if not nombre:
            messagebox.showerror("Error", "El nombre es obligatorio")
            return

        try:
            success = self.categoria_manejador.actualizar_categoria(
                id_categoria,
                tipo_identificador='id',
                nuevo_nombre=nombre,
                nueva_descripcion=descripcion
            )
            if success:
                messagebox.showinfo("Éxito", "Categoría actualizada correctamente")
                self.modify_window.destroy()
                self.load_categorias()
            else:
                messagebox.showerror("Error", "No se pudo actualizar la categoría. Verifique la consola para más detalles.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {str(e)}")

    def delete_categoria(self):
        """Elimina una categoría existente"""
        selected = self.tree_categorias.focus()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione una categoría para eliminar")
            return

        item_data = self.tree_categorias.item(selected)
        id_categoria = item_data['values'][0]
        nombre = item_data['values'][1]

        if not messagebox.askyesno("Confirmar Eliminación", f"¿Está seguro de eliminar la categoría:\n{nombre} (ID: {id_categoria})?"):
            return

        try:
            success = self.categoria_manejador.eliminar_categoria(id_categoria, 'id')
            if success:
                messagebox.showinfo("Éxito", "Categoría eliminada correctamente")
                self.load_categorias()
            else:
                messagebox.showerror("Error", "No se pudo eliminar la categoría. Verifique si está siendo referenciada en otras tablas (ej. productos).")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {str(e)}")

    # --- GESTIÓN DE PRODUCTOS ---
    def show_products(self):
        """Muestra la sección de gestión de productos"""
        self.clear_content()
        tk.Label(self.dynamic_content, text="Gestión de Productos", bg="#FDFBF6", fg="#1F2937", font=("Arial", 16, "bold")).pack(pady=10)

        # Botones de acción para productos
        button_frame = ctk.CTkFrame(self.dynamic_content)
        button_frame.pack(pady=(10, 20))

        ctk.CTkButton(button_frame, text="Agregar Producto", command=self.add_producto).pack(side=tk.LEFT, padx=5)
        ctk.CTkButton(button_frame, text="Modificar Producto", command=self.modify_producto).pack(side=tk.LEFT, padx=5)
        ctk.CTkButton(button_frame, text="Eliminar Producto", command=self.delete_producto).pack(side=tk.LEFT, padx=5)
        ctk.CTkButton(button_frame, text="Buscar Producto", command=self.search_product).pack(side=tk.LEFT, padx=5)

        # Treeview para mostrar productos
        columns = ("ID", "Nombre", "Descripción", "Costo Unitario", "Fecha Caducidad", "Cantidad", "Activo", "Unidad Medida", "Categoría", "Proveedor", "Stock Mínimo")
        self.tree_productos = ttk.Treeview(self.dynamic_content, columns=columns, show='headings', selectmode='browse')

        for col in columns:
            self.tree_productos.heading(col, text=col)
            self.tree_productos.column(col, anchor=tk.CENTER, width=100)
        
        self.tree_productos.column("Nombre", width=150)
        self.tree_productos.column("Descripción", width=200)
        self.tree_productos.column("Costo Unitario", width=100)
        self.tree_productos.column("Fecha Caducidad", width=120)
        self.tree_productos.column("Cantidad", width=80)
        self.tree_productos.column("Unidad Medida", width=100)
        self.tree_productos.column("Categoría", width=100)
        self.tree_productos.column("Proveedor", width=100)
        self.tree_productos.column("Stock Mínimo", width=100)

        scroll_y = ttk.Scrollbar(self.dynamic_content, orient=tk.VERTICAL, command=self.tree_productos.yview)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_productos.configure(yscrollcommand=scroll_y.set)
        self.tree_productos.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

        self.load_products()

    def load_products(self):
        """Carga los productos en el Treeview"""
        for item in self.tree_productos.get_children():
            self.tree_productos.delete(item)

        productos = self.productos_manejador.leer_todos_productos()

        for p in productos:
            estado = "Activo" if p['activo'] == 1 else "Inactivo"
            self.tree_productos.insert("", tk.END, values=(
                p['id_productos'],
                p['nombre_producto'],
                p['descripcion'] or "N/A",
                f"{p['costo_unitario']:.2f}",
                p['fecha_caducidad'] or "N/A",
                f"{p['cantidad']:.2f}",
                estado,
                p['unidad_medida'] + " (" + p['unidad_abreviatura'] + ")", # Combinar nombre y abreviatura
                p['categoria'],
                p['proveedor'],
                f"{p['stock_minimo_alerta']:.2f}" if p['stock_minimo_alerta'] is not None else "N/A"
            ))

    def add_producto(self):
        """Abre la ventana para agregar un nuevo producto"""
        self.add_window = ctk.CTkToplevel(self)
        self.add_window.title("Agregar Producto")
        self.add_window.geometry("550x500")
        self.add_window.grab_set()

        # Variables para los campos de selección
        self.prod_unidad_var = tk.StringVar()
        self.prod_categoria_var = tk.StringVar()
        self.prod_proveedor_var = tk.StringVar()
        self.selected_unidad_id = None
        self.selected_categoria_id = None
        self.selected_proveedor_id = None

        row_idx = 0
        ctk.CTkLabel(self.add_window, text="Nombre*:").grid(row=row_idx, column=0, padx=10, pady=5, sticky="e")
        self.entry_prod_nombre = ctk.CTkEntry(self.add_window, width=250)
        self.entry_prod_nombre.grid(row=row_idx, column=1, columnspan=2, padx=10, pady=5, sticky="ew")

        row_idx += 1
        ctk.CTkLabel(self.add_window, text="Descripción:").grid(row=row_idx, column=0, padx=10, pady=5, sticky="e")
        self.entry_prod_desc = ctk.CTkEntry(self.add_window, width=250)
        self.entry_prod_desc.grid(row=row_idx, column=1, columnspan=2, padx=10, pady=5, sticky="ew")

        row_idx += 1
        ctk.CTkLabel(self.add_window, text="Costo Unitario*:").grid(row=row_idx, column=0, padx=10, pady=5, sticky="e")
        self.entry_prod_costo = ctk.CTkEntry(self.add_window, width=250)
        self.entry_prod_costo.grid(row=row_idx, column=1, columnspan=2, padx=10, pady=5, sticky="ew")

        row_idx += 1
        ctk.CTkLabel(self.add_window, text="Fecha Caducidad (YYYY-MM-DD):").grid(row=row_idx, column=0, padx=10, pady=5, sticky="e")
        self.entry_prod_fecha = ctk.CTkEntry(self.add_window, width=250)
        self.entry_prod_fecha.grid(row=row_idx, column=1, columnspan=2, padx=10, pady=5, sticky="ew")

        row_idx += 1
        ctk.CTkLabel(self.add_window, text="Cantidad Inicial*:").grid(row=row_idx, column=0, padx=10, pady=5, sticky="e")
        self.entry_prod_cantidad = ctk.CTkEntry(self.add_window, width=250)
        self.entry_prod_cantidad.grid(row=row_idx, column=1, columnspan=2, padx=10, pady=5, sticky="ew")

        row_idx += 1
        ctk.CTkLabel(self.add_window, text="Stock Mínimo Alerta:").grid(row=row_idx, column=0, padx=10, pady=5, sticky="e")
        self.entry_prod_stock_min = ctk.CTkEntry(self.add_window, width=250)
        self.entry_prod_stock_min.grid(row=row_idx, column=1, columnspan=2, padx=10, pady=5, sticky="ew")

        row_idx += 1
        ctk.CTkLabel(self.add_window, text="Unidad de Medida*:").grid(row=row_idx, column=0, padx=10, pady=5, sticky="e")
        ctk.CTkButton(self.add_window, text="Seleccionar Unidad", command=self._select_unidad_for_product).grid(row=row_idx, column=1, padx=5, pady=5, sticky="w")
        ctk.CTkLabel(self.add_window, textvariable=self.prod_unidad_var).grid(row=row_idx, column=2, padx=5, pady=5, sticky="w")

        row_idx += 1
        ctk.CTkLabel(self.add_window, text="Categoría*:").grid(row=row_idx, column=0, padx=10, pady=5, sticky="e")
        ctk.CTkButton(self.add_window, text="Seleccionar Categoría", command=self._select_categoria_for_product).grid(row=row_idx, column=1, padx=5, pady=5, sticky="w")
        ctk.CTkLabel(self.add_window, textvariable=self.prod_categoria_var).grid(row=row_idx, column=2, padx=5, pady=5, sticky="w")

        row_idx += 1
        ctk.CTkLabel(self.add_window, text="Proveedor*:").grid(row=row_idx, column=0, padx=10, pady=5, sticky="e")
        ctk.CTkButton(self.add_window, text="Seleccionar Proveedor", command=self._select_proveedor_for_product).grid(row=row_idx, column=1, padx=5, pady=5, sticky="w")
        ctk.CTkLabel(self.add_window, textvariable=self.prod_proveedor_var).grid(row=row_idx, column=2, padx=5, pady=5, sticky="w")

        btn_frame = ctk.CTkFrame(self.add_window)
        btn_frame.grid(row=row_idx + 1, column=0, columnspan=3, pady=20)
        ctk.CTkButton(btn_frame, text="Guardar", fg_color="green", command=self.save_producto).pack(side=tk.LEFT, padx=10)
        ctk.CTkButton(btn_frame, text="Cancelar", fg_color="red", command=self.add_window.destroy).pack(side=tk.LEFT, padx=10)

    def _select_unidad_for_product(self):
        """Abre una ventana para seleccionar una unidad de medida para el producto"""
        select_window = ctk.CTkToplevel(self)
        select_window.title("Seleccionar Unidad de Medida")
        select_window.geometry("400x300")
        select_window.grab_set()

        columns = ("ID", "Nombre", "Abreviatura")
        tree = ttk.Treeview(select_window, columns=columns, show='headings', selectmode='browse')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor=tk.CENTER, width=100)
        tree.pack(fill=tk.BOTH, expand=True)

        unidades = self.unidad_medida_manejador.leer_unidades_medida()
        for u in unidades:
            tree.insert("", tk.END, values=(u['id_unidad_medida'], u['nombre_unidad_medida'], u['abreviatura']))

        def on_select():
            selected_item = tree.focus()
            if selected_item:
                item_data = tree.item(selected_item)['values']
                self.selected_unidad_id = item_data[0]
                self.prod_unidad_var.set(f"{item_data[1]} ({item_data[2]})")
                select_window.destroy()
            else:
                messagebox.showwarning("Advertencia", "Seleccione una unidad de medida.")

        ctk.CTkButton(select_window, text="Seleccionar", command=on_select).pack(pady=10)

    def _select_categoria_for_product(self):
        """Abre una ventana para seleccionar una categoría para el producto"""
        select_window = ctk.CTkToplevel(self)
        select_window.title("Seleccionar Categoría")
        select_window.geometry("400x300")
        select_window.grab_set()

        columns = ("ID", "Nombre")
        tree = ttk.Treeview(select_window, columns=columns, show='headings', selectmode='browse')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor=tk.CENTER, width=150)
        tree.pack(fill=tk.BOTH, expand=True)

        categorias = self.categoria_manejador.leer_todas_categorias()
        for c in categorias:
            tree.insert("", tk.END, values=(c['id_categorias'], c['nombre_categoria']))

        def on_select():
            selected_item = tree.focus()
            if selected_item:
                item_data = tree.item(selected_item)['values']
                self.selected_categoria_id = item_data[0]
                self.prod_categoria_var.set(item_data[1])
                select_window.destroy()
            else:
                messagebox.showwarning("Advertencia", "Seleccione una categoría.")

        ctk.CTkButton(select_window, text="Seleccionar", command=on_select).pack(pady=10)

    def _select_proveedor_for_product(self):
        """Abre una ventana para seleccionar un proveedor para el producto"""
        select_window = ctk.CTkToplevel(self)
        select_window.title("Seleccionar Proveedor")
        select_window.geometry("400x300")
        select_window.grab_set()

        columns = ("ID", "Nombre")
        tree = ttk.Treeview(select_window, columns=columns, show='headings', selectmode='browse')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor=tk.CENTER, width=150)
        tree.pack(fill=tk.BOTH, expand=True)

        proveedores = self.proveedor_manejador.leer_todos_proveedores()
        for p in proveedores:
            tree.insert("", tk.END, values=(p['id_proveedor'], p['nombre_proveedor']))

        def on_select():
            selected_item = tree.focus()
            if selected_item:
                item_data = tree.item(selected_item)['values']
                self.selected_proveedor_id = item_data[0]
                self.prod_proveedor_var.set(item_data[1])
                select_window.destroy()
            else:
                messagebox.showwarning("Advertencia", "Seleccione un proveedor.")

        ctk.CTkButton(select_window, text="Seleccionar", command=on_select).pack(pady=10)

    def save_producto(self):
        """Guarda un nuevo producto en la base de datos"""
        nombre = self.entry_prod_nombre.get().strip()
        descripcion = self.entry_prod_desc.get().strip() or None
        costo_unitario_str = self.entry_prod_costo.get().strip()
        fecha_caducidad = self.entry_prod_fecha.get().strip() or None
        cantidad_str = self.entry_prod_cantidad.get().strip()
        stock_minimo_str = self.entry_prod_stock_min.get().strip() or None

        if not nombre or not costo_unitario_str or not cantidad_str or \
           self.selected_unidad_id is None or self.selected_categoria_id is None or self.selected_proveedor_id is None:
            messagebox.showerror("Error", "Nombre, Costo Unitario, Cantidad, Unidad de Medida, Categoría y Proveedor son obligatorios.")
            return

        try:
            costo_unitario = float(costo_unitario_str)
            cantidad = float(cantidad_str)
            stock_minimo = float(stock_minimo_str) if stock_minimo_str else None
        except ValueError:
            messagebox.showerror("Error", "Costo Unitario, Cantidad y Stock Mínimo deben ser números válidos.")
            return
        
        if fecha_caducidad:
            try:
                datetime.strptime(fecha_caducidad, '%Y-%m-%d')
            except ValueError:
                messagebox.showerror("Error", "Formato de fecha de caducidad inválido. Use YYYY-MM-DD.")
                return

        try:
            nuevo_id = self.productos_manejador.crear_producto(
                nombre, descripcion, costo_unitario, self.selected_unidad_id, 
                self.selected_categoria_id, self.selected_proveedor_id, 
                fecha_caducidad, cantidad, stock_minimo
            )

            if nuevo_id is not None:
                messagebox.showinfo("Éxito", f"Producto '{nombre}' creado con ID: {nuevo_id}")
                self.add_window.destroy()
                self.load_products()
            else:
                messagebox.showerror("Error", "No se pudo crear el producto. Verifique la consola para más detalles.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {str(e)}")

    def modify_producto(self):
        """Abre la ventana para modificar un producto existente"""
        selected = self.tree_productos.focus()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un producto para modificar")
            return

        item_data = self.tree_productos.item(selected)['values']
        id_producto = item_data[0]
        
        producto_data = self.productos_manejador.leer_producto_por_id(id_producto)
        if not producto_data:
            messagebox.showerror("Error", "No se pudo cargar la información del producto seleccionado.")
            return

        self.modify_window = ctk.CTkToplevel(self)
        self.modify_window.title("Modificar Producto")
        self.modify_window.geometry("550x500")
        self.modify_window.grab_set()

        # Variables para los campos de selección (con valores actuales)
        self.mod_prod_unidad_var = tk.StringVar(value=f"{producto_data['unidad_medida']} ({producto_data['unidad_abreviatura']})")
        self.mod_prod_categoria_var = tk.StringVar(value=producto_data['categoria'])
        self.mod_prod_proveedor_var = tk.StringVar(value=producto_data['proveedor'])
        self.selected_mod_unidad_id = producto_data['id_unidad_medida']
        self.selected_mod_categoria_id = producto_data['id_categorias']
        self.selected_mod_proveedor_id = producto_data['id_proveedor']

        row_idx = 0
        ctk.CTkLabel(self.modify_window, text="ID Producto:").grid(row=row_idx, column=0, padx=10, pady=5, sticky="e")
        ctk.CTkLabel(self.modify_window, text=str(id_producto)).grid(row=row_idx, column=1, columnspan=2, padx=10, pady=5, sticky="ew")

        row_idx += 1
        ctk.CTkLabel(self.modify_window, text="Nombre*:").grid(row=row_idx, column=0, padx=10, pady=5, sticky="e")
        self.entry_mod_prod_nombre = ctk.CTkEntry(self.modify_window, width=250)
        self.entry_mod_prod_nombre.insert(0, producto_data['nombre_producto'])
        self.entry_mod_prod_nombre.grid(row=row_idx, column=1, columnspan=2, padx=10, pady=5, sticky="ew")

        row_idx += 1
        ctk.CTkLabel(self.modify_window, text="Descripción:").grid(row=row_idx, column=0, padx=10, pady=5, sticky="e")
        self.entry_mod_prod_desc = ctk.CTkEntry(self.modify_window, width=250)
        self.entry_mod_prod_desc.insert(0, producto_data['descripcion'] or "")
        self.entry_mod_prod_desc.grid(row=row_idx, column=1, columnspan=2, padx=10, pady=5, sticky="ew")

        row_idx += 1
        ctk.CTkLabel(self.modify_window, text="Costo Unitario*:").grid(row=row_idx, column=0, padx=10, pady=5, sticky="e")
        self.entry_mod_prod_costo = ctk.CTkEntry(self.modify_window, width=250)
        self.entry_mod_prod_costo.insert(0, str(producto_data['costo_unitario']))
        self.entry_mod_prod_costo.grid(row=row_idx, column=1, columnspan=2, padx=10, pady=5, sticky="ew")

        row_idx += 1
        ctk.CTkLabel(self.modify_window, text="Fecha Caducidad (YYYY-MM-DD):").grid(row=row_idx, column=0, padx=10, pady=5, sticky="e")
        self.entry_mod_prod_fecha = ctk.CTkEntry(self.modify_window, width=250)
        self.entry_mod_prod_fecha.insert(0, producto_data['fecha_caducidad'] or "")
        self.entry_mod_prod_fecha.grid(row=row_idx, column=1, columnspan=2, padx=10, pady=5, sticky="ew")

        row_idx += 1
        ctk.CTkLabel(self.modify_window, text="Cantidad*:").grid(row=row_idx, column=0, padx=10, pady=5, sticky="e")
        self.entry_mod_prod_cantidad = ctk.CTkEntry(self.modify_window, width=250)
        self.entry_mod_prod_cantidad.insert(0, str(producto_data['cantidad']))
        self.entry_mod_prod_cantidad.grid(row=row_idx, column=1, columnspan=2, padx=10, pady=5, sticky="ew")

        row_idx += 1
        ctk.CTkLabel(self.modify_window, text="Stock Mínimo Alerta:").grid(row=row_idx, column=0, padx=10, pady=5, sticky="e")
        self.entry_mod_prod_stock_min = ctk.CTkEntry(self.modify_window, width=250)
        self.entry_mod_prod_stock_min.insert(0, str(producto_data['stock_minimo_alerta'] or ""))
        self.entry_mod_prod_stock_min.grid(row=row_idx, column=1, columnspan=2, padx=10, pady=5, sticky="ew")

        row_idx += 1
        ctk.CTkLabel(self.modify_window, text="Unidad de Medida*:").grid(row=row_idx, column=0, padx=10, pady=5, sticky="e")
        ctk.CTkButton(self.modify_window, text="Seleccionar Unidad", command=lambda: self._select_unidad_for_product(modify=True)).grid(row=row_idx, column=1, padx=5, pady=5, sticky="w")
        ctk.CTkLabel(self.modify_window, textvariable=self.mod_prod_unidad_var).grid(row=row_idx, column=2, padx=5, pady=5, sticky="w")

        row_idx += 1
        ctk.CTkLabel(self.modify_window, text="Categoría*:").grid(row=row_idx, column=0, padx=10, pady=5, sticky="e")
        ctk.CTkButton(self.modify_window, text="Seleccionar Categoría", command=lambda: self._select_categoria_for_product(modify=True)).grid(row=row_idx, column=1, padx=5, pady=5, sticky="w")
        ctk.CTkLabel(self.modify_window, textvariable=self.mod_prod_categoria_var).grid(row=row_idx, column=2, padx=5, pady=5, sticky="w")

        row_idx += 1
        ctk.CTkLabel(self.modify_window, text="Proveedor*:").grid(row=row_idx, column=0, padx=10, pady=5, sticky="e")
        ctk.CTkButton(self.modify_window, text="Seleccionar Proveedor", command=lambda: self._select_proveedor_for_product(modify=True)).grid(row=row_idx, column=1, padx=5, pady=5, sticky="w")
        ctk.CTkLabel(self.modify_window, textvariable=self.mod_prod_proveedor_var).grid(row=row_idx, column=2, padx=5, pady=5, sticky="w")

        btn_frame = ctk.CTkFrame(self.modify_window)
        btn_frame.grid(row=row_idx + 1, column=0, columnspan=3, pady=20)
        ctk.CTkButton(btn_frame, text="Guardar Cambios", fg_color="green", command=lambda: self.update_producto(id_producto)).pack(side=tk.LEFT, padx=10)
        ctk.CTkButton(btn_frame, text="Cancelar", fg_color="red", command=self.modify_window.destroy).pack(side=tk.LEFT, padx=10)

    def _select_unidad_for_product(self, modify=False):
        """Abre una ventana para seleccionar una unidad de medida para el producto (para agregar o modificar)"""
        select_window = ctk.CTkToplevel(self)
        select_window.title("Seleccionar Unidad de Medida")
        select_window.geometry("400x300")
        select_window.grab_set()

        columns = ("ID", "Nombre", "Abreviatura")
        tree = ttk.Treeview(select_window, columns=columns, show='headings', selectmode='browse')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor=tk.CENTER, width=100)
        tree.pack(fill=tk.BOTH, expand=True)

        unidades = self.unidad_medida_manejador.leer_unidades_medida()
        for u in unidades:
            tree.insert("", tk.END, values=(u['id_unidad_medida'], u['nombre_unidad_medida'], u['abreviatura']))

        def on_select():
            selected_item = tree.focus()
            if selected_item:
                item_data = tree.item(selected_item)['values']
                if modify:
                    self.selected_mod_unidad_id = item_data[0]
                    self.mod_prod_unidad_var.set(f"{item_data[1]} ({item_data[2]})")
                else:
                    self.selected_unidad_id = item_data[0]
                    self.prod_unidad_var.set(f"{item_data[1]} ({item_data[2]})")
                select_window.destroy()
            else:
                messagebox.showwarning("Advertencia", "Seleccione una unidad de medida.")

        ctk.CTkButton(select_window, text="Seleccionar", command=on_select).pack(pady=10)

    def _select_categoria_for_product(self, modify=False):
        """Abre una ventana para seleccionar una categoría para el producto (para agregar o modificar)"""
        select_window = ctk.CTkToplevel(self)
        select_window.title("Seleccionar Categoría")
        select_window.geometry("400x300")
        select_window.grab_set()

        columns = ("ID", "Nombre")
        tree = ttk.Treeview(select_window, columns=columns, show='headings', selectmode='browse')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor=tk.CENTER, width=150)
        tree.pack(fill=tk.BOTH, expand=True)

        categorias = self.categoria_manejador.leer_todas_categorias()
        for c in categorias:
            tree.insert("", tk.END, values=(c['id_categorias'], c['nombre_categoria']))

        def on_select():
            selected_item = tree.focus()
            if selected_item:
                item_data = tree.item(selected_item)['values']
                if modify:
                    self.selected_mod_categoria_id = item_data[0]
                    self.mod_prod_categoria_var.set(item_data[1])
                else:
                    self.selected_categoria_id = item_data[0]
                    self.prod_categoria_var.set(item_data[1])
                select_window.destroy()
            else:
                messagebox.showwarning("Advertencia", "Seleccione una categoría.")

        ctk.CTkButton(select_window, text="Seleccionar", command=on_select).pack(pady=10)

    def _select_proveedor_for_product(self, modify=False):
        """Abre una ventana para seleccionar un proveedor para el producto (para agregar o modificar)"""
        select_window = ctk.CTkToplevel(self)
        select_window.title("Seleccionar Proveedor")
        select_window.geometry("400x300")
        select_window.grab_set()

        columns = ("ID", "Nombre")
        tree = ttk.Treeview(select_window, columns=columns, show='headings', selectmode='browse')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor=tk.CENTER, width=150)
        tree.pack(fill=tk.BOTH, expand=True)

        proveedores = self.proveedor_manejador.leer_todos_proveedores()
        for p in proveedores:
            tree.insert("", tk.END, values=(p['id_proveedor'], p['nombre_proveedor']))

        def on_select():
            selected_item = tree.focus()
            if selected_item:
                item_data = tree.item(selected_item)['values']
                if modify:
                    self.selected_mod_proveedor_id = item_data[0]
                    self.mod_prod_proveedor_var.set(item_data[1])
                else:
                    self.selected_proveedor_id = item_data[0]
                    self.prod_proveedor_var.set(item_data[1])
                select_window.destroy()
            else:
                messagebox.showwarning("Advertencia", "Seleccione un proveedor.")

        ctk.CTkButton(select_window, text="Seleccionar", command=on_select).pack(pady=10)

    def update_producto(self, id_producto):
        """Actualiza un producto existente en la base de datos"""
        nombre = self.entry_mod_prod_nombre.get().strip()
        descripcion = self.entry_mod_prod_desc.get().strip() or None
        costo_unitario_str = self.entry_mod_prod_costo.get().strip()
        fecha_caducidad = self.entry_mod_prod_fecha.get().strip() or None
        cantidad_str = self.entry_mod_prod_cantidad.get().strip()
        stock_minimo_str = self.entry_mod_prod_stock_min.get().strip() or None

        if not nombre or not costo_unitario_str or not cantidad_str or \
           self.selected_mod_unidad_id is None or self.selected_mod_categoria_id is None or self.selected_mod_proveedor_id is None:
            messagebox.showerror("Error", "Nombre, Costo Unitario, Cantidad, Unidad de Medida, Categoría y Proveedor son obligatorios.")
            return

        try:
            costo_unitario = float(costo_unitario_str)
            cantidad = float(cantidad_str)
            stock_minimo = float(stock_minimo_str) if stock_minimo_str else None
        except ValueError:
            messagebox.showerror("Error", "Costo Unitario, Cantidad y Stock Mínimo deben ser números válidos.")
            return
        
        if fecha_caducidad:
            try:
                datetime.strptime(fecha_caducidad, '%Y-%m-%d')
            except ValueError:
                messagebox.showerror("Error", "Formato de fecha de caducidad inválido. Use YYYY-MM-DD.")
                return

        try:
            success = self.productos_manejador.actualizar_producto(
                id_producto, 
                'id', # Tipo de identificador
                nuevo_nombre=nombre, 
                nueva_descripcion=descripcion, 
                nuevo_costo_unitario=costo_unitario, 
                nueva_fecha_caducidad=fecha_caducidad, 
                nueva_cantidad=cantidad, 
                nuevo_stock_minimo_alerta=stock_minimo,
                nuevo_id_unidad_medida=self.selected_mod_unidad_id,
                nuevo_id_categorias=self.selected_mod_categoria_id,
                nuevo_id_proveedor=self.selected_mod_proveedor_id
            )

            if success:
                messagebox.showinfo("Éxito", f"Producto '{nombre}' actualizado correctamente")
                self.modify_window.destroy()
                self.load_products()
            else:
                messagebox.showerror("Error", "No se pudo actualizar el producto. Verifique la consola para más detalles.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {str(e)}")

    def delete_producto(self):
        """Elimina un producto existente"""
        selected = self.tree_productos.focus()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un producto para eliminar")
            return

        item_data = self.tree_productos.item(selected)
        id_producto = item_data['values'][0]
        nombre = item_data['values'][1]

        if not messagebox.askyesno("Confirmar Eliminación", f"¿Está seguro de eliminar el producto:\n{nombre} (ID: {id_producto})?"):
            return

        try:
            success = self.productos_manejador.eliminar_producto(id_producto, 'id')
            if success:
                messagebox.showinfo("Éxito", "Producto eliminado correctamente")
                self.load_products()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el producto. Verifique si está siendo referenciado en otras tablas (ej. inventario, movimientos).")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {str(e)}")

    def search_product(self):
        """Abre la ventana para buscar un producto por nombre"""
        search_window = ctk.CTkToplevel(self)
        search_window.title("Buscar Producto")
        search_window.geometry("400x200")
        search_window.grab_set()

        ctk.CTkLabel(search_window, text="Nombre del Producto:").pack(pady=(20, 5))

        self.search_entry = ctk.CTkEntry(search_window, width=300)
        self.search_entry.pack(pady=5)

        ctk.CTkButton(search_window, text="Buscar", command=self.execute_search).pack(pady=20)

    def execute_search(self):
        """Ejecuta la búsqueda de un producto y lo selecciona en el Treeview"""
        nombre = self.search_entry.get().strip()
        if not nombre:
            messagebox.showwarning("Advertencia", "Ingrese un nombre para buscar")
            return

        try:
            resultado = self.productos_manejador.leer_producto_por_nombre(nombre)
        
            if resultado:
                # Limpiar selección actual
                self.tree_productos.selection_remove(self.tree_productos.selection())
                # Buscar y seleccionar el item en el treeview
                for item in self.tree_productos.get_children():
                    if self.tree_productos.item(item, 'values')[0] == resultado['id_productos']: # Comparar por ID
                        self.tree_productos.selection_set(item)
                        self.tree_productos.focus(item)
                        self.tree_productos.see(item) # Asegura que el item sea visible
                        messagebox.showinfo("Búsqueda Exitosa", f"Producto '{nombre}' encontrado y seleccionado.")
                        self.search_entry.master.destroy() # Cierra la ventana de búsqueda
                        return
                messagebox.showinfo("Resultado", "El producto fue encontrado en la base de datos, pero no visible en la tabla actual (puede estar filtrado o no cargado).")
            else:
                messagebox.showinfo("Resultado", f"No se encontró el producto con nombre '{nombre}'.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error en la búsqueda: {str(e)}")

    # --- GESTIÓN DE MOVIMIENTOS ---
    def show_movements(self):
        """Muestra la sección de gestión de movimientos de inventario"""
        self.clear_content()
        tk.Label(self.dynamic_content, text="Historial de Movimientos de Inventario", bg="#FDFBF6", fg="#1F2937", font=("Arial", 16, "bold")).pack(pady=10)

        # Botones de acción para movimientos
        button_frame = ctk.CTkFrame(self.dynamic_content)
        button_frame.pack(pady=(10, 20))

        ctk.CTkButton(button_frame, text="Registrar Nuevo Movimiento", command=self.add_movimiento).pack(side=tk.LEFT, padx=5)

        # Treeview para mostrar movimientos
        columns = ("ID Mov.", "Tipo", "Producto", "Cantidad", "Ubicación Origen", "Ubicación Destino", "Fecha", "Referencia Doc.", "Centro Costos")
        self.tree_movimientos = ttk.Treeview(self.dynamic_content, columns=columns, show='headings', selectmode='browse')

        for col in columns:
            self.tree_movimientos.heading(col, text=col)
            self.tree_movimientos.column(col, anchor=tk.CENTER, width=100)
        
        self.tree_movimientos.column("Tipo", width=120)
        self.tree_movimientos.column("Producto", width=150)
        self.tree_movimientos.column("Cantidad", width=80)
        self.tree_movimientos.column("Ubicación Origen", width=120)
        self.tree_movimientos.column("Ubicación Destino", width=120)
        self.tree_movimientos.column("Fecha", width=150)
        self.tree_movimientos.column("Referencia Doc.", width=120)
        self.tree_movimientos.column("Centro Costos", width=120)

        scroll_y = ttk.Scrollbar(self.dynamic_content, orient=tk.VERTICAL, command=self.tree_movimientos.yview)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_movimientos.configure(yscrollcommand=scroll_y.set)
        self.tree_movimientos.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

        self.load_movimientos()

    def load_movimientos(self):
        """Carga los movimientos en el Treeview"""
        for item in self.tree_movimientos.get_children():
            self.tree_movimientos.delete(item)
        
        movimientos = self.movimientos_manejador.leer_todos_los_movimientos()
        
        for mov in movimientos:
            ubicacion_destino_str = mov['ubicacion_destino'] if mov['ubicacion_destino'] else "N/A"
            self.tree_movimientos.insert("", tk.END, values=(
                mov['id'],
                mov['tipo_movimiento'],
                mov['nombre_producto'],
                f"{mov['cantidad']:.2f}",
                mov['ubicacion_origen'],
                ubicacion_destino_str,
                mov['fecha_movimiento'],
                mov['referencia_documento'] or "N/A",
                mov['centro_costos']
            ))

    def add_movimiento(self):
        """Abre la ventana para registrar un nuevo movimiento"""
        self.add_window = ctk.CTkToplevel(self)
        self.add_window.title("Registrar Nuevo Movimiento")
        self.add_window.geometry("600x550")
        self.add_window.grab_set()

        # Variables para los campos
        self.mov_producto_var = tk.StringVar()
        self.mov_cantidad_entry = ctk.CTkEntry(self.add_window)
        self.mov_centro_costo_var = tk.StringVar()
        self.mov_ubicacion_origen_var = tk.StringVar()
        self.mov_tipo_movimiento_var = ctk.StringVar(value="ENTRADA") # Valor por defecto
        self.mov_ubicacion_destino_var = tk.StringVar()
        self.mov_referencia_entry = ctk.CTkEntry(self.add_window)
        self.mov_observaciones_entry = ctk.CTkEntry(self.add_window)

        # IDs seleccionados
        self.selected_mov_product_id = None
        self.selected_mov_centro_costo_id = None
        self.selected_mov_ubicacion_origen_id = None
        self.selected_mov_ubicacion_destino_id = None

        row_idx = 0
        ctk.CTkLabel(self.add_window, text="Producto*:").grid(row=row_idx, column=0, padx=10, pady=5, sticky="e")
        ctk.CTkButton(self.add_window, text="Seleccionar Producto", command=self._select_product_for_movement).grid(row=row_idx, column=1, padx=10, pady=5, sticky="w")
        ctk.CTkLabel(self.add_window, textvariable=self.mov_producto_var).grid(row=row_idx, column=2, padx=10, pady=5, sticky="w")

        row_idx += 1
        ctk.CTkLabel(self.add_window, text="Cantidad*:").grid(row=row_idx, column=0, padx=10, pady=5, sticky="e")
        self.mov_cantidad_entry.grid(row=row_idx, column=1, columnspan=2, padx=10, pady=5, sticky="ew")

        row_idx += 1
        ctk.CTkLabel(self.add_window, text="Centro de Costos*:").grid(row=row_idx, column=0, padx=10, pady=5, sticky="e")
        ctk.CTkButton(self.add_window, text="Seleccionar Centro", command=self._select_centro_costo_for_movement).grid(row=row_idx, column=1, padx=10, pady=5, sticky="w")
        ctk.CTkLabel(self.add_window, textvariable=self.mov_centro_costo_var).grid(row=row_idx, column=2, padx=10, pady=5, sticky="w")

        row_idx += 1
        ctk.CTkLabel(self.add_window, text="Ubicación Origen*:").grid(row=row_idx, column=0, padx=10, pady=5, sticky="e")
        ctk.CTkButton(self.add_window, text="Seleccionar Origen", command=lambda: self._select_ubicacion_for_movement('origen')).grid(row=row_idx, column=1, padx=10, pady=5, sticky="w")
        ctk.CTkLabel(self.add_window, textvariable=self.mov_ubicacion_origen_var).grid(row=row_idx, column=2, padx=10, pady=5, sticky="w")

        row_idx += 1
        ctk.CTkLabel(self.add_window, text="Tipo de Movimiento*:").grid(row=row_idx, column=0, padx=10, pady=5, sticky="e")
        self.mov_tipo_movimiento_optionmenu = ctk.CTkOptionMenu(self.add_window, variable=self.mov_tipo_movimiento_var, values=self.movimientos_manejador.MOVIMIENTO_TIPOS, command=self._toggle_ubicacion_destino)
        self.mov_tipo_movimiento_optionmenu.grid(row=row_idx, column=1, columnspan=2, padx=10, pady=5, sticky="ew")

        row_idx += 1
        self.label_ubicacion_destino = ctk.CTkLabel(self.add_window, text="Ubicación Destino:")
        self.label_ubicacion_destino.grid(row=row_idx, column=0, padx=10, pady=5, sticky="e")
        self.btn_ubicacion_destino = ctk.CTkButton(self.add_window, text="Seleccionar Destino", command=lambda: self._select_ubicacion_for_movement('destino'))
        self.btn_ubicacion_destino.grid(row=row_idx, column=1, padx=10, pady=5, sticky="w")
        self.display_ubicacion_destino = ctk.CTkLabel(self.add_window, textvariable=self.mov_ubicacion_destino_var)
        self.display_ubicacion_destino.grid(row=row_idx, column=2, padx=10, pady=5, sticky="w")
        self._toggle_ubicacion_destino(self.mov_tipo_movimiento_var.get()) # Inicializar visibilidad

        row_idx += 1
        ctk.CTkLabel(self.add_window, text="Referencia Documento:").grid(row=row_idx, column=0, padx=10, pady=5, sticky="e")
        self.mov_referencia_entry.grid(row=row_idx, column=1, columnspan=2, padx=10, pady=5, sticky="ew")

        row_idx += 1
        ctk.CTkLabel(self.add_window, text="Observaciones:").grid(row=row_idx, column=0, padx=10, pady=5, sticky="e")
        self.mov_observaciones_entry.grid(row=row_idx, column=1, columnspan=2, padx=10, pady=5, sticky="ew")

        # Botones de acción
        btn_frame = ctk.CTkFrame(self.add_window)
        btn_frame.grid(row=row_idx + 1, column=0, columnspan=3, pady=20)

        ctk.CTkButton(btn_frame, text="Registrar", fg_color="green", command=self._save_movimiento).pack(side=tk.LEFT, padx=10)
        ctk.CTkButton(btn_frame, text="Cancelar", fg_color="red", command=self.add_window.destroy).pack(side=tk.LEFT, padx=10)

    def _toggle_ubicacion_destino(self, selected_type):
        """Muestra u oculta el campo de Ubicación Destino según el tipo de movimiento"""
        if selected_type == 'TRANSFERENCIA':
            self.label_ubicacion_destino.grid()
            self.btn_ubicacion_destino.grid()
            self.display_ubicacion_destino.grid()
        else:
            self.label_ubicacion_destino.grid_remove()
            self.btn_ubicacion_destino.grid_remove()
            self.display_ubicacion_destino.grid_remove()
            self.mov_ubicacion_destino_var.set("")
            self.selected_mov_ubicacion_destino_id = None

    def _select_product_for_movement(self):
        """Abre una ventana para seleccionar un producto para el movimiento"""
        select_window = ctk.CTkToplevel(self)
        select_window.title("Seleccionar Producto")
        select_window.geometry("600x400")
        select_window.grab_set()

        columns = ("ID", "Nombre", "Unidad", "Costo")
        tree = ttk.Treeview(select_window, columns=columns, show='headings', selectmode='browse')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor=tk.CENTER, width=100)
        tree.pack(fill=tk.BOTH, expand=True)

        productos = self.productos_manejador.leer_todos_productos()
        for p in productos:
            tree.insert("", tk.END, values=(p['id_productos'], p['nombre_producto'], p['unidad_abreviatura'], f"{p['costo_unitario']:.2f}"))

        def on_select():
            selected_item = tree.focus()
            if selected_item:
                item_data = tree.item(selected_item)['values']
                self.selected_mov_product_id = item_data[0]
                self.mov_producto_var.set(item_data[1])
                select_window.destroy()
            else:
                messagebox.showwarning("Advertencia", "Seleccione un producto.")

        ctk.CTkButton(select_window, text="Seleccionar", command=on_select).pack(pady=10)

    def _select_centro_costo_for_movement(self):
        """Abre una ventana para seleccionar un centro de costos para el movimiento"""
        select_window = ctk.CTkToplevel(self)
        select_window.title("Seleccionar Centro de Costos")
        select_window.geometry("400x300")
        select_window.grab_set()

        columns = ("ID", "Nombre")
        tree = ttk.Treeview(select_window, columns=columns, show='headings', selectmode='browse')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor=tk.CENTER, width=150)
        tree.pack(fill=tk.BOTH, expand=True)

        centros = self.centros_costos_manejador.leer_todos_centros_costo()
        for cc in centros:
            tree.insert("", tk.END, values=(cc['id_centro_costos'], cc['nombre_centro']))

        def on_select():
            selected_item = tree.focus()
            if selected_item:
                item_data = tree.item(selected_item)['values']
                self.selected_mov_centro_costo_id = item_data[0]
                self.mov_centro_costo_var.set(item_data[1])
                select_window.destroy()
            else:
                messagebox.showwarning("Advertencia", "Seleccione un centro de costos.")

        ctk.CTkButton(select_window, text="Seleccionar", command=on_select).pack(pady=10)

    def _select_ubicacion_for_movement(self, tipo: str): # tipo puede ser 'origen' o 'destino'
        """Abre una ventana para seleccionar una ubicación (origen o destino) para el movimiento"""
        select_window = ctk.CTkToplevel(self)
        select_window.title(f"Seleccionar Ubicación {tipo.capitalize()}")
        select_window.geometry("400x300")
        select_window.grab_set()

        columns = ("ID", "Nombre", "Capacidad", "Ocupado")
        tree = ttk.Treeview(select_window, columns=columns, show='headings', selectmode='browse')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor=tk.CENTER, width=100)
        tree.pack(fill=tk.BOTH, expand=True)

        ubicaciones = self.ubicacion_almacen_manejador.leer_todas_ubicaciones()
        for ub in ubicaciones:
            tree.insert("", tk.END, values=(ub['id_ubicacion'], ub['nombre_ubicacion'], f"{ub['capacidad_total']:.2f}", f"{ub['espacio_ocupado']:.2f}"))

        def on_select():
            selected_item = tree.focus()
            if selected_item:
                item_data = tree.item(selected_item)['values']
                if tipo == 'origen':
                    self.selected_mov_ubicacion_origen_id = item_data[0]
                    self.mov_ubicacion_origen_var.set(item_data[1])
                else: # destino
                    self.selected_mov_ubicacion_destino_id = item_data[0]
                    self.mov_ubicacion_destino_var.set(item_data[1])
                select_window.destroy()
            else:
                messagebox.showwarning("Advertencia", "Seleccione una ubicación.")

        ctk.CTkButton(select_window, text="Seleccionar", command=on_select).pack(pady=10)

    def _save_movimiento(self):
        """Guarda un nuevo movimiento en la base de datos"""
        try:
            id_producto = self.selected_mov_product_id
            cantidad_str = self.mov_cantidad_entry.get().strip()
            id_centro = self.selected_mov_centro_costo_id
            id_ubicacion_origen = self.selected_mov_ubicacion_origen_id
            tipo_movimiento = self.mov_tipo_movimiento_var.get()
            id_ubicacion_destino = self.selected_mov_ubicacion_destino_id if tipo_movimiento == 'TRANSFERENCIA' else None
            referencia_documento = self.mov_referencia_entry.get().strip() or None
            observaciones = self.mov_observaciones_entry.get().strip() or None

            if not id_producto or not cantidad_str or not id_centro or not id_ubicacion_origen:
                messagebox.showerror("Error", "Producto, Cantidad, Centro de Costos y Ubicación Origen son obligatorios.")
                return
            
            if tipo_movimiento == 'TRANSFERENCIA' and not id_ubicacion_destino:
                messagebox.showerror("Error", "Para TRANSFERENCIA, la Ubicación Destino es obligatoria.")
                return

            try:
                cantidad = float(cantidad_str)
                if cantidad <= 0:
                    messagebox.showerror("Error", "La cantidad debe ser un número positivo.")
                    return
            except ValueError:
                messagebox.showerror("Error", "La cantidad debe ser un número válido.")
                return

            success = self.movimientos_manejador.crear_movimiento(
                id_producto, cantidad, id_centro, id_ubicacion_origen,
                tipo_movimiento, id_ubicacion_destino, referencia_documento, observaciones
            )

            if success:
                messagebox.showinfo("Éxito", "Movimiento registrado exitosamente.")
                self.add_window.destroy()
                self.load_movimientos()
                # Opcional: Recargar inventario y ubicaciones para reflejar cambios
                # self.inventario_ubicacion_manejador.mostrar_todo_inventario() 
                # self.ubicacion_almacen_manejador.mostrar_todas_ubicaciones() 
            else:
                messagebox.showerror("Error", "No se pudo registrar el movimiento. Verifique los datos y los mensajes de error en consola.")

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {str(e)}")

    # --- GESTIÓN DE ALMACÉN ---
    def show_warehouse(self):
        """Muestra la sección de gestión de almacén"""
        self.clear_content()
        tk.Label(
            self.dynamic_content,
            text="Gestión de Almacén",
            bg="#FDFBF6",
            fg="#1F2937",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        # Frame para botones de selección de sub-módulos
        button_frame = ctk.CTkFrame(self.dynamic_content)
        button_frame.pack(pady=(10, 20))

        ctk.CTkButton(
            button_frame,
            text="Gestionar Ubicaciones",
            command=self.show_ubicaciones_almacen,
            width=250,
            height=40,
            font=("Arial", 16, "bold")
        ).pack(side=tk.LEFT, padx=10)

        ctk.CTkButton(
            button_frame,
            text="Gestionar Inventario por Ubicación",
            command=self.show_inventario_por_ubicacion,
            width=250,
            height=40,
            font=("Arial", 16, "bold")
        ).pack(side=tk.LEFT, padx=10)

        self.warehouse_message = tk.Label(
            self.dynamic_content,
            text="Seleccione una opción para administrar el almacén",
            bg="#FDFBF6",
            fg="#1F2937",
            font=("Arial", 16)
        )
        self.warehouse_message.pack(pady=50)

    def clear_content_except_buttons(self):
        """Limpia el contenido dinámico, manteniendo los botones de selección de catálogo/almacén"""
        # Obtener los widgets que son los botones de selección de catálogo/almacén
        # y el título de la sección principal (Gestión de Catálogos/Almacén)
        widgets_to_keep = []
        if hasattr(self, 'btn_select_catalog'): # Para catálogos
            widgets_to_keep.append(self.btn_select_catalog.master) # El frame que contiene los botones
            widgets_to_keep.append(self.dynamic_content.winfo_children()[0]) # El título "Gestión de Catálogos"
        elif hasattr(self, 'warehouse_message') and self.warehouse_message.winfo_exists(): # Para almacén
            # Si estamos en la pantalla de almacén, los botones de "Gestionar Ubicaciones"
            # y "Gestionar Inventario" están en un frame, y el título de la sección.
            # Necesitamos limpiar todo lo que se añadió DESPUÉS de esos botones.
            # La forma más sencilla es recrear el contenido dinámico o destruir todo y volver a añadir los botones.
            # Para simplificar, si ya estamos en una sub-sección (ubicaciones/inventario),
            # simplemente destruimos todo y volvemos a añadir el título y los botones CRUD específicos.
            pass # La lógica de show_ubicaciones_almacen/show_inventario_por_ubicacion ya maneja esto.

        for widget in self.dynamic_content.winfo_children():
            if widget not in widgets_to_keep:
                widget.destroy()

    # --- GESTIÓN DE UBICACIONES DE ALMACÉN ---
    def show_ubicaciones_almacen(self):
        """Muestra la interfaz para gestionar ubicaciones de almacén"""
        if hasattr(self, 'warehouse_message'):
            self.warehouse_message.pack_forget()
        
        # Limpiar contenido previo si existe (excepto el título principal de "Gestión de Almacén" y sus botones de sub-módulo)
        # Una forma más robusta es limpiar todo y recrear la sección.
        self.clear_content() 
        self.show_warehouse() # Recrea el título y los botones de sub-módulo
        
        # Ahora, limpiar el mensaje inicial de warehouse y añadir el título específico
        if hasattr(self, 'warehouse_message'):
            self.warehouse_message.pack_forget()

        tk.Label(
            self.dynamic_content,
            text="Gestión de Ubicaciones de Almacén",
            bg="#FDFBF6",
            fg="#1F2937",
            font=("Arial", 14, "bold")
        ).pack(pady=(10, 0))

        # Botones CRUD para Ubicaciones
        crud_button_frame = ctk.CTkFrame(self.dynamic_content)
        crud_button_frame.pack(pady=(10, 20))

        ctk.CTkButton(crud_button_frame, text="Agregar Ubicación", command=self.add_ubicacion_almacen).pack(side=tk.LEFT, padx=5)
        ctk.CTkButton(crud_button_frame, text="Modificar Ubicación", command=self.modify_ubicacion_almacen).pack(side=tk.LEFT, padx=5)
        ctk.CTkButton(crud_button_frame, text="Eliminar Ubicación", command=self.delete_ubicacion_almacen).pack(side=tk.LEFT, padx=5)

        # Treeview para mostrar ubicaciones
        columns = ("ID", "Nombre", "Capacidad Total", "Espacio Ocupado")
        self.tree_ubicaciones = ttk.Treeview(
            self.dynamic_content,
            columns=columns,
            show='headings',
            selectmode='browse'
        )
        for col in columns:
            self.tree_ubicaciones.heading(col, text=col)
            self.tree_ubicaciones.column(col, anchor=tk.CENTER, width=150)
        
        scroll_y = ttk.Scrollbar(self.dynamic_content, orient=tk.VERTICAL, command=self.tree_ubicaciones.yview)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_ubicaciones.configure(yscrollcommand=scroll_y.set)
        self.tree_ubicaciones.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

        self.load_ubicaciones_almacen()

    def load_ubicaciones_almacen(self):
        """Carga las ubicaciones de almacén en el Treeview"""
        for item in self.tree_ubicaciones.get_children():
            self.tree_ubicaciones.delete(item)
        
        ubicaciones = self.ubicacion_almacen_manejador.leer_todas_ubicaciones()
        for ub in ubicaciones:
            self.tree_ubicaciones.insert("", tk.END, values=(
                ub['id_Ubicacion_Almacen'],
                ub['nombre_almacen'],
                f"{ub['capacidad_total']:.2f}",
                f"{ub['espacio_ocupado']:.2f}"
            ))

    def add_ubicacion_almacen(self):
        """Abre la ventana para agregar una nueva ubicación de almacén"""
        self.add_window = ctk.CTkToplevel(self)
        self.add_window.title("Agregar Ubicación de Almacén")
        self.add_window.geometry("400x250")
        self.add_window.grab_set()

        ctk.CTkLabel(self.add_window, text="Nombre*:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.entry_nombre_ubicacion = ctk.CTkEntry(self.add_window, width=250)
        self.entry_nombre_ubicacion.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        ctk.CTkLabel(self.add_window, text="Capacidad Total*:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.entry_capacidad_ubicacion = ctk.CTkEntry(self.add_window, width=250)
        self.entry_capacidad_ubicacion.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        btn_frame = ctk.CTkFrame(self.add_window)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=20)
        ctk.CTkButton(btn_frame, text="Guardar", fg_color="green", command=self._save_ubicacion_almacen).pack(side=tk.LEFT, padx=10)
        ctk.CTkButton(btn_frame, text="Cancelar", fg_color="red", command=self.add_window.destroy).pack(side=tk.LEFT, padx=10)

    def _save_ubicacion_almacen(self):
        """Guarda una nueva ubicación de almacén en la base de datos"""
        nombre = self.entry_nombre_ubicacion.get().strip()
        capacidad_str = self.entry_capacidad_ubicacion.get().strip()

        if not nombre or not capacidad_str:
            messagebox.showerror("Error", "Nombre y Capacidad Total son obligatorios.")
            return
        
        try:
            capacidad = float(capacidad_str)
            if capacidad <= 0:
                messagebox.showerror("Error", "La capacidad total debe ser un número positivo.")
                return
        except ValueError:
            messagebox.showerror("Error", "La capacidad total debe ser un número válido.")
            return

        try:
            # El manejador de ubicaciones ya maneja espacio_ocupado por defecto en 0.0
            nuevo_id = self.ubicacion_almacen_manejador.crear_ubicacion_almacen(nombre, capacidad)
            if nuevo_id:
                messagebox.showinfo("Éxito", f"Ubicación '{nombre}' creada con ID: {nuevo_id}")
                self.add_window.destroy()
                self.load_ubicaciones_almacen()
            else:
                messagebox.showerror("Error", "No se pudo crear la ubicación. Verifique la consola para más detalles.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {str(e)}")

    def modify_ubicacion_almacen(self):
        """Abre la ventana para modificar una ubicación de almacén existente"""
        selected = self.tree_ubicaciones.focus()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione una ubicación para modificar.")
            return
        
        item_data = self.tree_ubicaciones.item(selected)['values']
        id_ubicacion = item_data[0]
        current_nombre = item_data[1]
        current_capacidad = item_data[2]
        current_ocupado = item_data[3]

        self.modify_window = ctk.CTkToplevel(self)
        self.modify_window.title("Modificar Ubicación de Almacén")
        self.modify_window.geometry("400x300")
        self.modify_window.grab_set()

        ctk.CTkLabel(self.modify_window, text="ID:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        ctk.CTkLabel(self.modify_window, text=str(id_ubicacion)).grid(row=0, column=1, padx=10, pady=5, sticky="w")

        ctk.CTkLabel(self.modify_window, text="Nombre*:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.entry_mod_nombre_ubicacion = ctk.CTkEntry(self.modify_window, width=250)
        self.entry_mod_nombre_ubicacion.insert(0, current_nombre)
        self.entry_mod_nombre_ubicacion.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        ctk.CTkLabel(self.modify_window, text="Capacidad Total*:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.entry_mod_capacidad_ubicacion = ctk.CTkEntry(self.modify_window, width=250)
        self.entry_mod_capacidad_ubicacion.insert(0, current_capacidad)
        self.entry_mod_capacidad_ubicacion.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        ctk.CTkLabel(self.modify_window, text="Espacio Ocupado*:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.entry_mod_espacio_ocupado = ctk.CTkEntry(self.modify_window, width=250)
        self.entry_mod_espacio_ocupado.insert(0, current_ocupado)
        self.entry_mod_espacio_ocupado.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
        
        btn_frame = ctk.CTkFrame(self.modify_window)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=20)
        ctk.CTkButton(btn_frame, text="Guardar Cambios", fg_color="green", command=lambda: self._update_ubicacion_almacen(id_ubicacion)).pack(side=tk.LEFT, padx=10)
        ctk.CTkButton(btn_frame, text="Cancelar", fg_color="red", command=self.modify_window.destroy).pack(side=tk.LEFT, padx=10)

    def _update_ubicacion_almacen(self, id_ubicacion):
        """Actualiza una ubicación de almacén existente en la base de datos"""
        nombre = self.entry_mod_nombre_ubicacion.get().strip()
        capacidad_str = self.entry_mod_capacidad_ubicacion.get().strip()
        ocupado_str = self.entry_mod_espacio_ocupado.get().strip()

        if not nombre or not capacidad_str or not ocupado_str:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return
        
        try:
            capacidad = float(capacidad_str)
            ocupado = float(ocupado_str)
            if capacidad <= 0:
                messagebox.showerror("Error", "La capacidad total debe ser un número positivo.")
                return
            if ocupado < 0:
                messagebox.showerror("Error", "El espacio ocupado no puede ser negativo.")
                return
            if ocupado > capacidad:
                messagebox.showerror("Error", "El espacio ocupado no puede exceder la capacidad total.")
                return
        except ValueError:
            messagebox.showerror("Error", "Capacidad y Espacio Ocupado deben ser números válidos.")
            return

        try:
            success = self.ubicacion_almacen_manejador.actualizar_ubicacion_almacen(
                id_ubicacion,
                nuevo_nombre=nombre,
                nueva_capacidad_total=capacidad,
                nuevo_espacio_ocupado=ocupado
            )
            if success:
                messagebox.showinfo("Éxito", "Ubicación actualizada exitosamente.")
                self.modify_window.destroy()
                self.load_ubicaciones_almacen()
            else:
                messagebox.showerror("Error", "No se pudo actualizar la ubicación. Verifique la consola para más detalles.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {str(e)}")

    def delete_ubicacion_almacen(self):
        """Elimina una ubicación de almacén existente"""
        selected = self.tree_ubicaciones.focus()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione una ubicación para eliminar.")
            return
        
        item_data = self.tree_ubicaciones.item(selected)['values']
        id_ubicacion = item_data[0]
        nombre_ubicacion = item_data[1]

        if not messagebox.askyesno("Confirmar Eliminación", f"¿Está seguro de eliminar la ubicación '{nombre_ubicacion}' (ID: {id_ubicacion})?\nEsto podría afectar registros de inventario asociados."):
            return
        
        try:
            success = self.ubicacion_almacen_manejador.eliminar_ubicacion_almacen(id_ubicacion)
            if success:
                messagebox.showinfo("Éxito", "Ubicación eliminada exitosamente.")
                self.load_ubicaciones_almacen()
            else:
                messagebox.showerror("Error", "No se pudo eliminar la ubicación. Verifique si hay inventario asociado o si está siendo referenciada en movimientos.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {str(e)}")

    # --- GESTIÓN DE INVENTARIO POR UBICACIÓN ---
    def show_inventario_por_ubicacion(self):
        """Muestra la interfaz para gestionar el inventario por ubicación"""
        if hasattr(self, 'warehouse_message'):
            self.warehouse_message.pack_forget()
        
        self.clear_content()
        self.show_warehouse() # Recrea el título y los botones de sub-módulo

        if hasattr(self, 'warehouse_message'):
            self.warehouse_message.pack_forget()

        tk.Label(
            self.dynamic_content,
            text="Gestión de Inventario por Ubicación",
            bg="#FDFBF6",
            fg="#1F2937",
            font=("Arial", 14, "bold")
        ).pack(pady=(10, 0))

        # Botones CRUD para Inventario por Ubicación
        crud_button_frame = ctk.CTkFrame(self.dynamic_content)
        crud_button_frame.pack(pady=(10, 20))

        ctk.CTkButton(crud_button_frame, text="Agregar Registro", command=self.add_inventario_registro).pack(side=tk.LEFT, padx=5)
        ctk.CTkButton(crud_button_frame, text="Modificar Registro", command=self.modify_inventario_registro).pack(side=tk.LEFT, padx=5)
        ctk.CTkButton(crud_button_frame, text="Eliminar Registro", command=self.delete_inventario_registro).pack(side=tk.LEFT, padx=5)

        # Treeview para mostrar inventario
        columns = ("ID Reg.", "Producto", "Unidad", "Ubicación", "Stock Actual", "Última Actualización", "Centro Costos")
        self.tree_inventario = ttk.Treeview(
            self.dynamic_content,
            columns=columns,
            show='headings',
            selectmode='browse'
        )
        for col in columns:
            self.tree_inventario.heading(col, text=col)
            self.tree_inventario.column(col, anchor=tk.CENTER, width=120)
        
        self.tree_inventario.column("Producto", width=180)
        self.tree_inventario.column("Ubicación", width=150)
        self.tree_inventario.column("Última Actualización", width=150)

        scroll_y = ttk.Scrollbar(self.dynamic_content, orient=tk.VERTICAL, command=self.tree_inventario.yview)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_inventario.configure(yscrollcommand=scroll_y.set)
        self.tree_inventario.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

        self.load_inventario_por_ubicacion()

    def load_inventario_por_ubicacion(self):
        """Carga los registros de inventario por ubicación en el Treeview"""
        for item in self.tree_inventario.get_children():
            self.tree_inventario.delete(item)
        
        inventario = self.inventario_ubicacion_manejador.leer_todo_inventario()
        for inv in inventario:
            self.tree_inventario.insert("", tk.END, values=(
                inv['id'],
                inv['nombre_producto'],
                inv['unidad_medida_abreviatura'],
                inv['nombre_ubicacion'],
                f"{inv['stock_actual']:.2f}",
                inv['ultima_actualizacion'],
                inv['centro_costos']
            ))

    def add_inventario_registro(self):
        """Abre la ventana para agregar un nuevo registro de inventario por ubicación"""
        self.add_window = ctk.CTkToplevel(self)
        self.add_window.title("Agregar Registro de Inventario")
        self.add_window.geometry("500x400")
        self.add_window.grab_set()

        self.inv_prod_var = tk.StringVar()
        self.inv_ubicacion_var = tk.StringVar()
        self.inv_centro_costo_var = tk.StringVar()
        self.inv_stock_inicial_entry = ctk.CTkEntry(self.add_window)

        self.selected_inv_product_id = None
        self.selected_inv_ubicacion_id = None
        self.selected_inv_centro_costo_id = None

        row_idx = 0
        ctk.CTkLabel(self.add_window, text="Producto*:").grid(row=row_idx, column=0, padx=10, pady=5, sticky="e")
        ctk.CTkButton(self.add_window, text="Seleccionar Producto", command=self._select_product_for_inv_add).grid(row=row_idx, column=1, padx=10, pady=5, sticky="w")
        ctk.CTkLabel(self.add_window, textvariable=self.inv_prod_var).grid(row=row_idx, column=2, padx=10, pady=5, sticky="w")

        row_idx += 1
        ctk.CTkLabel(self.add_window, text="Ubicación*:").grid(row=row_idx, column=0, padx=10, pady=5, sticky="e")
        ctk.CTkButton(self.add_window, text="Seleccionar Ubicación", command=self._select_ubicacion_for_inv_add).grid(row=row_idx, column=1, padx=10, pady=5, sticky="w")
        ctk.CTkLabel(self.add_window, textvariable=self.inv_ubicacion_var).grid(row=row_idx, column=2, padx=10, pady=5, sticky="w")

        row_idx += 1
        ctk.CTkLabel(self.add_window, text="Centro de Costos*:").grid(row=row_idx, column=0, padx=10, pady=5, sticky="e")
        ctk.CTkButton(self.add_window, text="Seleccionar Centro", command=self._select_centro_costo_for_inv_add).grid(row=row_idx, column=1, padx=10, pady=5, sticky="w")
        ctk.CTkLabel(self.add_window, textvariable=self.inv_centro_costo_var).grid(row=row_idx, column=2, padx=10, pady=5, sticky="w")

        row_idx += 1
        ctk.CTkLabel(self.add_window, text="Stock Inicial*:").grid(row=row_idx, column=0, padx=10, pady=5, sticky="e")
        self.inv_stock_inicial_entry.grid(row=row_idx, column=1, columnspan=2, padx=10, pady=5, sticky="ew")

        btn_frame = ctk.CTkFrame(self.add_window)
        btn_frame.grid(row=row_idx + 1, column=0, columnspan=3, pady=20)
        ctk.CTkButton(btn_frame, text="Guardar", fg_color="green", command=self._save_inventario_registro).pack(side=tk.LEFT, padx=10)
        ctk.CTkButton(btn_frame, text="Cancelar", fg_color="red", command=self.add_window.destroy).pack(side=tk.LEFT, padx=10)

    def _select_product_for_inv_add(self):
        """Abre una ventana para seleccionar un producto para el registro de inventario"""
        select_window = ctk.CTkToplevel(self)
        select_window.title("Seleccionar Producto")
        select_window.geometry("600x400")
        select_window.grab_set()

        columns = ("ID", "Nombre", "Unidad")
        tree = ttk.Treeview(select_window, columns=columns, show='headings', selectmode='browse')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor=tk.CENTER, width=150)
        tree.pack(fill=tk.BOTH, expand=True)

        productos = self.productos_manejador.leer_todos_productos()
        for p in productos:
            tree.insert("", tk.END, values=(p['id_productos'], p['nombre_producto'], p['unidad_abreviatura']))

        def on_select():
            selected_item = tree.focus()
            if selected_item:
                item_data = tree.item(selected_item)['values']
                self.selected_inv_product_id = item_data[0]
                self.inv_prod_var.set(item_data[1])
                select_window.destroy()
            else:
                messagebox.showwarning("Advertencia", "Seleccione un producto.")

        ctk.CTkButton(select_window, text="Seleccionar", command=on_select).pack(pady=10)

    def _select_ubicacion_for_inv_add(self):
        """Abre una ventana para seleccionar una ubicación para el registro de inventario"""
        select_window = ctk.CTkToplevel(self)
        select_window.title("Seleccionar Ubicación")
        select_window.geometry("400x300")
        select_window.grab_set()

        columns = ("ID", "Nombre", "Capacidad", "Ocupado")
        tree = ttk.Treeview(select_window, columns=columns, show='headings', selectmode='browse')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor=tk.CENTER, width=100)
        tree.pack(fill=tk.BOTH, expand=True)

        ubicaciones = self.ubicacion_almacen_manejador.leer_todas_ubicaciones()
        for ub in ubicaciones:
            tree.insert("", tk.END, values=(ub['id_ubicacion'], ub['nombre_ubicacion'], f"{ub['capacidad_total']:.2f}", f"{ub['espacio_ocupado']:.2f}"))

        def on_select():
            selected_item = tree.focus()
            if selected_item:
                item_data = tree.item(selected_item)['values']
                self.selected_inv_ubicacion_id = item_data[0]
                self.inv_ubicacion_var.set(item_data[1])
                select_window.destroy()
            else:
                messagebox.showwarning("Advertencia", "Seleccione una ubicación.")

        ctk.CTkButton(select_window, text="Seleccionar", command=on_select).pack(pady=10)

    def _select_centro_costo_for_inv_add(self):
        """Abre una ventana para seleccionar un centro de costos para el registro de inventario"""
        select_window = ctk.CTkToplevel(self)
        select_window.title("Seleccionar Centro de Costos")
        select_window.geometry("400x300")
        select_window.grab_set()

        columns = ("ID", "Nombre")
        tree = ttk.Treeview(select_window, columns=columns, show='headings', selectmode='browse')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor=tk.CENTER, width=150)
        tree.pack(fill=tk.BOTH, expand=True)

        centros = self.centros_costos_manejador.leer_todos_centros_costo()
        for cc in centros:
            tree.insert("", tk.END, values=(cc['id_centro_costos'], cc['nombre_centro']))

        def on_select():
            selected_item = tree.focus()
            if selected_item:
                item_data = tree.item(selected_item)['values']
                self.selected_inv_centro_costo_id = item_data[0]
                self.inv_centro_costo_var.set(item_data[1])
                select_window.destroy()
            else:
                messagebox.showwarning("Advertencia", "Seleccione un centro de costos.")

        ctk.CTkButton(select_window, text="Seleccionar", command=on_select).pack(pady=10)

    def _save_inventario_registro(self):
        """Guarda un nuevo registro de inventario por ubicación en la base de datos"""
        id_producto = self.selected_inv_product_id
        id_ubicacion = self.selected_inv_ubicacion_id
        id_centro_costos = self.selected_inv_centro_costo_id
        stock_inicial_str = self.inv_stock_inicial_entry.get().strip()

        if not id_producto or not id_ubicacion or not id_centro_costos or not stock_inicial_str:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return
        
        try:
            stock_inicial = float(stock_inicial_str)
            if stock_inicial < 0:
                messagebox.showerror("Error", "El stock inicial no puede ser negativo.")
                return
        except ValueError:
            messagebox.showerror("Error", "El stock inicial debe ser un número válido.")
            return

        # Validar si ya existe un registro para este producto en esta ubicación
        existing_record = self.inventario_ubicacion_manejador.leer_stock_por_ubicacion_y_producto(id_producto, id_ubicacion)
        if existing_record:
            messagebox.showerror("Error", "Ya existe un registro de inventario para este producto en esta ubicación. Use la opción 'Modificar' o 'Movimientos' para actualizar el stock.")
            return

        # Validar capacidad de la ubicación antes de crear el registro
        ubicacion_data = self.ubicacion_almacen_manejador.leer_ubicacion_por_id(id_ubicacion)
        if not ubicacion_data:
            messagebox.showerror("Error", "La ubicación seleccionada no existe.")
            return
        
        new_espacio_ocupado = ubicacion_data['espacio_ocupado'] + stock_inicial
        if new_espacio_ocupado > ubicacion_data['capacidad_total']:
            messagebox.showerror("Error", f"El stock inicial ({stock_inicial:.2f}) excede la capacidad disponible en la ubicación '{ubicacion_data['nombre_ubicacion']}' (Disponible: {ubicacion_data['capacidad_total'] - ubicacion_data['espacio_ocupado']:.2f}).")
            return

        try:
            nuevo_id = self.inventario_ubicacion_manejador.crear_registro_inventario(
                id_producto, id_ubicacion, stock_inicial, id_centro_costos
            )
            
            if nuevo_id:
                # La actualización del espacio ocupado en la ubicación se maneja dentro del manejador de inventario
                messagebox.showinfo("Éxito", f"Registro de inventario creado con ID: {nuevo_id}")
                self.add_window.destroy()
                self.load_inventario_por_ubicacion()
                self.load_ubicaciones_almacen() # Refrescar la tabla de ubicaciones también
            else:
                messagebox.showerror("Error", "No se pudo crear el registro de inventario. Verifique la consola para más detalles.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {str(e)}")

    def modify_inventario_registro(self):
        """Abre la ventana para modificar un registro de inventario por ubicación"""
        selected = self.tree_inventario.focus()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un registro de inventario para modificar.")
            return
        
        item_data = self.tree_inventario.item(selected)['values']
        id_registro = item_data[0]

        record_data = self.inventario_ubicacion_manejador.leer_inventario_por_id(id_registro)
        if not record_data:
            messagebox.showerror("Error", "No se pudo cargar el registro de inventario.")
            return

        self.modify_window = ctk.CTkToplevel(self)
        self.modify_window.title("Modificar Registro de Inventario")
        self.modify_window.geometry("500x350")
        self.modify_window.grab_set()

        self.mod_inv_centro_costo_var = tk.StringVar(value=record_data['centro_costos'])
        self.selected_mod_inv_centro_costo_id = record_data['id_centro_costos']

        row_idx = 0
        ctk.CTkLabel(self.modify_window, text="ID Registro:").grid(row=row_idx, column=0, padx=10, pady=5, sticky="e")
        ctk.CTkLabel(self.modify_window, text=str(record_data['id'])).grid(row=row_idx, column=1, padx=10, pady=5, sticky="w")

        row_idx += 1
        ctk.CTkLabel(self.modify_window, text="Producto:").grid(row=row_idx, column=0, padx=10, pady=5, sticky="e")
        ctk.CTkLabel(self.modify_window, text=record_data['nombre_producto']).grid(row=row_idx, column=1, padx=10, pady=5, sticky="w")

        row_idx += 1
        ctk.CTkLabel(self.modify_window, text="Ubicación:").grid(row=row_idx, column=0, padx=10, pady=5, sticky="e")
        ctk.CTkLabel(self.modify_window, text=record_data['nombre_ubicacion']).grid(row=row_idx, column=1, padx=10, pady=5, sticky="w")

        row_idx += 1
        ctk.CTkLabel(self.modify_window, text="Stock Actual*:").grid(row=row_idx, column=0, padx=10, pady=5, sticky="e")
        self.entry_mod_stock_actual = ctk.CTkEntry(self.modify_window, width=250)
        self.entry_mod_stock_actual.insert(0, str(record_data['stock_actual']))
        self.entry_mod_stock_actual.grid(row=row_idx, column=1, padx=10, pady=5, sticky="ew")

        row_idx += 1
        ctk.CTkLabel(self.modify_window, text="Centro de Costos*:").grid(row=row_idx, column=0, padx=10, pady=5, sticky="e")
        ctk.CTkButton(self.modify_window, text="Seleccionar Centro", command=self._select_centro_costo_for_inv_modify).grid(row=row_idx, column=1, padx=10, pady=5, sticky="w")
        ctk.CTkLabel(self.modify_window, textvariable=self.mod_inv_centro_costo_var).grid(row=row_idx, column=2, padx=10, pady=5, sticky="w")

        btn_frame = ctk.CTkFrame(self.modify_window)
        btn_frame.grid(row=row_idx + 1, column=0, columnspan=3, pady=20)
        ctk.CTkButton(btn_frame, text="Guardar Cambios", fg_color="green", command=lambda: self._update_inventario_registro(id_registro)).pack(side=tk.LEFT, padx=10)
        ctk.CTkButton(btn_frame, text="Cancelar", fg_color="red", command=self.modify_window.destroy).pack(side=tk.LEFT, padx=10)

    def _select_centro_costo_for_inv_modify(self):
        """Abre una ventana para seleccionar un nuevo centro de costos para el registro de inventario"""
        select_window = ctk.CTkToplevel(self)
        select_window.title("Seleccionar Nuevo Centro de Costos")
        select_window.geometry("400x300")
        select_window.grab_set()

        columns = ("ID", "Nombre")
        tree = ttk.Treeview(select_window, columns=columns, show='headings', selectmode='browse')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor=tk.CENTER, width=150)
        tree.pack(fill=tk.BOTH, expand=True)

        centros = self.centros_costos_manejador.leer_todos_centros_costo()
        for cc in centros:
            tree.insert("", tk.END, values=(cc['id_centro_costos'], cc['nombre_centro']))

        def on_select():
            selected_item = tree.focus()
            if selected_item:
                item_data = tree.item(selected_item)['values']
                self.selected_mod_inv_centro_costo_id = item_data[0]
                self.mod_inv_centro_costo_var.set(item_data[1])
                select_window.destroy()
            else:
                messagebox.showwarning("Advertencia", "Seleccione un centro de costos.")

        ctk.CTkButton(select_window, text="Seleccionar", command=on_select).pack(pady=10)

    def _update_inventario_registro(self, id_registro):
        """Actualiza un registro de inventario por ubicación en la base de datos"""
        stock_actual_str = self.entry_mod_stock_actual.get().strip()
        id_centro_costos = self.selected_mod_inv_centro_costo_id

        if not stock_actual_str or id_centro_costos is None:
            messagebox.showerror("Error", "Stock Actual y Centro de Costos son obligatorios.")
            return
        
        try:
            stock_actual = float(stock_actual_str)
            if stock_actual < 0:
                messagebox.showerror("Error", "El stock actual no puede ser negativo.")
                return
        except ValueError:
            messagebox.showerror("Error", "El stock actual debe ser un número válido.")
            return

        try:
            success = self.inventario_ubicacion_manejador.actualizar_registro_inventario_completo(
                id_registro,
                nuevo_stock_actual=stock_actual,
                nuevo_id_centro_costos=id_centro_costos
            )
            if success:
                messagebox.showinfo("Éxito", "Registro de inventario actualizado exitosamente.")
                self.modify_window.destroy()
                self.load_inventario_por_ubicacion()
                self.load_ubicaciones_almacen() # Refrescar la tabla de ubicaciones también
            else:
                messagebox.showerror("Error", "No se pudo actualizar el registro de inventario. Verifique la consola para más detalles.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {str(e)}")

    def delete_inventario_registro(self):
        """Elimina un registro de inventario por ubicación"""
        selected = self.tree_inventario.focus()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un registro de inventario para eliminar.")
            return
        
        item_data = self.tree_inventario.item(selected)['values']
        id_registro = item_data[0]
        producto_nombre = item_data[1]
        ubicacion_nombre = item_data[3]

        if not messagebox.askyesno("Confirmar Eliminación", f"¿Está seguro de eliminar el registro de inventario para '{producto_nombre}' en '{ubicacion_nombre}' (ID Reg: {id_registro})?\nEsto eliminará el stock de este producto en esta ubicación y ajustará el espacio ocupado."):
            return
        
        try:
            success = self.inventario_ubicacion_manejador.eliminar_registro_inventario(id_registro)
            if success:
                messagebox.showinfo("Éxito", "Registro de inventario eliminado exitosamente.")
                self.load_inventario_por_ubicacion()
                self.load_ubicaciones_almacen() # Refrescar la tabla de ubicaciones también
            else:
                messagebox.showerror("Error", "No se pudo eliminar el registro de inventario. Verifique la consola para más detalles.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {str(e)}")

    # --- SECCIÓN DE REPORTES (Placeholder) ---
    def show_reports(self):
        """Muestra la sección de reportes (placeholder)"""
        self.clear_content()
        tk.Label(
            self.dynamic_content,
            text="Sección de Reportes (En desarrollo)",
            bg="#FDFBF6",
            fg="#1F2937",
            font=("Arial", 16, "bold")
        ).pack(pady=50)

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
