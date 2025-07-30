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
        
        # Inicializar base de datos
        self.conn = db.get_connection()
        if not self.conn:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            return
        
        # Inicializar manejadores
        self.centro_costos_manejador = Manejador_centros_costos(self.conn)
        self.productos_manejador = Manejador_productos(self.conn)
        self.unidad_medida_manejador = Manejador_unidad_medida(self.conn)
        self.proveedor_manejador = Manejador_proveedor(self.conn)
        self.categorias_manejador = Manejador_categorias(self.conn)
        self.movimientos_manejador = Manejador_movimientos(self.conn)
        self.ubicacion_almacen_manejador = Manejador_ubicacion_almacen(self.conn)
        self.inventario_manejador = Manejador_inventario_por_ubicacion(self.conn)
        
        # Variables para selección
        self.selected_centro_costo_id = None
        self.selected_producto_id = None
        self.selected_unidad_medida_id = None
        self.selected_proveedor_id = None
        self.selected_categoria_id = None
        self.selected_movimiento_id = None
        self.selected_ubicacion_id = None
        self.selected_inv_ubicacion_id = None
        
        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        # Frame principal
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título
        title_label = ctk.CTkLabel(main_frame, text="Sistema de Gestión de Inventario", 
                                  font=ctk.CTkFont(size=24, weight="bold"))
        title_label.pack(pady=20)
        
        # Notebook para las pestañas
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Crear pestañas
        self.create_catalogos_tab()
        self.create_productos_tab()
        self.create_movimientos_tab()
        self.create_inventario_tab()
    
    def create_catalogos_tab(self):
        """Crea la pestaña de catálogos"""
        catalogos_frame = ctk.CTkFrame(self.notebook)
        self.notebook.add(catalogos_frame, text="Catálogos")
        
        # Notebook interno para sub-pestañas
        catalogos_notebook = ttk.Notebook(catalogos_frame)
        catalogos_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Pestaña Centros de Costos
        self.create_centro_costos_tab(catalogos_notebook)
        
        # Pestaña Unidades de Medida
        self.create_unidad_medida_tab(catalogos_notebook)
        
        # Pestaña Proveedores
        self.create_proveedores_tab(catalogos_notebook)
        
        # Pestaña Categorías
        self.create_categorias_tab(catalogos_notebook)
    
    def create_centro_costos_tab(self, parent):
        """Crea la pestaña de centros de costos"""
        frame = ctk.CTkFrame(parent)
        parent.add(frame, text="Centros de Costos")
        
        # Frame para botones
        button_frame = ctk.CTkFrame(frame)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Botones
        ctk.CTkButton(button_frame, text="Agregar", command=self.add_centro_costo).pack(side=tk.LEFT, padx=5)
        ctk.CTkButton(button_frame, text="Editar", command=self.edit_centro_costo).pack(side=tk.LEFT, padx=5)
        ctk.CTkButton(button_frame, text="Eliminar", command=self.delete_centro_costo).pack(side=tk.LEFT, padx=5)
        
        # Treeview
        columns = ("ID", "Nombre", "Descripción")
        self.tree_centro_costos = ttk.Treeview(frame, columns=columns, show='headings', selectmode='browse')
        
        for col in columns:
            self.tree_centro_costos.heading(col, text=col)
            self.tree_centro_costos.column(col, anchor=tk.CENTER, width=150)
        
        self.tree_centro_costos.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree_centro_costos.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_centro_costos.configure(yscrollcommand=scrollbar.set)
        
        # Binding para selección
        self.tree_centro_costos.bind('<<TreeviewSelect>>', lambda e: self.on_centro_costo_select())
    
    def create_unidad_medida_tab(self, parent):
        """Crea la pestaña de unidades de medida"""
        frame = ctk.CTkFrame(parent)
        parent.add(frame, text="Unidades de Medida")
        
        # Frame para botones
        button_frame = ctk.CTkFrame(frame)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Botones
        ctk.CTkButton(button_frame, text="Agregar", command=self.add_unidad_medida).pack(side=tk.LEFT, padx=5)
        ctk.CTkButton(button_frame, text="Editar", command=self.edit_unidad_medida).pack(side=tk.LEFT, padx=5)
        ctk.CTkButton(button_frame, text="Eliminar", command=self.delete_unidad_medida).pack(side=tk.LEFT, padx=5)
        
        # Treeview
        columns = ("ID", "Nombre", "Descripción")
        self.tree_unidad_medida = ttk.Treeview(frame, columns=columns, show='headings', selectmode='browse')
        
        for col in columns:
            self.tree_unidad_medida.heading(col, text=col)
            self.tree_unidad_medida.column(col, anchor=tk.CENTER, width=150)
        
        self.tree_unidad_medida.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree_unidad_medida.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_unidad_medida.configure(yscrollcommand=scrollbar.set)
        
        # Binding para selección
        self.tree_unidad_medida.bind('<<TreeviewSelect>>', lambda e: self.on_unidad_medida_select())
    
    def create_proveedores_tab(self, parent):
        """Crea la pestaña de proveedores"""
        frame = ctk.CTkFrame(parent)
        parent.add(frame, text="Proveedores")
        
        # Frame para botones
        button_frame = ctk.CTkFrame(frame)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Botones
        ctk.CTkButton(button_frame, text="Agregar", command=self.add_proveedor).pack(side=tk.LEFT, padx=5)
        ctk.CTkButton(button_frame, text="Editar", command=self.edit_proveedor).pack(side=tk.LEFT, padx=5)
        ctk.CTkButton(button_frame, text="Eliminar", command=self.delete_proveedor).pack(side=tk.LEFT, padx=5)
        
        # Treeview
        columns = ("ID", "Nombre", "Teléfono", "Email", "Dirección")
        self.tree_proveedores = ttk.Treeview(frame, columns=columns, show='headings', selectmode='browse')
        
        for col in columns:
            self.tree_proveedores.heading(col, text=col)
            self.tree_proveedores.column(col, anchor=tk.CENTER, width=120)
        
        self.tree_proveedores.column("Nombre", width=150)
        self.tree_proveedores.column("Email", width=150)
        self.tree_proveedores.column("Dirección", width=200)
        
        self.tree_proveedores.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree_proveedores.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_proveedores.configure(yscrollcommand=scrollbar.set)
        
        # Binding para selección
        self.tree_proveedores.bind('<<TreeviewSelect>>', lambda e: self.on_proveedor_select())
    
    def create_categorias_tab(self, parent):
        """Crea la pestaña de categorías"""
        frame = ctk.CTkFrame(parent)
        parent.add(frame, text="Categorías")
        
        # Frame para botones
        button_frame = ctk.CTkFrame(frame)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Botones
        ctk.CTkButton(button_frame, text="Agregar", command=self.add_categoria).pack(side=tk.LEFT, padx=5)
        ctk.CTkButton(button_frame, text="Editar", command=self.edit_categoria).pack(side=tk.LEFT, padx=5)
        ctk.CTkButton(button_frame, text="Eliminar", command=self.delete_categoria).pack(side=tk.LEFT, padx=5)
        
        # Treeview
        columns = ("ID", "Nombre", "Descripción")
        self.tree_categorias = ttk.Treeview(frame, columns=columns, show='headings', selectmode='browse')
        
        for col in columns:
            self.tree_categorias.heading(col, text=col)
            self.tree_categorias.column(col, anchor=tk.CENTER, width=150)
        
        self.tree_categorias.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree_categorias.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_categorias.configure(yscrollcommand=scrollbar.set)
        
        # Binding para selección
        self.tree_categorias.bind('<<TreeviewSelect>>', lambda e: self.on_categoria_select())