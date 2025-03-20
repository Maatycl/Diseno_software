import customtkinter as ctk
from tkinter import messagebox, ttk
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from datetime import datetime
from database import get_session
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from graficos import graficar_ventas_por_fecha, graficar_menus_mas_comprados, graficar_uso_ingredientes
from crud.ingrediente_crud import IngredienteCRUD
from crud.menu_crud import MenuCRUD
from crud.cliente_crud import ClienteCRUD
from crud.pedido_crud import PedidoCRUD
from database import get_session, engine, Base
from models import Ingrediente, Menu, MenuIngrediente, Pedido, Cliente
from graficos import graficar_menus_mas_comprados, graficar_uso_ingredientes, graficar_ventas_por_fecha
# Configuración de la ventana principal
ctk.set_appearance_mode("System")  # Opciones: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # Opciones: "blue", "green", "dark-blue"
# Crear las tablas en la base de datos
# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Gestión de Clientes, Pedidos y menús")
        self.geometry("1450x600")

        # Crear el Tabview (pestañas)
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(pady=20, padx=20, fill="both", expand=True)

        # Pestaña de Ingredientes
        self.tab_ingredientes = self.tabview.add("Ingredientes")
        self.crear_formulario_ingrediente(self.tab_ingredientes)

        # Pestaña de Clientes
        self.tab_menu = self.tabview.add("Menus")
        self.crear_formulario_menu(self.tab_menu) 

        # Pestaña de Clientes
        self.tab_clientes = self.tabview.add("Clientes")
        self.crear_formulario_cliente(self.tab_clientes)

        # Pestaña de Panel de compra
        self.tab_clientes = self.tabview.add("Panel de compra")
        self.crear_formulario_panel_de_compra(self.tab_clientes)            #cambiar

        # Pestaña de Pedidos
        self.tab_pedidos = self.tabview.add("Pedidos")
        self.crear_formulario_pedido(self.tab_pedidos)

        # Pestaña de Graficos
        self.tab_graficos = self.tabview.add("Graficos")
        self.crear_formulario_grafico(self.tab_graficos)

        # Revisar el cambio de pestaña periódicamente
        self.current_tab = self.tabview.get()  # Almacena la pestaña actual
        self.after(500, self.check_tab_change)  # Llama a check_tab_change cada 500 ms

        self.ingredientes_menu = []

    def check_tab_change(self):
        """Revisa si la pestaña activa cambió a 'Pedidos'."""
        new_tab = self.tabview.get()
        if new_tab != self.current_tab:
            self.current_tab = new_tab
            if new_tab == "Panel de compra":
                self.actualizar_menu_combobox()
            if new_tab == "Pedidos":
                self.actualizar_emails_combobox_pedidos()
        self.after(500, self.check_tab_change)  # Vuelve a revisar cada 500 ms


