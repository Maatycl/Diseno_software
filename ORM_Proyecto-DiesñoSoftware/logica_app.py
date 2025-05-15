from database import get_session
from crud.ingrediente_crud import IngredienteCRUD
from crud.menu_crud import MenuCRUD
from crud.cliente_crud import ClienteCRUD
from crud.pedido_crud import PedidoCRUD
from models import Menu, Ingrediente, Pedido
import matplotlib.pyplot as plt
from sqlalchemy import func
from datetime import datetime, timedelta
from collections import defaultdict
import re

class LogicaApp:

    @staticmethod
    def cargar_ingredientes():
        """Obtiene los ingredientes desde la base de datos."""
        db = next(get_session())
        ingredientes = IngredienteCRUD.leer_ingredientes(db)
        db.close()
        return ingredientes

    @staticmethod
    def crear_ingrediente(nombre, tipo, cantidad, unidad):
        """Crea un nuevo ingrediente en la base de datos."""
        db = next(get_session())
        IngredienteCRUD.crear_ingrediente(db, nombre, tipo, cantidad, unidad)
        db.close()

    @staticmethod
    def actualizar_ingrediente(nombre, tipo, cantidad, unidad):
        """Actualiza un ingrediente existente en la base de datos."""
        db = next(get_session())
        IngredienteCRUD.actualizar_ingrediente(db, nombre, tipo, cantidad, unidad)
        db.close()

    @staticmethod
    def eliminar_ingrediente(nombre):
        """Elimina un ingrediente de la base de datos."""
        db = next(get_session())
        IngredienteCRUD.borrar_ingrediente(db, nombre)
        db.close()
    
    #Menus
    @staticmethod
    def crear_menu(nombre: str, descripcion: str, precio: float, ingredientes_lista: list[dict], ruta_imagen: str):
        """Crea un menú en la base de datos, incluyendo la ruta de la imagen."""
        db = next(get_session())

        try:
            # Convertir lista de ingredientes a dict para el CRUD
            ingredientes_dict = {
                item["nombre"]: item["cantidad"] for item in ingredientes_lista
            }

            # Crear el menú en la base de datos
            nuevo_menu = Menu(
                nombre=nombre,
                descripcion=descripcion,
                precio=precio,
                ruta_imagen=ruta_imagen  # Asociar la ruta de la imagen
            )
            db.add(nuevo_menu)

            # Guardar los ingredientes asociados al menú
            for nombre_ingrediente, cantidad in ingredientes_dict.items():
                # Buscar el ingrediente directamente en la base de datos
                ingrediente = db.query(Ingrediente).filter(Ingrediente.nombre == nombre_ingrediente).first()
                if ingrediente:
                    # Actualizar la cantidad del ingrediente si ya existe
                    nueva_cantidad = ingrediente.cantidad - cantidad
                    if nueva_cantidad < 0:
                        raise ValueError(f"No hay suficiente cantidad del ingrediente '{nombre_ingrediente}'.")
                    ingrediente.cantidad = nueva_cantidad
                    db.commit()
                else:
                    # Si el ingrediente no existe, crearlo
                    IngredienteCRUD.crear_ingrediente(db, nombre_ingrediente, "Desconocido", cantidad, "unidad")

            db.commit()
            print(f"Menú '{nombre}' creado exitosamente.")
        except Exception as e:
            print(f"Error al crear el menú: {e}")
            db.rollback()
        finally:
            db.close()

    @staticmethod
    def obtener_nombres_ingredientes():
        """Retorna una lista con los nombres de todos los ingredientes."""
        db = next(get_session())
        ingredientes = IngredienteCRUD.leer_ingredientes(db)
        db.close()
        return [ingrediente.nombre for ingrediente in ingredientes]
    
    @staticmethod
    def obtener_ingrediente_por_nombre(nombre: str):
        """Retorna un objeto Ingrediente por su nombre."""
        db = next(get_session())
        ingrediente = Ingrediente.obtener_ingrediente_por_nombre(db, nombre)
        db.close()
        return ingrediente


    @staticmethod
    def descontar_cantidad_ingrediente(nombre: str, cantidad: int):
        """Resta la cantidad de un ingrediente en la base de datos."""
        db = next(get_session())
        ingrediente = Ingrediente.obtener_ingrediente_por_nombre(db, nombre)
        if ingrediente:
            nueva_cantidad = ingrediente.cantidad - cantidad
            Ingrediente.actualizar_cantidad_ingrediente(db, nombre, nueva_cantidad)
        db.close()

    @staticmethod
    def restaurar_cantidad_ingrediente(nombre: str, cantidad: int):
        """Suma la cantidad de un ingrediente en la base de datos."""
        db = next(get_session())
        ingrediente = Ingrediente.obtener_ingrediente_por_nombre(db, nombre)
        if ingrediente:
            nueva_cantidad = ingrediente.cantidad + cantidad
            Ingrediente.actualizar_cantidad_ingrediente(db, nombre, nueva_cantidad)
        else:
            # Ingrediente no existe, lo volvemos a crear como básico
            Ingrediente.crear_ingrediente(db,nombre=nombre,tipo="Desconocido",cantidad=cantidad,unidad="unidad")
        db.close()

    #clientes
    @staticmethod
    def crear_cliente(nombre, email, edad):
        db = next(get_session())
        cliente = ClienteCRUD.crear_cliente(db, nombre, email, edad)
        db.close()
        return cliente

    @staticmethod
    def actualizar_cliente(email_actual, nuevo_nombre, nuevo_email, nueva_edad):
        db = next(get_session())
        cliente = ClienteCRUD.actualizar_cliente(db, email_actual, nuevo_nombre, nuevo_email, nueva_edad)
        db.close()
        return cliente

    @staticmethod
    def eliminar_cliente(email):
        db = next(get_session())
        ClienteCRUD.eliminar_cliente(db, email)
        db.close()

    @staticmethod
    def leer_clientes():
        db = next(get_session())
        clientes = ClienteCRUD.leer_clientes(db)
        db.close()
        return clientes
    
    #panel de compra

    @staticmethod
    def obtener_emails_clientes():
        db = next(get_session())
        clientes = ClienteCRUD.leer_clientes(db)
        db.close()
        return [cliente.email for cliente in clientes]
    
    @staticmethod
    def obtener_nombres_menus():
        db = next(get_session())
        menus = MenuCRUD.leer_menus(db)
        db.close()
        return [menu.nombre for menu in menus]
    
    @staticmethod
    def obtener_cliente_y_menu(email: str, menu_nombre: str):
        db = next(get_session())
        cliente = ClienteCRUD.leer_cliente_por_email(db, email)
        menu = MenuCRUD.leer_menu_por_nombre(db, menu_nombre)
        db.close()
        return cliente, menu

    #pedidos

    @staticmethod
    def obtener_emails_clientes():
        db = next(get_session())
        clientes = ClienteCRUD.leer_clientes(db)
        db.close()
        return [cliente.email for cliente in clientes]

    @staticmethod
    def obtener_pedidos_por_cliente(email_cliente: str):
        db = next(get_session())
        pedidos = PedidoCRUD.leer_pedidos_por_cliente(db, email_cliente)
        db.close()
        return pedidos

    @staticmethod
    def graficar_ventas_por_fecha():
        """Genera un gráfico de barras para las ventas agrupadas por fecha."""
        db = next(get_session())
        try:
            # Consultar datos de ventas agrupados por fecha (últimos 30 días)
            rango_inicio = datetime.now() - timedelta(days=1)
            resultados = db.query(
                Pedido.fecha_creacion,
                func.sum(Pedido.total).label("total_vendido")
            ).filter(Pedido.fecha_creacion >= rango_inicio).group_by(Pedido.fecha_creacion).order_by(Pedido.fecha_creacion).all()

            # Validar si hay datos
            if not resultados:
                print("No hay datos de ventas disponibles para el rango seleccionado.")
                return

            # Procesar resultados
            fechas = [pedido[0].strftime('%Y-%m-%d') for pedido in resultados]
            totales = [pedido[1] for pedido in resultados]

            # Crear el gráfico
            plt.figure(figsize=(10, 6))
            plt.bar(fechas, totales, color='blue')
            plt.title("Ventas por Fecha (Últimos 30 días)")
            plt.xlabel("Fecha")
            plt.ylabel("Total Vendido")
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()
        finally:
            db.close()

    def graficar_menus_mas_comprados():
        """Genera un gráfico de torta para los menús más vendidos."""
        db = next(get_session())
        try:
            # Crear un mapeo entre nombres y descripciones de menús
            menus_map = dict(db.query(Menu.nombre, Menu.descripcion).all())
            print("Mapeo de Menús (nombre -> descripcion):", menus_map)

            # Consultar las descripciones de los menús más vendidos en los pedidos
            resultados = db.query(
                Pedido.descripcion,
                func.sum(Pedido.cantidad_menus).label("cantidad_vendida")
            ).group_by(Pedido.descripcion) \
            .order_by(func.sum(Pedido.cantidad_menus).desc()) \
            .all()
            print("Resultados de la consulta (descripcion -> cantidad_vendida):", resultados)

            # Validar resultados
            if not resultados:
                print("No hay datos disponibles para los menús más vendidos.")
                return

            # Procesar las descripciones para extraer nombres de menús
            menu_cantidades = defaultdict(int)  # Almacena las cantidades agrupadas por menú

            for descripcion, cantidad in resultados:
                # Extraer el nombre del menú usando una expresión regular
                match = re.search(r"Pedido de (\w+)", descripcion)
                if match:
                    nombre_menu = match.group(1)
                    if nombre_menu in menus_map:
                        menu_cantidades[nombre_menu] += cantidad
                    else:
                        print(f"Nombre '{nombre_menu}' no encontrado en menus_map.")
                else:
                    print(f"No se pudo extraer un nombre de menú de la descripción: {descripcion}")

            # Convertir los resultados a listas separadas para el gráfico
            nombres_menus = list(menu_cantidades.keys())
            cantidades = list(menu_cantidades.values())

            print("Nombres de menús:", nombres_menus)
            print("Cantidades vendidas:", cantidades)

            if not nombres_menus or sum(cantidades) == 0:
                print("Datos insuficientes para generar el gráfico.")
                return

            # Crear el gráfico
            plt.figure(figsize=(8, 8))
            plt.pie(cantidades, labels=nombres_menus, autopct='%1.1f%%', startangle=140)
            plt.title("Distribución de Menús Más Comprados")
            plt.show()
        finally:
            db.close()

    def graficar_uso_ingredientes():
        """Genera un gráfico de barras para los ingredientes utilizados."""
        db = next(get_session())
        try:
            # Consultar datos de uso de ingredientes
            resultados = db.query(Ingrediente.nombre, Ingrediente.cantidad).all()
            ingredientes = [resultado[0] for resultado in resultados]
            cantidades = [resultado[1] for resultado in resultados]

            # Crear el gráfico
            plt.figure(figsize=(10, 6))
            plt.bar(ingredientes, cantidades, color='green')
            plt.title("Uso de Ingredientes en Pedidos")
            plt.xlabel("Ingrediente")
            plt.ylabel("Cantidad Utilizada")
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()
        finally:
            db.close()