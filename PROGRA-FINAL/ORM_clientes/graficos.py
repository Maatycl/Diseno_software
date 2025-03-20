import matplotlib.pyplot as plt
from sqlalchemy import func
from database import get_session
from models import Pedido, Menu, Ingrediente
from datetime import datetime, timedelta
from collections import defaultdict
import re

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