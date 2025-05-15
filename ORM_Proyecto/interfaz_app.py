import customtkinter as ctk
from tkinter import ttk, messagebox
from logica_app import LogicaApp
import os


class InterfazApp:
    def __init__(self, app):
        self.app = app
        self.imagenes = {}  # Diccionario para mapear nombres a imágenes

    def crear_formulario_ingrediente(self, parent):
        """Crea el formulario para gestionar ingredientes."""
        # Frame superior
        frame_superior = ctk.CTkFrame(parent)
        frame_superior.pack(pady=10, padx=10, fill="x")

        # Campos de entrada
        ctk.CTkLabel(frame_superior, text="Nombre").grid(row=0, column=0, pady=10, padx=10)
        self.combo_box_nombre = ctk.CTkComboBox(frame_superior, values=["Pan", "Hamburguesa", "Lechuga", "Tomate", "Papas", "Bebida", "Vienesa"])
        self.combo_box_nombre.grid(row=0, column=1, pady=10, padx=10)

        ctk.CTkLabel(frame_superior, text="Tipo").grid(row=0, column=2, pady=10, padx=10)
        self.entry_tipo = ctk.CTkEntry(frame_superior)
        self.entry_tipo.grid(row=0, column=3, pady=10, padx=10)

        ctk.CTkLabel(frame_superior, text="Cantidad").grid(row=0, column=4, pady=10, padx=10)
        self.entry_cantidad = ctk.CTkEntry(frame_superior)
        self.entry_cantidad.grid(row=0, column=5, pady=10, padx=10)

        ctk.CTkLabel(frame_superior, text="Unidad").grid(row=0, column=6, pady=10, padx=10)
        self.entry_unidad = ctk.CTkEntry(frame_superior)
        self.entry_unidad.grid(row=0, column=7, pady=10, padx=10)

        # Botones
        ctk.CTkButton(frame_superior, text="Añadir Ingrediente", command=self.crear_ingrediente).grid(row=1, column=1, pady=10, padx=10)
        ctk.CTkButton(frame_superior, text="Actualizar Ingrediente", command=self.actualizar_ingrediente).grid(row=1, column=3, pady=10, padx=10)
        ctk.CTkButton(frame_superior, text="Eliminar Ingrediente", command=self.eliminar_ingrediente).grid(row=1, column=5, pady=10, padx=10)

        # Frame inferior
        frame_inferior = ctk.CTkFrame(parent)
        frame_inferior.pack(pady=10, padx=10, fill="both", expand=True)

        # Treeview
        self.treeview_ingredientes = ttk.Treeview(frame_inferior, columns=("Nombre", "Tipo", "Cantidad", "Unidad"), show="headings")
        self.treeview_ingredientes.heading("Nombre", text="Nombre")
        self.treeview_ingredientes.heading("Tipo", text="Tipo")
        self.treeview_ingredientes.heading("Cantidad", text="Cantidad")
        self.treeview_ingredientes.heading("Unidad", text="Unidad")
        self.treeview_ingredientes.pack(pady=10, padx=10, fill="both", expand=True)

        # Cargar los ingredientes al Treeview
        self.cargar_ingredientes_treeview()

    def cargar_ingredientes_treeview(self):
        """Carga los ingredientes en el Treeview."""
        ingredientes = LogicaApp.cargar_ingredientes()
        self.treeview_ingredientes.delete(*self.treeview_ingredientes.get_children())
        for ingrediente in ingredientes:
            self.treeview_ingredientes.insert("", "end", values=(ingrediente.nombre, ingrediente.tipo, ingrediente.cantidad, ingrediente.unidad))

    def crear_ingrediente(self):
        """Llama a la lógica para crear un ingrediente."""
        nombre = self.combo_box_nombre.get()
        tipo = self.entry_tipo.get()
        try:
            cantidad = int(self.entry_cantidad.get())
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número entero.")
            return
        unidad = self.entry_unidad.get()
        LogicaApp.crear_ingrediente(nombre, tipo, cantidad, unidad)
        self.cargar_ingredientes_treeview()

    def actualizar_ingrediente(self):
        """Llama a la lógica para actualizar un ingrediente."""
        nombre = self.combo_box_nombre.get()
        tipo = self.entry_tipo.get()
        cantidad = self.entry_cantidad.get()
        unidad = self.entry_unidad.get()
        LogicaApp.actualizar_ingrediente(nombre, tipo, cantidad, unidad)
        self.cargar_ingredientes_treeview()

    def eliminar_ingrediente(self):
        """Llama a la lógica para eliminar un ingrediente."""
        selected_item = self.treeview_ingredientes.selection()
        if selected_item:
            nombre = self.treeview_ingredientes.item(selected_item, "values")[0]
            LogicaApp.eliminar_ingrediente(nombre)
            self.cargar_ingredientes_treeview()
            

    def crear_formulario_menu(self, parent):
        """Crea el formulario para crear un menú y seleccionar ingredientes."""
        # Frame superior
        frame_superior = ctk.CTkFrame(parent)
        frame_superior.pack(pady=10, padx=10, fill="x")
        self.ingredientes_menu = []  # Lista temporal para ingredientes del menú


        # Fila para el nombre y descripción del menú
        ctk.CTkLabel(frame_superior, text="Nombre del Menú").grid(row=0, column=0, pady=10, padx=10)
        self.combo_box_menu_nombre = ctk.CTkComboBox(frame_superior)
        self.combo_box_menu_nombre.grid(row=0, column=1, pady=10, padx=10)

        # Cargar imágenes y nombres en el ComboBox
        self.cargar_imagenes_en_combobox_menu()

        ctk.CTkLabel(frame_superior, text="Descripción del Menú").grid(row=0, column=2, pady=10, padx=10)
        self.entry_menu_descripcion = ctk.CTkEntry(frame_superior)
        self.entry_menu_descripcion.grid(row=0, column=3, pady=10, padx=10)

        ctk.CTkLabel(frame_superior, text="Precio").grid(row=0, column=4, pady=10, padx=10)
        self.entry_precio = ctk.CTkEntry(frame_superior)
        self.entry_precio.grid(row=0, column=5, pady=10, padx=10)

        # Botón para crear el menú
        self.btn_crear_menu = ctk.CTkButton(frame_superior, text="Crear Menú", command=self.crear_menu)
        self.btn_crear_menu.grid(row=0, column=6, columnspan=3, pady=10, padx=10)


        # Fila para seleccionar ingredientes
        ctk.CTkLabel(frame_superior, text="Seleccionar Ingredientes").grid(row=1, column=0, pady=10, padx=10)
        self.combobox_ingredientes = ttk.Combobox(frame_superior, state="readonly")
        self.combobox_ingredientes.grid(row=1, column=1, pady=10, padx=10)

        ctk.CTkLabel(frame_superior, text="Cantidad").grid(row=1, column=2, pady=10, padx=10)
        self.entry_cantidad2 = ctk.CTkEntry(frame_superior)
        self.entry_cantidad2.grid(row=1, column=3, pady=10, padx=10)

        # Botón para agregar ingredientes seleccionados al menú
        self.btn_agregar_ingrediente = ctk.CTkButton(frame_superior, text="Agregar Ingrediente", command=self.agregar_ingrediente)
        self.btn_agregar_ingrediente.grid(row=1, column=4, pady=10, padx=10)

        self.btn_eliminar_ingrediente = ctk.CTkButton(frame_superior, text="Eliminar Ingrediente", command=self.quitar_ingrediente)
        self.btn_eliminar_ingrediente.grid(row=1, column=5, pady=10, padx=10)

        # Frame inferior
        frame_inferior = ctk.CTkFrame(parent)
        frame_inferior.pack(pady=10, padx=10, fill="both", expand=True)

        # Treeview para mostrar ingredientes añadidos al menú en el frame inferior
        self.treeview_menu_ingredientes2 = ttk.Treeview(frame_inferior, columns=("Nombre", "Cantidad"), show="headings")
        self.treeview_menu_ingredientes2.heading("Nombre", text="Nombre")
        self.treeview_menu_ingredientes2.heading("Cantidad", text="Cantidad")
        self.treeview_menu_ingredientes2.pack(pady=10, padx=10, fill="both", expand=True)

        self.actualizar_combobox_ingredientes() 

    def crear_menu(self):
        """Crea un objeto Menu usando LogicaApp y limpia la interfaz."""

        nombre_menu = self.combo_box_menu_nombre.get().strip()
        descripcion_menu = self.entry_menu_descripcion.get().strip()

        try:
            precio_menu = float(self.entry_precio.get())
        except ValueError:
            messagebox.showerror("Error", "El precio debe ser un número válido.")
            return

        if not nombre_menu:
            messagebox.showerror("Error", "El nombre del menú no puede estar vacío.")
            return

        if not self.ingredientes_menu:
            messagebox.showerror("Error", "Debe agregar al menos un ingrediente.")
            return

        try:
            # Obtener la ruta de la imagen asociada al nombre del menú
            ruta_imagen = self.imagenes.get(nombre_menu, None)

            # Usar la capa lógica para crear el menú
            LogicaApp.crear_menu(nombre_menu, descripcion_menu, precio_menu, self.ingredientes_menu, ruta_imagen)
            messagebox.showinfo("Éxito", f"Menú '{nombre_menu}' creado correctamente.")

            # Limpiar campos
            self.combo_box_menu_nombre.set("")
            self.entry_menu_descripcion.delete(0, 'end')
            self.entry_precio.delete(0, 'end')
            self.treeview_menu_ingredientes2.delete(*self.treeview_menu_ingredientes2.get_children())
            self.ingredientes_menu.clear()

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al crear el menú: {e}")


    def actualizar_combobox_ingredientes(self):
        """Actualiza el Combobox usando la lógica de negocio."""
        nuevos_valores = LogicaApp.obtener_nombres_ingredientes()

        if self.combobox_ingredientes["values"] != tuple(nuevos_valores):
            self.combobox_ingredientes["values"] = nuevos_valores

        self.app.after(1000, self.actualizar_combobox_ingredientes)


    def agregar_ingrediente(self):
        ingrediente_seleccionado = self.combobox_ingredientes.get()
        try:
            cantidad_seleccionada = int(self.entry_cantidad2.get())
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número entero.")
            return

        ingrediente = LogicaApp.obtener_ingrediente_por_nombre(ingrediente_seleccionado)

        if ingrediente:
            if cantidad_seleccionada <= ingrediente.cantidad:
                for item in self.treeview_menu_ingredientes2.get_children():
                    values = self.treeview_menu_ingredientes2.item(item, "values")
                    if values[0] == ingrediente_seleccionado:
                        nueva_cantidad = int(values[1]) + cantidad_seleccionada
                        self.treeview_menu_ingredientes2.item(item, values=(ingrediente_seleccionado, nueva_cantidad))

                        for ing in self.ingredientes_menu:
                            if ing["nombre"] == ingrediente_seleccionado:
                                ing["cantidad"] = nueva_cantidad
                        break
                else:
                    self.treeview_menu_ingredientes2.insert("", "end", values=(ingrediente_seleccionado, cantidad_seleccionada))
                    self.ingredientes_menu.append({"nombre": ingrediente_seleccionado, "cantidad": cantidad_seleccionada})

                LogicaApp.descontar_cantidad_ingrediente(ingrediente_seleccionado, cantidad_seleccionada)
            else:
                messagebox.showerror("Error", f"No hay suficiente cantidad del ingrediente '{ingrediente_seleccionado}'.")
        else:
            messagebox.showerror("Error", f"El ingrediente '{ingrediente_seleccionado}' no existe.")


    def quitar_ingrediente(self):
        seleccion = self.treeview_menu_ingredientes2.selection()
        if seleccion:
            item = self.treeview_menu_ingredientes2.item(seleccion)
            ingrediente_nombre = item["values"][0]
            cantidad = int(item["values"][1])

            LogicaApp.restaurar_cantidad_ingrediente(ingrediente_nombre, cantidad)

            self.treeview_menu_ingredientes2.delete(seleccion)

            self.ingredientes_menu = [
                ing for ing in self.ingredientes_menu
                if ing["nombre"] != ingrediente_nombre or ing["cantidad"] != cantidad
            ]

            print(f"Ingrediente '{ingrediente_nombre}' quitado del menú y restaurado en base de datos.")
        else:
            messagebox.showwarning("Advertencia", "Seleccione un ingrediente para eliminar.")

    def crear_formulario_cliente(self, parent):
        """Crea el formulario en el Frame superior y el Treeview en el Frame inferior para la gestión de clientes."""
        # Frame superior para el formulario y botones
        frame_superior = ctk.CTkFrame(parent)
        frame_superior.pack(pady=10, padx=10, fill="x")

        ctk.CTkLabel(frame_superior, text="Nombre").grid(row=0, column=0, pady=10, padx=10)
        self.entry_nombre_cliente = ctk.CTkEntry(frame_superior)
        self.entry_nombre_cliente.grid(row=0, column=1, pady=10, padx=10)

        ctk.CTkLabel(frame_superior, text="Email").grid(row=0, column=2, pady=10, padx=10)
        self.entry_email = ctk.CTkEntry(frame_superior)
        self.entry_email.grid(row=0, column=3, pady=10, padx=10)

        ctk.CTkLabel(frame_superior, text="Edad").grid(row=0, column=4, pady=10, padx=10)
        self.entry_edad = ctk.CTkEntry(frame_superior)
        self.entry_edad.grid(row=0, column=5, pady=10, padx=10)

        # Botones alineados horizontalmente en el frame superior
        self.btn_crear_cliente = ctk.CTkButton(frame_superior, text="Crear Cliente", command=self.crear_cliente)
        self.btn_crear_cliente.grid(row=1, column=0, pady=10, padx=10)

        self.btn_actualizar_cliente = ctk.CTkButton(frame_superior, text="Actualizar Cliente", command=self.actualizar_cliente)
        self.btn_actualizar_cliente.grid(row=1, column=1, pady=10, padx=10)

        self.btn_eliminar_cliente = ctk.CTkButton(frame_superior, text="Eliminar Cliente", command=self.eliminar_cliente)
        self.btn_eliminar_cliente.grid(row=1, column=2, pady=10, padx=10)

        # Frame inferior para el Treeview
        frame_inferior = ctk.CTkFrame(parent)
        frame_inferior.pack(pady=10, padx=10, fill="both", expand=True)

        # Treeview para mostrar los clientes
        self.treeview_clientes = ttk.Treeview(frame_inferior, columns=("Email", "Nombre", "Edad"), show="headings")
        self.treeview_clientes.heading("Email", text="Email")
        self.treeview_clientes.heading("Nombre", text="Nombre")
        self.treeview_clientes.heading("Edad", text="Edad")
        self.treeview_clientes.pack(pady=10, padx=10, fill="both", expand=True)

        self.cargar_clientes()

    def cargar_clientes(self):
        self.treeview_clientes.delete(*self.treeview_clientes.get_children())
        clientes = LogicaApp.leer_clientes()
        for cliente in clientes:
            self.treeview_clientes.insert("", "end", values=(cliente.email, cliente.nombre, cliente.edad))

    def crear_cliente(self):
        nombre = self.entry_nombre_cliente.get()
        email = self.entry_email.get()
        edad = self.entry_edad.get()

        if not (nombre and email and edad):
            messagebox.showwarning("Campos Vacíos", "Por favor, ingrese todos los campos.")
            return

        cliente = LogicaApp.crear_cliente(nombre, email, edad)
        if cliente:
            messagebox.showinfo("Éxito", "Cliente creado correctamente.")
            self.cargar_clientes()
            self.actualizar_emails_combobox()
        else:
            messagebox.showwarning("Error", "El cliente ya existe.")

    def actualizar_cliente(self):
        selected_item = self.treeview_clientes.selection()
        if not selected_item:
            messagebox.showwarning("Selección", "Por favor, seleccione un cliente.")
            return

        email_viejo = self.treeview_clientes.item(selected_item)["values"][0]
        nombre = self.entry_nombre_cliente.get()
        email = self.entry_email.get()
        edad = self.entry_edad.get()

        if not (nombre and email and edad):
            messagebox.showwarning("Campos Vacíos", "Por favor, complete todos los campos.")
            return

        cliente_actualizado = LogicaApp.actualizar_cliente(email_viejo, nombre, email, edad)
        if cliente_actualizado:
            messagebox.showinfo("Éxito", "Cliente actualizado correctamente.")
            self.cargar_clientes()
        else:
            messagebox.showwarning("Error", "No se pudo actualizar el cliente.")

    def eliminar_cliente(self):
        selected_item = self.treeview_clientes.selection()
        if not selected_item:
            messagebox.showwarning("Selección", "Por favor, seleccione un cliente.")
            return

        email = self.treeview_clientes.item(selected_item)["values"][0]
        LogicaApp.eliminar_cliente(email)
        messagebox.showinfo("Éxito", "Cliente eliminado correctamente.")
        self.cargar_clientes()
        self.actualizar_emails_combobox()

    def crear_formulario_panel_de_compra(self, parent):
            """Crea el formulario en el Frame superior y el Treeview en el Frame inferior para la gestión de clientes."""
            # Frame superior para el formulario y botones
            frame_superior = ctk.CTkFrame(parent)
            frame_superior.pack(pady=10, padx=10, fill="x")

            ctk.CTkLabel(frame_superior, text="Menú").grid(row=0, column=0, pady=10, padx=10)
            self.menu_panel = ctk.CTkComboBox(frame_superior)
            self.menu_panel.grid(row=0, column=1, pady=10, padx=10)
            self.actualizar_menu_combobox()

            # Combobox para seleccionar el email del cliente
            ctk.CTkLabel(frame_superior, text="Clientes").grid(row=0, column=2, pady=10, padx=10)
            self.combobox_cliente_email = ctk.CTkComboBox(frame_superior)
            self.combobox_cliente_email.grid(row=0, column=3, pady=10, padx=10)
            self.actualizar_emails_combobox()  # Llenar el combobox con emails de los clientes

            # Botón para cargar compras
            self.btn_agr_compra = ctk.CTkButton(frame_superior, text="Cargar compras", command=self.cargar_compras)
            self.btn_agr_compra.grid(row=1, column=0, pady=10, padx=10)

            # Frame inferior para el Treeview
            frame_inferior = ctk.CTkFrame(parent)
            frame_inferior.pack(pady=10, padx=10, fill="both", expand=True)

            # Treeview para mostrar los clientes
            self.treeview_panel = ttk.Treeview(frame_inferior, columns=("Cliente", "Menú", "Cantidad", "Precio"), show="headings")
            self.treeview_panel .heading("Cliente", text="Cliente")
            self.treeview_panel.heading("Menú", text="Menú")
            self.treeview_panel.heading("Cantidad", text="Cantidad")
            self.treeview_panel.heading("Precio", text="Precio")
            
            self.treeview_panel.grid(row=0, column=0, pady=10, padx=10, sticky="nsew")

            # Configuración de expansión para Treeview
            frame_inferior.grid_rowconfigure(0, weight=1)
            frame_inferior.grid_columnconfigure(0, weight=1)

    def cargar_compras(self):
        """Agrega los datos seleccionados al Treeview."""
        menu_seleccionado = self.menu_panel.get()
        email_seleccionado = self.combobox_cliente_email.get()

        if not menu_seleccionado:
            messagebox.showerror("Error", "Por favor, selecciona un menú.")
            return

        if not email_seleccionado:
            messagebox.showerror("Error", "Por favor, selecciona un cliente.")
            return

        cliente, menu = LogicaApp.obtener_cliente_y_menu(email_seleccionado, menu_seleccionado)

        if not cliente:
            messagebox.showerror("Error", "Cliente no encontrado.")
            return

        if not menu:
            messagebox.showerror("Error", "Menú no encontrado.")
            return

        cantidad = 1
        precio = menu.precio

        # Verificar si ya existe una fila con este cliente y menú
        for item in self.treeview_panel.get_children():
            valores = self.treeview_panel.item(item, "values")
            if valores[0] == cliente.email and valores[1] == menu.nombre:
                cantidad_actual = int(valores[2])
                cantidad += cantidad_actual
                total_precio = cantidad * precio
                self.treeview_panel.item(item, values=(cliente.email, menu.nombre, cantidad, total_precio))
                return

        total_precio = cantidad * precio
        self.treeview_panel.insert("", "end", values=(cliente.email, menu.nombre, cantidad, total_precio))

    def actualizar_emails_combobox(self):
        """Llena el Combobox con los emails de los clientes."""
        emails = LogicaApp.obtener_emails_clientes()
        self.combobox_cliente_email.configure(values=emails)

    def actualizar_menu_combobox(self):
        """Llena el Combobox con los nombres de los menús disponibles."""
        nombres_menus = LogicaApp.obtener_nombres_menus()
        self.menu_panel.configure(values=nombres_menus)


    def crear_formulario_pedido(self, parent):
            # Frame superior para el formulario y botones
            frame_superior = ctk.CTkFrame(parent)
            frame_superior.pack(pady=10, padx=10, fill="x")

            ctk.CTkLabel(frame_superior, text="Cliente Email").grid(row=0, column=0, pady=10, padx=10)
            self.combobox_cliente_email_pedido = ttk.Combobox(frame_superior, state="readonly")
            self.combobox_cliente_email_pedido.grid(row=0, column=1, pady=10, padx=10)
            self.actualizar_emails_combobox_pedidos()

            #Este botón no está funcionando
            self.btn_actualizar_pedidos = ctk.CTkButton(frame_superior, text="Actualizar datos", command=self.cargar_pedidos_por_cliente)
            self.btn_actualizar_pedidos.grid(row=0, column=2, pady=10, padx=10)

            # Asociamos el evento de selección de un email a una función
            self.combobox_cliente_email_pedido.bind("<<ComboboxSelected>>", self.cargar_pedidos_por_cliente)

            # Frame inferior para el Treeview
            frame_inferior = ctk.CTkFrame(parent)
            frame_inferior.pack(pady=10, padx=10, fill="both", expand=True)

            # Treeview para mostrar los pedidos
            self.treeview_pedidos = ttk.Treeview(frame_inferior, columns=("ID", "Descripción", "Total del Pedido", "Fecha de Creación", "Cantidad de Menús comprados"), show="headings")
            self.treeview_pedidos.heading("ID", text="ID", command=lambda: self.ordenar_treeview(self.treeview_pedidos, columna=0))
            self.treeview_pedidos.heading("Descripción", text="Descripción", command=lambda: self.ordenar_treeview(self.treeview_pedidos, columna=1))
            self.treeview_pedidos.heading("Total del Pedido", text="Total del Pedido", command=lambda: self.ordenar_treeview(self.treeview_pedidos, columna=2))
            self.treeview_pedidos.heading("Fecha de Creación", text="Fecha de Creación", command=lambda: self.ordenar_treeview(self.treeview_pedidos, columna=3))
            self.treeview_pedidos.heading("Cantidad de Menús comprados", text="Cantidad de Menús comprados", command=lambda: self.ordenar_treeview(self.treeview_pedidos, columna=4))
            
            self.treeview_pedidos.pack(pady=10, padx=10, fill="both", expand=True)

    def actualizar_emails_combobox_pedidos(self):
        """Llena el Combobox con los emails de los clientes."""
        emails = LogicaApp.obtener_emails_clientes()
        self.combobox_cliente_email_pedido.configure(values=emails)

    
    def cargar_pedidos_por_cliente(self, event=None):
        """Carga los pedidos del cliente seleccionado en el Treeview."""
        cliente_email = self.combobox_cliente_email_pedido.get()

        if cliente_email:
            self.treeview_pedidos.delete(*self.treeview_pedidos.get_children())
            pedidos = LogicaApp.obtener_pedidos_por_cliente(cliente_email)

            for pedido in pedidos:
                self.treeview_pedidos.insert(
                    "", "end",
                    values=(pedido.id, pedido.descripcion, pedido.total, pedido.fecha_creacion, pedido.cantidad_menus)
                )

    
    def crear_formulario_grafico(self, parent):
        """Crea el formulario para seleccionar y mostrar gráficos estadísticos."""
        # Frame superior para selección del gráfico
        frame_superior = ctk.CTkFrame(parent)
        frame_superior.pack(pady=10, padx=10, fill="x")

        # Menú desplegable para seleccionar el tipo de gráfico
        ctk.CTkLabel(frame_superior, text="Selecciona un tipo de gráfico:").grid(row=0, column=0, pady=10, padx=10)
        self.combo_graficos = ctk.CTkComboBox(frame_superior, values=["Ventas por Fecha", "Menús Más Comprados", "Uso de Ingredientes"])
        self.combo_graficos.grid(row=0, column=1, pady=10, padx=10)

        # Botón para generar el gráfico
        self.btn_generar_grafico = ctk.CTkButton(frame_superior, text="Generar Gráfico", command=self.generar_grafico)
        self.btn_generar_grafico.grid(row=0, column=2, pady=10, padx=10)

    def generar_grafico(self):
        """Genera el gráfico según la opción seleccionada."""
        tipo_grafico = self.combo_graficos.get()

        if tipo_grafico == "Ventas por Fecha":
            LogicaApp.graficar_ventas_por_fecha()
        elif tipo_grafico == "Menús Más Comprados":
            LogicaApp.graficar_menus_mas_comprados()
        elif tipo_grafico == "Uso de Ingredientes":
            LogicaApp.graficar_uso_ingredientes()
        else:
            messagebox.showwarning("Advertencia", "Selecciona un tipo de gráfico válido.")


    def ordenar_treeview(self, treeview, columna, reverse=None):
        # Si reverse es None, alterna el orden
        if reverse is None:
            reverse = False if not hasattr(self, 'reverse_order') else not self.reverse_order
            self.reverse_order = reverse

        # Obtener los elementos del Treeview en forma de lista de tuplas
        datos = [(treeview.item(item)["values"], item) for item in treeview.get_children()]
        
        # Ordenar los datos según la columna seleccionada
        datos.sort(key=lambda x: x[0][columna], reverse=reverse)
        
        # Reinsertar los elementos en el Treeview en el orden correcto
        for index, (valor, item) in enumerate(datos):
            treeview.item(item, values=valor)

    def cargar_imagenes_en_combobox_menu(self):
        """Carga las imágenes de la carpeta Images y las asocia con nombres en el ComboBox del menú."""
        carpeta_actual = os.path.dirname(os.path.abspath(__file__))
        carpeta_imagenes = os.path.join(carpeta_actual, "Images")

        nombres_personalizados = ["Papas fritas", "Completo", "Hamburguesa", "Bebida"]  # Nombres personalizados

        # Verificar que hay 4 imágenes en la carpeta
        imagenes = [f for f in os.listdir(carpeta_imagenes) if f.endswith((".png", ".jpg", ".jpeg"))]
        if len(imagenes) != 4:
            messagebox.showerror("Error", "La carpeta 'Images' debe contener exactamente 4 imágenes.")
            return

        # Asociar nombres personalizados con imágenes
        self.imagenes = {}  # Diccionario para mapear nombres a rutas de imágenes
        for nombre, archivo_imagen in zip(nombres_personalizados, imagenes):
            ruta_imagen = os.path.join(carpeta_imagenes, archivo_imagen)
            self.imagenes[nombre] = ruta_imagen  # Guardar la ruta de la imagen

        # Agregar los nombres personalizados al ComboBox del menú
        self.combo_box_menu_nombre.configure(values=nombres_personalizados)


    def crear_panel_estado_pedido(self, parent):
        from database import SessionLocal
        from models import Pedido
        from pedido_state import obtener_estado_instancia

        frame = ctk.CTkFrame(parent)
        frame.pack(pady=10, padx=10, fill="x")

        ctk.CTkLabel(frame, text="ID del Pedido:").grid(row=0, column=0, padx=5, pady=5)
        entry_id = ctk.CTkEntry(frame)
        entry_id.grid(row=0, column=1, padx=5, pady=5)

        def avanzar_estado():
            try:
                pedido_id = int(entry_id.get())
                db = SessionLocal()
                pedido = db.query(Pedido).get(pedido_id)
                if not pedido:
                    messagebox.showerror("Error", "Pedido no encontrado.")
                    return

                estado_actual = obtener_estado_instancia(pedido.estado)
                estado_actual.avanzar(pedido)
                db.commit()
                messagebox.showinfo("Estado actualizado", f"Nuevo estado: {pedido.estado}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        def cancelar_pedido():
            try:
                pedido_id = int(entry_id.get())
                db = SessionLocal()
                pedido = db.query(Pedido).get(pedido_id)
                if not pedido:
                    messagebox.showerror("Error", "Pedido no encontrado.")
                    return

                estado_actual = obtener_estado_instancia(pedido.estado)
                estado_actual.cancelar(pedido)
                db.commit()
                messagebox.showinfo("Pedido cancelado", f"Estado actual: {pedido.estado}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(frame, text="Avanzar Estado", command=avanzar_estado).grid(row=1, column=0, pady=10, padx=5)
        ctk.CTkButton(frame, text="Cancelar Pedido", command=cancelar_pedido).grid(row=1, column=1, pady=10, padx=5)
