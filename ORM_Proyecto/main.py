import customtkinter as ctk
from interfaz_app import InterfazApp
from logica_app import LogicaApp
from database import Base, engine

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gestión de Clientes, Pedidos y Menús")
        self.geometry("1450x600")

        # Instanciar lógica y GUI
        self.logica = LogicaApp()
        self.interfaz = InterfazApp(self)

        # Crear pestañas
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(pady=20, padx=20, fill="both", expand=True)

        # Crear formularios en las pestañas
        self.tab_ingredientes = self.tabview.add("Ingredientes")
        self.interfaz.crear_formulario_ingrediente(self.tab_ingredientes)

        self.tab_menu = self.tabview.add("Menús")
        self.interfaz.crear_formulario_menu(self.tab_menu)

        self.tab_clientes = self.tabview.add("Clientes")
        self.interfaz.crear_formulario_cliente(self.tab_clientes)

        self.tab_pedidos = self.tabview.add("Panel de Compra")
        self.interfaz.crear_formulario_panel_de_compra(self.tab_pedidos)

        self.tab_pedidos = self.tabview.add("Pedidos")
        self.interfaz.crear_formulario_pedido(self.tab_pedidos)

        self.tab_graficos = self.tabview.add("Graficos")
        self.interfaz.crear_formulario_grafico(self.tab_graficos)

        self.tab_estado = self.tabview.add("Estados Pedido")
        self.interfaz.crear_panel_estado_pedido(self.tab_estado)



        #self.tab_graficos = self.tabview.add("Gráficos")
        #self.interfaz.crear_formulario_grafico(self.tab_graficos)

    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    app = App()
    app.mainloop()