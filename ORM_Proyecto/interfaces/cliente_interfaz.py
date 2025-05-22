import customtkinter as ctk
from tkinter import messagebox, ttk
from PIL import Image
from customtkinter import CTkImage
from logicas.cliente_logica import LogicaCliente

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class ClienteApp(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Tienda de Menús - Cliente")
        self.geometry("900x700")

        ctk.CTkLabel(self, text="Email del Cliente").pack(pady=5)
        self.entry_email = ctk.CTkEntry(self)
        self.entry_email.pack(pady=5)

        self.menu_frame = ctk.CTkScrollableFrame(self, label_text="Menús Disponibles")
        self.menu_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.carrito_frame = ctk.CTkFrame(self)
        self.carrito_frame.pack(pady=10, padx=20, fill="x")
        ctk.CTkLabel(self.carrito_frame, text="Carrito de Compras").pack()

        self.tree_carrito = ttk.Treeview(self.carrito_frame, columns=("Menú", "Cantidad", "Precio Total"), show="headings")
        self.tree_carrito.heading("Menú", text="Menú")
        self.tree_carrito.heading("Cantidad", text="Cantidad")
        self.tree_carrito.heading("Precio Total", text="Precio Total")
        self.tree_carrito.pack(fill="x")

        ctk.CTkButton(self, text="Finalizar Compra", command=self.finalizar_compra).pack(pady=10)
        ctk.CTkButton(self, text="Registrarse", command=self.ventana_registro).pack(pady=5)

        self.menus_dict = {}
        self.carrito = []
        self.cargar_menus()

    def cargar_menus(self):
        menus = LogicaCliente.obtener_menus()  # Obtener menús desde la lógica
        for widget in self.menu_frame.winfo_children():
            widget.destroy()

        for menu in menus:
            frame = ctk.CTkFrame(self.menu_frame)
            frame.pack(pady=10, padx=10, fill="x")

            ctk.CTkLabel(frame, text=menu.nombre, font=("Arial", 14, "bold")).pack(anchor="w")
            try:
                # Cargar la imagen desde la ruta almacenada en el menú
                if menu.ruta_imagen:
                    img = CTkImage(light_image=Image.open(menu.ruta_imagen), size=(80, 80))
                    label_img = ctk.CTkLabel(frame, image=img, text="")
                    label_img.image = img
                    label_img.pack(anchor="w")
                else:
                    print(f"El menú '{menu.nombre}' no tiene una ruta de imagen asociada.")
            except Exception as e:
                print(f"No se pudo cargar la imagen para el menú '{menu.nombre}': {e}")

            ctk.CTkLabel(frame, text=menu.descripcion).pack(anchor="w")
            ctk.CTkLabel(frame, text=f"Precio: {menu.precio:.2f} CLP").pack(anchor="w")
            entry_cant = ctk.CTkEntry(frame, placeholder_text="Cantidad")
            entry_cant.pack(side="left", padx=5, pady=5)
            ctk.CTkButton(frame, text="Agregar al Carrito", command=lambda m=menu, c=entry_cant: self.agregar_carrito(m, c)).pack(side="right", padx=5, pady=5)
            self.menus_dict[menu.nombre] = menu

    def agregar_carrito(self, menu, cantidad_entry):
        try:
            cantidad = int(cantidad_entry.get())
            self.carrito, total = LogicaCliente.agregar_a_carrito(self.carrito, menu, cantidad)
            self.tree_carrito.insert("", "end", values=(menu.nombre, cantidad, f"{total:.2f}"))
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número entero.")

    def finalizar_compra(self):
        email = self.entry_email.get().strip()
        if not email:
            messagebox.showerror("Error", "Debe ingresar el email del cliente.")
            return
        if not self.carrito:
            messagebox.showerror("Error", "El carrito está vacío.")
            return

        cliente, resultado = LogicaCliente.realizar_pedido(email, self.carrito)
        if cliente:
            messagebox.showinfo("Éxito", "Pedidos realizados y boleta generada.")
            self.tree_carrito.delete(*self.tree_carrito.get_children())
            self.carrito.clear()
        else:
            messagebox.showerror("Error", resultado)

    def ventana_registro(self):
        ventana = ctk.CTkToplevel(self)
        ventana.title("Registro de Cliente")
        ventana.geometry("400x300")

        ctk.CTkLabel(ventana, text="Nombre").pack(pady=5)
        entry_nombre = ctk.CTkEntry(ventana)
        entry_nombre.pack(pady=5)

        ctk.CTkLabel(ventana, text="Email").pack(pady=5)
        entry_email = ctk.CTkEntry(ventana)
        entry_email.pack(pady=5)

        ctk.CTkLabel(ventana, text="Edad").pack(pady=5)
        entry_edad = ctk.CTkEntry(ventana)
        entry_edad.pack(pady=5)

        def guardar_cliente():
            nombre = entry_nombre.get().strip()
            email = entry_email.get().strip()
            edad = entry_edad.get().strip()
            if not nombre or not email or not edad:
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return
            try:
                edad = int(edad)
            except ValueError:
                messagebox.showerror("Error", "Edad inválida.")
                return

            cliente = LogicaCliente.registrar_cliente(nombre, email, edad)
            if cliente:
                messagebox.showinfo("Éxito", "Cliente registrado.")
                ventana.destroy()
            else:
                messagebox.showerror("Error", "El cliente ya existe.")

        ctk.CTkButton(ventana, text="Guardar", command=guardar_cliente).pack(pady=10)