##### Formularios #####

    def crear_formulario_ingrediente(self, parent):
        """Crea el formulario en el Frame superior y el Treeview en el Frame inferior para la gestión de clientes."""
        # Frame superior para el formulario y botones
        frame_superior = ctk.CTkFrame(parent)
        frame_superior.pack(pady=10, padx=10, fill="x")

        # Fila 1 - Elementos de la primera fila, no alineados con la segunda fila
        ctk.CTkLabel(frame_superior, text="Nombre").grid(row=0, column=0, pady=10, padx=10)
        self.entry_nombre = ctk.CTkEntry(frame_superior)
        self.entry_nombre.grid(row=0, column=1, pady=10, padx=10)

        ctk.CTkLabel(frame_superior, text="Tipo").grid(row=0, column=2, pady=10, padx=10)
        self.entry_tipo = ctk.CTkEntry(frame_superior)
        self.entry_tipo.grid(row=0, column=3, pady=10, padx=10)

        ctk.CTkLabel(frame_superior, text="Cantidad").grid(row=0, column=4, pady=10, padx=10)
        self.entry_cantidad = ctk.CTkEntry(frame_superior)
        self.entry_cantidad.grid(row=0, column=5, pady=10, padx=10)

        ctk.CTkLabel(frame_superior, text="Unidad").grid(row=0, column=6, pady=10, padx=10)
        self.entry_unidad = ctk.CTkEntry(frame_superior)
        self.entry_unidad.grid(row=0, column=7, pady=10, padx=10)

        # Fila 2 - Botones alineados horizontalmente en la segunda fila
        self.btn_crear_ingrediente = ctk.CTkButton(frame_superior, text="Añadir Ingrediente", command=self.crear_ingrediente)
        self.btn_crear_ingrediente.grid(row=1, column=1, pady=10, padx=10)

        self.btn_actualizar_ingrediente = ctk.CTkButton(frame_superior, text="Actualizar Ingrediente", command=self.actualizar_ingrediente)
        self.btn_actualizar_ingrediente.grid(row=1, column=3, pady=10, padx=10)

        self.btn_eliminar_ingrediente = ctk.CTkButton(frame_superior, text="Eliminar Ingrediente", command=self.eliminar_ingrediente)
        self.btn_eliminar_ingrediente.grid(row=1, column=5, pady=10, padx=10)

        self.btn_actualizar_ingrediente = ctk.CTkButton(frame_superior, text="Actualizar datos", command=self.cargar_ingredientes)
        self.btn_actualizar_ingrediente.grid(row=1, column=10, pady=10, padx=10)

        # Frame inferior para el Treeview
        frame_inferior = ctk.CTkFrame(parent)
        frame_inferior.pack(pady=10, padx=10, fill="both", expand=True)

        # Treeview para mostrar los ingredientes
        self.treeview_ingredientes = ttk.Treeview(frame_inferior, columns=("Nombre", "Tipo", "Cantidad","Unidad de medida"), show="headings")
        self.treeview_ingredientes.heading("Nombre", text="Nombre")
        self.treeview_ingredientes.heading("Tipo", text="Tipo")
        self.treeview_ingredientes.heading("Cantidad", text="Cantidad")
        self.treeview_ingredientes.heading("Unidad de medida", text="Unidad de medida")
        self.treeview_ingredientes.pack(pady=10, padx=10, fill="both", expand=True)

        self.cargar_ingredientes()

    def crear_formulario_menu(self, parent):
        """Crea el formulario para crear un menú y seleccionar ingredientes."""
        # Frame superior
        frame_superior = ctk.CTkFrame(parent)
        frame_superior.pack(pady=10, padx=10, fill="x")

        # Fila para el nombre y descripción del menú
        ctk.CTkLabel(frame_superior, text="Nombre del Menú").grid(row=0, column=0, pady=10, padx=10)
        self.entry_menu_nombre = ctk.CTkEntry(frame_superior)
        self.entry_menu_nombre.grid(row=0, column=1, pady=10, padx=10)

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

        # Botón alinead horizontalmente en el frame inferior
        self.btn_pdf = ctk.CTkButton(frame_inferior, text="Crear boleta", command=self.crear_boleta)
        self.btn_pdf.grid(row=1, column=0, pady=10, padx=10)

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

    def crear_formulario_pedido(self, parent):
        """Crea el formulario en el Frame superior y el Treeview en el Frame inferior para la gestión de pedidos."""
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
            graficar_ventas_por_fecha()
        elif tipo_grafico == "Menús Más Comprados":
            graficar_menus_mas_comprados()
        elif tipo_grafico == "Uso de Ingredientes":
            graficar_uso_ingredientes()
        else:
            messagebox.showwarning("Advertencia", "Selecciona un tipo de gráfico válido.")

    def generar_pdf(self, cliente, menu_seleccionado, cantidad, total, fecha_creacion):
        # Nombre del archivo PDF
        archivo_pdf = f"boleta_{cliente.nombre}_{fecha_creacion.strftime('%Y-%m-%d_%H-%M-%S')}.pdf"

        # Crear el objeto canvas (PDF)
        c = canvas.Canvas(archivo_pdf, pagesize=letter)
        width, height = letter  # Dimensiones de la página

        # Margenes
        margen_x = 50
        margen_y = height - 50
        linea_separacion = 20

        # Encabezado
        c.setFillColor(colors.lightgrey)
        c.rect(0, height - 80, width, 80, fill=1)
        c.setFillColor(colors.black)
        c.setFont("Times-Italic", 18)
        c.drawString(margen_x, height - 40, "Universidad Católica de Temuco")  # Subir el título
        c.setFont("Times-Italic", 12)
        c.drawString(margen_x, height - 60, "Boleta de Pedido")  # Subir el subtítulo

        # Número de boleta
        numero_boleta = f"{fecha_creacion.strftime('%Y%m%d')}-{datetime.now().strftime('%H%M%S')}"
        margen_y -= 70  # Ajustar espacio después del título
        c.setFont("Times-Italic", 12)
        c.drawString(margen_x, margen_y, f"Número de Boleta: {numero_boleta}")
        
        # Línea divisoria
        margen_y -= 15  # Aumentar espacio entre el contenido y la línea
        c.setLineWidth(0.5)
        c.setStrokeColor(colors.grey)
        c.line(margen_x, margen_y, width - margen_x, margen_y)
        
        # Información del cliente
        margen_y -= 30
        c.setFont("Times-Italic", 12)
        c.drawString(margen_x, margen_y, "Información del Cliente:")
        c.setFont("Times-Italic", 11)
        c.drawString(margen_x, margen_y - linea_separacion, f"Nombre: {cliente.nombre}")
        c.drawString(margen_x, margen_y - 2 * linea_separacion, f"Email: {cliente.email}")
        
        # Detalles del pedido en tabla
        margen_y -= 80
        c.setFont("Times-Italic", 12)
        c.drawString(margen_x, margen_y, "Detalles del Pedido:")
        
        datos_pedido = [["Menú", "Cantidad", "Precio Unitario (CLP)", "Total (CLP)"],
                        [menu_seleccionado, cantidad, f"{total / cantidad:.2f}", f"{total}"]]
        
        tabla = Table(datos_pedido, colWidths=[150, 100, 150, 100])
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Times-Italic'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        tabla.wrapOn(c, margen_x, margen_y - 50)
        tabla.drawOn(c, margen_x, margen_y - 100)
        
        # Fecha y hora de creación
        margen_y -= 150
        c.setFont("Times-Italic", 11)
        c.drawString(margen_x, margen_y, f"Fecha de creación: {fecha_creacion.strftime('%Y-%m-%d')}")
        c.drawString(margen_x, margen_y - linea_separacion, f"Hora de creación: {datetime.now().strftime('%H:%M:%S')}")

        # Pie de página
        c.setFont("Times-Italic", 10)
        c.setFillColor(colors.darkgrey)
        c.drawString(margen_x, 30, "Gracias por su preferencia. Si tiene dudas, contáctenos.")

        # Guardar el PDF
        c.save()
        return archivo_pdf
    
    def crear_boleta(self):
        """Generar boleta y guardar en la base de datos."""
        # Obtener los datos del Treeview
        item_seleccionado = self.treeview_panel.focus()
        if not item_seleccionado:
            messagebox.showerror("Error", "Por favor, selecciona un pedido.")
            return

        datos_pedido = self.treeview_panel.item(item_seleccionado)["values"]
        if len(datos_pedido) < 3:
            messagebox.showerror("Error", "Faltan datos para generar la boleta.")
            return

        nombre_cliente, menu_seleccionado, cantidad = datos_pedido[:3]

        # Conectar a la base de datos
        db = next(get_session())

        # Buscar cliente y menú
        cliente = ClienteCRUD.leer_cliente_por_email(db, nombre_cliente)
        menu = MenuCRUD.leer_menu_por_nombre(db, menu_seleccionado)

        if not cliente:
            messagebox.showerror("Error", "Cliente no encontrado.")
            db.close()
            return

        if not menu:
            messagebox.showerror("Error", "Menú no encontrado.")
            db.close()
            return

        try:
            cantidad = int(cantidad)  # Validar cantidad como número
        except ValueError:
            messagebox.showerror("Error", "Cantidad debe ser un número.")
            db.close()
            return

        total = menu.precio * cantidad
        fecha_creacion = datetime.now()

        # Crear la boleta en formato PDF
        archivo_pdf = self.generar_pdf(cliente, menu_seleccionado, cantidad, total, fecha_creacion)

        # Insertar el pedido en la base de datos
        nuevo_pedido = Pedido(
            descripcion=f"Pedido de {menu_seleccionado} para {cliente.nombre}",
            total=total,
            cantidad_menus=cantidad,
            fecha_creacion=fecha_creacion,
            cliente_id=cliente.id,
        )
        db.add(nuevo_pedido)
        if not PedidoCRUD._try_commit(db):
            messagebox.showerror("Error", "No se pudo guardar el pedido en la base de datos.")
            db.close()
            return

        # Confirmar creación
        messagebox.showinfo("Éxito", f"Boleta generada con éxito. El archivo PDF está en: {archivo_pdf}")
        db.close()

    # Método para actualizar los menús en el Combobox
    def actualizar_menu_combobox(self):
        """Llena el Combobox con los menus de los clientes."""
        db = next(get_session())
        menu = [menu.nombre for menu in MenuCRUD.leer_menus(db)]
        self.menu_panel.configure(values=menu)
        db.close()

    

    def cargar_compras(self):
        """Agrega los datos seleccionados al Treeview."""
        # Obtener el menú seleccionado
        menu_seleccionado = self.menu_panel.get()

        # Validar si hay un menú seleccionado
        if not menu_seleccionado:
            messagebox.showerror("Error", "Por favor, selecciona un menú.")
            return

        # Obtener el cliente seleccionado
        email_seleccionado = self.combobox_cliente_email.get()
        if not email_seleccionado:
            messagebox.showerror("Error", "Por favor, selecciona un cliente.")
            return

        # Conectar a la base de datos
        db = next(get_session())

        # Buscar el cliente y menú en la base de datos
        cliente = ClienteCRUD.leer_cliente_por_email(db, email_seleccionado)
        menu = MenuCRUD.leer_menu_por_nombre(db, menu_seleccionado, )

        if not cliente:
            messagebox.showerror("Error", "Cliente no encontrado.")
            db.close()
            return

        if not menu:
            messagebox.showerror("Error", "Menú no encontrado.")
            db.close()
            return

        # Obtener datos
        nombre_cliente = cliente.email  # Cambiado
        cantidad = 1
        precio = menu.precio  

        # Verificar si ya existe una fila con este cliente y menú
        for item in self.treeview_panel.get_children():
            valores = self.treeview_panel.item(item, "values")
            cliente_existente = valores[0]
            menu_existente = valores[1]

            if cliente_existente == nombre_cliente and menu_existente == menu_seleccionado:
                # Actualizar la cantidad en la fila existente
                cantidad_actual = int(valores[2])
                cantidad += cantidad_actual
                total_precio = cantidad * precio
                self.treeview_panel.item(item, values=(cliente.email, menu_seleccionado, cantidad, total_precio))
                db.close()
                return
            
        total_precio = cantidad * precio

        # Insertar en el Treeview
        self.treeview_panel.insert("", "end", values=(cliente.email, menu_seleccionado, cantidad, total_precio))

        # Cerrar conexión
        db.close()
   
   # Método para actualizar los correos electrónicos en el Combobox
    def actualizar_emails_combobox(self):
        """Llena el Combobox con los emails de los clientes."""
        db = next(get_session())
        emails = [cliente.email for cliente in ClienteCRUD.leer_clientes(db)]
        self.combobox_cliente_email.configure(values=emails)
        db.close()

    def actualizar_emails_combobox_pedidos(self):
        """Llena el Combobox con los emails de los clientes."""
        db = next(get_session())
        emails = [cliente.email for cliente in ClienteCRUD.leer_clientes(db)]
        self.combobox_cliente_email_pedido.configure(values=emails)
        db.close()

    # Métodos CRUD para Clientes
    def cargar_clientes(self):
        db = next(get_session())
        self.treeview_clientes.delete(*self.treeview_clientes.get_children())
        clientes = ClienteCRUD.leer_clientes(db)
        for cliente in clientes:
            self.treeview_clientes.insert("", "end", values=(cliente.email, cliente.nombre, cliente.edad))
        db.close()

    def crear_cliente(self):
        nombre = self.entry_nombre_cliente.get()
        email = self.entry_email.get()
        edad = self.entry_edad.get()
        if nombre and email and edad:
            db = next(get_session())
            cliente = ClienteCRUD.crear_cliente(db, nombre, email, edad)
            if cliente:
                messagebox.showinfo("Éxito", "Cliente creado correctamente.")
                self.cargar_clientes()
                self.actualizar_emails_combobox()  # Actualizar el Combobox con el nuevo email
            else:
                messagebox.showwarning("Error", "El cliente ya existe.")
            db.close()
        else:
            messagebox.showwarning("Campos Vacíos", "Por favor, ingrese todos los campos.")

    def actualizar_cliente(self):
        selected_item = self.treeview_clientes.selection()
        if not selected_item:
            messagebox.showwarning("Selección", "Por favor, seleccione un cliente.")
            return
        nombre = self.entry_nombre_cliente.get()
        email = self.entry_email.get()
        edad = self.entry_edad.get()
        if not nombre.strip():
            messagebox.showwarning("Campo Vacío", "Por favor, ingrese un nombre.")
            return
        if not email.strip():
            messagebox.showwarning("Campo Vacío", "Por favor, ingrese un email.")
            return
        email_viejo = self.treeview_clientes.item(selected_item)["values"][0]
        nombre = self.entry_nombre_cliente.get()
        edad=self.entry_edad.get()
        if nombre:
            db = next(get_session())
            cliente_actualizado = ClienteCRUD.actualizar_cliente(db, email_viejo, nombre,email,edad)
            if cliente_actualizado:
                messagebox.showinfo("Éxito", "Cliente actualizado correctamente.")
                self.cargar_clientes()
            else:
                messagebox.showwarning("Error", "No se pudo actualizar el cliente.")
            db.close()
        else:
            messagebox.showwarning("Campos Vacíos", "Por favor, ingrese el nombre.")

    def eliminar_cliente(self):
        selected_item = self.treeview_clientes.selection()
        if not selected_item:
            messagebox.showwarning("Selección", "Por favor, seleccione un cliente.")
            return
        email = self.treeview_clientes.item(selected_item)["values"][0]
        db = next(get_session())
        ClienteCRUD.eliminar_cliente(db, email,)
        messagebox.showinfo("Éxito", "Cliente eliminado correctamente.")
        self.cargar_clientes()
        self.actualizar_emails_combobox()  # Actualizar el Combobox después de eliminar
        db.close()


    def cargar_pedidos_por_cliente(self, event):
        """Carga los pedidos del cliente seleccionado en el Treeview"""
        cliente_email = self.combobox_cliente_email_pedido.get()  # Obtener el email seleccionado del combobox

        # Si se ha seleccionado un email, proceder con la carga de los pedidos
        if cliente_email:
            db = next(get_session())
            self.treeview_pedidos.delete(*self.treeview_pedidos.get_children())  # Limpiar el Treeview antes de llenarlo
            pedidos = PedidoCRUD.leer_pedidos_por_cliente(db, cliente_email)  # Modificar el CRUD para aceptar un filtro de cliente
            for pedido in pedidos:
                # Suponiendo que la descripción, total y otros datos están disponibles en el objeto pedido
                self.treeview_pedidos.insert("", "end", values=(pedido.id, pedido.descripcion, pedido.total, pedido.fecha_creacion, pedido.cantidad_menus))
            db.close()

    def ordenar_treeview(self, treeview, columna, reverse=None):
        """
        Ordena el Treeview según la columna especificada.
        :param treeview: El widget Treeview que contiene los datos.
        :param columna: La columna por la cual ordenar (en base a su índice o nombre).
        :param reverse: Si se debe ordenar de manera descendente o ascendente.
        """
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

    def crear_pedido(self):
        cliente_email = self.combobox_cliente_email.get()
        descripcion = self.entry_descripcion.get()
        if cliente_email and descripcion:
            db = next(get_session())
            pedido = PedidoCRUD.crear_pedido(db, cliente_email, descripcion)
            if pedido:
                messagebox.showinfo("Éxito", "Pedido creado correctamente.")
                self.cargar_pedidos()
            else:
                messagebox.showwarning("Error", "No se pudo crear el pedido.")
            db.close()
        else:
            messagebox.showwarning("Campos Vacíos", "Por favor, ingrese todos los campos.")

    def actualizar_pedido(self):
        selected_item = self.treeview_pedidos.selection()
        if not selected_item:
            messagebox.showwarning("Selección", "Por favor, seleccione un pedido.")
            return
        pedido_id = self.treeview_pedidos.item(selected_item)["values"][0]
        descripcion = self.entry_descripcion.get()
        if descripcion:
            db = next(get_session())
            pedido_actualizado = PedidoCRUD.actualizar_pedido(db, pedido_id, descripcion)
            if pedido_actualizado:
                messagebox.showinfo("Éxito", "Pedido actualizado correctamente.")
                self.cargar_pedidos()
            else:
                messagebox.showwarning("Error", "No se pudo actualizar el pedido.")
            db.close()
        else:
            messagebox.showwarning("Campos Vacíos", "Por favor, ingrese la descripción.")

    def eliminar_pedido(self):
        selected_item = self.treeview_pedidos.selection()
        if not selected_item:
            messagebox.showwarning("Selección", "Por favor, seleccione un pedido.")
            return
        pedido_id = self.treeview_pedidos.item(selected_item)["values"][0]
        db = next(get_session())
        PedidoCRUD.borrar_pedido(db, pedido_id)
        messagebox.showinfo("Éxito", "Pedido eliminado correctamente.")
        self.cargar_pedidos()
        db.close()
        
    def crear_ingrediente(self):
        nombre = self.entry_nombre.get()
        tipo = self.entry_tipo.get()
        cantidad = self.entry_cantidad.get()
        unidad = self.entry_unidad.get()
        if nombre and tipo and cantidad and unidad:
            db = next(get_session())
            ingrediente = IngredienteCRUD.crear_ingrediente(db, nombre, tipo, cantidad, unidad)
            if ingrediente:
                messagebox.showinfo("Exito","Ingrediente ingresado correctamente")
                self.cargar_ingredientes()
            else:
                messagebox.showwarning("Error", "El ingrediente ya existe.")
            db.close()
        else:
            messagebox.showwarning("Campos Vacíos", "Por favor, ingrese todos los campos.")


    def actualizar_ingrediente(self):
        selected_item = self.treeview_ingredientes.selection()
        if not selected_item:
            messagebox.showwarning("Selección", "Por favor, seleccione un ingrediente.")
            return
    
        # Obteniendo valores de los campos de entrada
        nombre = self.entry_nombre.get().strip()
        tipo = self.entry_tipo.get().strip()
        cantidad = self.entry_cantidad.get().strip()
        unidad = self.entry_unidad.get().strip()
    
        # Validación de campos
        if not nombre:
            messagebox.showwarning("Campo Vacío", "Por favor, ingrese un nombre.")
            return
        if not tipo:
            messagebox.showwarning("Campo Vacío", "Por favor, ingrese un tipo.")
            return
        if not cantidad:
            messagebox.showwarning("Campo Vacío", "Por favor, ingrese una cantidad.")
            return
        if not unidad:
            messagebox.showwarning("Campo Vacío", "Por favor, ingrese una unidad.")
            return
    
        # Nombre viejo para actualizar
        nombre_viejo = self.treeview_ingredientes.item(selected_item)["values"][0]
    
        # Conexión a la base de datos y actualización
        db = next(get_session())
        ingrediente_actualizado = IngredienteCRUD.actualizar_ingrediente(db, nombre_viejo,nombre, tipo, cantidad, unidad)
        db.close()
    
        # Verificación de resultado
        if ingrediente_actualizado:
            messagebox.showinfo("Éxito", "Cliente actualizado correctamente.")
            self.cargar_ingredientes()
        else:
            messagebox.showwarning("Error", "No se pudo actualizar el cliente.")


    def eliminar_ingrediente(self):
        selected_item = self.treeview_ingredientes.selection()
        if not selected_item:
            messagebox.showwarning("Selección", "Por favor, seleccione un ingrediente.")
            return
        nombre = self.treeview_ingredientes.item(selected_item)["values"][0]
        db = next(get_session())
        IngredienteCRUD.borrar_ingrediente(db, nombre)
        messagebox.showinfo("Éxito", "Ingrediente eliminado correctamente.")
        self.cargar_ingredientes()

        db.close()

    def cargar_ingredientes(self):
        db = next(get_session())
        self.treeview_ingredientes.delete(*self.treeview_ingredientes.get_children())
        ingredientes = IngredienteCRUD.leer_ingredientes(db)
        for ingrediente in ingredientes:
            self.treeview_ingredientes.insert("", "end", values=(ingrediente.nombre, ingrediente.tipo,ingrediente.cantidad,ingrediente.unidad))
        db.close()

    def actualizar_combobox_ingredientes(self):
        """Actualiza el Combobox con los ingredientes disponibles en la base de datos."""
        db = next(get_session())
        ingredientes = IngredienteCRUD.leer_ingredientes(db)
        nuevos_valores = [ingrediente.nombre for ingrediente in ingredientes]
        db.close()

        # Verificar si los valores han cambiado para evitar actualizaciones innecesarias
        if self.combobox_ingredientes["values"] != tuple(nuevos_valores):
            self.combobox_ingredientes["values"] = nuevos_valores

        # Llamar a este método nuevamente después de 1000 ms (1 segundo)
        self.after(1000, self.actualizar_combobox_ingredientes)

    def cargar_menus(self):
        db = next(get_session())
        self.treeview_menus.delete(*self.treeview_menus.get_children())
        menus = MenuCRUD.leer_menus(db)
        for menu in menus:
            self.treeview_menus.insert("", "end", values=(menu.nombre, menu.descripcion))
        db.close()

    def crear_menu(self):
        db = next(get_session())
        # Obtener el nombre, la descripción del menú y el precio
        nombre_menu = self.entry_menu_nombre.get()
        descripcion_menu = self.entry_menu_descripcion.get()
        precio = float(self.entry_precio.get())

        if not nombre_menu or not descripcion_menu:
            # Mostrar un mensaje de error si falta el nombre o la descripción
            messagebox.showerror("Error", "El nombre y la descripción son obligatorios.")
            return

        # Crear un objeto Menu
        nuevo_menu = Menu(nombre=nombre_menu, descripcion=descripcion_menu, precio=precio)

        # Obtener los ingredientes del Treeview
        ingredientes_seleccionados = []
        for item in self.treeview_menu_ingredientes2.get_children():
            nombre_ingrediente = self.treeview_menu_ingredientes2.item(item, "values")[0]
            cantidad_ingrediente = self.treeview_menu_ingredientes2.item(item, "values")[1]
        
            # Buscar el ingrediente en la base de datos
        ingrediente = db.query(Ingrediente).filter_by(nombre=nombre_ingrediente).first()

        if ingrediente:
            # Asignar la cantidad del ingrediente
            ingrediente_menu = {"ingrediente": ingrediente, "cantidad": cantidad_ingrediente}
            ingredientes_seleccionados.append(ingrediente_menu)

        # Asociar los ingredientes al nuevo menú
        for ingrediente in ingredientes_seleccionados:
            ingrediente_obj = ingrediente["ingrediente"]
            # Aquí debes agregar la lógica para asociar la cantidad con el ingrediente (si es necesario).
            # Podrías usar una tabla intermedia para almacenar la relación entre menú e ingrediente junto con la cantidad
            nuevo_menu.ingredientes.append(ingrediente_obj)

                # Guardar el menú en la base de datos
        db.add(nuevo_menu)
        db.commit()

        # Confirmar la creación
        messagebox.showinfo("Éxito", f"Menú '{nombre_menu}' creado con éxito.")
    
        # Limpiar los campos
        self.entry_menu_nombre.delete(0, 'end')
        self.entry_menu_descripcion.delete(0, 'end')
        self.treeview_menu_ingredientes2.delete(*self.treeview_menu_ingredientes2.get_children())


    def eliminar_menu(self):
        selected_item = self.treeview_menus.selection()
        if not selected_item:
            messagebox.showwarning("Selección", "Por favor, seleccione un menú.")
            return

        nombre = self.treeview_menus.item(selected_item)["values"][0]
        db = next(get_session())
        MenuCRUD.borrar_menu(db, nombre)
        db.close()

        messagebox.showinfo("Éxito", "Menú eliminado correctamente.")
        self.cargar_menus()

    def agregar_ingrediente(self):
        """Agrega el ingrediente seleccionado al menú, actualizando la base de datos."""
        ingrediente_seleccionado = self.combobox_ingredientes.get()
        cantidad_seleccionada = int(self.entry_cantidad2.get())  # Asegúrate de que la cantidad sea un número entero
        
        db = next(get_session())
        try:
            # Verificar si el ingrediente está en la base de datos
            ingrediente = Ingrediente.obtener_ingrediente_por_nombre(db, ingrediente_seleccionado)
        
            if ingrediente:
                # Verificar si la cantidad a agregar no excede la cantidad disponible
                if cantidad_seleccionada <= ingrediente.cantidad:
                    # Agregar el ingrediente al Treeview
                    for item in self.treeview_menu_ingredientes2.get_children():
                        values = self.treeview_menu_ingredientes2.item(item, "values")
                        if values[0] == ingrediente_seleccionado:  # Ingrediente ya existe en el Treeview
                            nueva_cantidad = int(values[1]) + cantidad_seleccionada
                            self.treeview_menu_ingredientes2.item(item, values=(ingrediente_seleccionado, nueva_cantidad))
                            
                            # Actualizar la cantidad en la lista temporal
                            for ing in self.ingredientes_menu:
                                if ing["nombre"] == ingrediente_seleccionado:
                                    ing["cantidad"] = nueva_cantidad
                            break
                    else:
                        # Nuevo ingrediente en el Treeview
                        self.treeview_menu_ingredientes2.insert("", "end", values=(ingrediente_seleccionado, cantidad_seleccionada))
                        self.ingredientes_menu.append({"nombre": ingrediente_seleccionado, "cantidad": cantidad_seleccionada})
                    
                    # Actualizar la cantidad del ingrediente en la base de datos
                    nueva_cantidad_db = ingrediente.cantidad - cantidad_seleccionada
                    Ingrediente.actualizar_cantidad_ingrediente(db, ingrediente_seleccionado, nueva_cantidad_db)
                else:
                    print(f"No hay suficiente cantidad del ingrediente {ingrediente_seleccionado}.")
            else:
                print(f"El ingrediente {ingrediente_seleccionado} no existe en la base de datos.")
        finally:
            db.close()

    def quitar_ingrediente(self):
        """Quita el ingrediente seleccionado del menú y actualiza la base de datos."""
        seleccion = self.treeview_menu_ingredientes2.selection()
        if seleccion:
            # Obtener los datos del ingrediente y la cantidad desde el TreeView
            item = self.treeview_menu_ingredientes2.item(seleccion)
            ingrediente_seleccionado = item["values"][0]
            cantidad_seleccionada = int(item["values"][1])

            db = next(get_session())

            try:
                # Restaurar la cantidad del ingrediente en la base de datos
                ingrediente = Ingrediente.obtener_ingrediente_por_nombre(db, ingrediente_seleccionado)
                if ingrediente:
                    nueva_cantidad = ingrediente.cantidad + cantidad_seleccionada
                    Ingrediente.actualizar_cantidad_ingrediente(db, ingrediente_seleccionado, nueva_cantidad)
                else:
                    # Si el ingrediente no está en la base de datos (por alguna inconsistencia), agregarlo
                    print(f"El ingrediente '{ingrediente_seleccionado}' no existe en la base de datos. Restaurando...")
                    Ingrediente.crear_ingrediente(
                        db,
                        nombre=ingrediente_seleccionado,
                        tipo="Desconocido",  # Sustituir según lógica de la aplicación
                        cantidad=cantidad_seleccionada,
                        unidad="unidad"     # Sustituir según lógica de la aplicación
                    )

                # Eliminar el ingrediente del TreeView
                self.treeview_menu_ingredientes2.delete(seleccion)

                # También eliminarlo de la lista temporal de ingredientes
                self.ingredientes_menu = [
                    ing for ing in self.ingredientes_menu
                    if ing["nombre"] != ingrediente_seleccionado or ing["cantidad"] != cantidad_seleccionada
                ]

                print(f"El ingrediente '{ingrediente_seleccionado}' ha sido eliminado del menú y restaurado en la base de datos.")
            
            except Exception as e:
                db.rollback()
                print(f"Ocurrió un error al quitar el ingrediente: {e}")
            
            finally:
                db.close()
        else:
            print("Por favor, seleccione un ingrediente para eliminar.")


    def crear_menu(self):
        """Crea un objeto Menu con su nombre, descripción, lista de ingredientes y precio , y limpia el TreeView."""
        nombre_menu = self.entry_menu_nombre.get().strip()
        descripcion_menu = self.entry_menu_descripcion.get().strip()
        precio_menu = float(self.entry_precio.get())
        
        if not nombre_menu:
            print("El nombre del menú no puede estar vacío.")
            return

        db = next(get_session())

        try:
            # Verificar si el menú ya existe
            menu_existente = db.query(Menu).filter_by(nombre=nombre_menu).first()
            if menu_existente:
                print(f"El menú '{nombre_menu}' ya existe en la base de datos.")
                return

            # Crear el objeto Menu
            nuevo_menu = Menu(nombre=nombre_menu, descripcion=descripcion_menu, precio=precio_menu)

            # Usar los ingredientes almacenados en la lista temporal
            for ingrediente_data in self.ingredientes_menu:
                ingrediente_nombre = ingrediente_data["nombre"]
                cantidad = ingrediente_data["cantidad"]

                # Crear la relación MenuIngrediente
                menu_ingrediente = MenuIngrediente(
                    menu_nombre=nombre_menu,
                    ingrediente_nombre=ingrediente_nombre,
                    cantidad=cantidad
                )
                nuevo_menu.menu_ingredientes.append(menu_ingrediente)

            # Agregar el nuevo menú a la base de datos
            db.add(nuevo_menu)
            db.commit()
            print(f"El menú '{nombre_menu}' se ha creado correctamente.")

        except Exception as e:
            db.rollback()
            print(f"Ocurrió un error al crear el menú: {e}")
        finally:
            db.close()

        # Limpiar la lista de ingredientes temporal después de crear el menú
        self.ingredientes_menu.clear()

        # Limpiar el TreeView
        self.treeview_menu_ingredientes2.delete(*self.treeview_menu_ingredientes2.get_children())

        # Limpiar los campos del formulario
        self.entry_menu_nombre.delete(0, 'end')
        self.entry_menu_descripcion.delete(0, 'end')



if __name__ == "__main__":
    app = App()
    app.mainloop()