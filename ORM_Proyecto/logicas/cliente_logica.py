from data.database import get_session
from models.models import Pedido
from crud.cliente_crud import ClienteCRUD
from crud.menu_crud import MenuCRUD
from crud.pedido_crud import PedidoCRUD
from datetime import datetime
from utils.generar_pdf import generar_pdf_boleta

class LogicaCliente:
    @staticmethod
    def obtener_menus():
        """Obtiene los menús disponibles desde la base de datos."""
        db = next(get_session())
        menus = MenuCRUD.leer_menus(db)
        db.close()
        return menus

    @staticmethod
    def agregar_a_carrito(carrito, menu, cantidad):
        """Agrega un menú al carrito."""
        total = cantidad * menu.precio
        carrito.append({"menu": menu, "cantidad": cantidad, "total": total})
        return carrito, total

    @staticmethod
    def realizar_pedido(email, carrito):
        """Realiza un pedido para un cliente."""
        db = next(get_session())
        cliente = ClienteCRUD.leer_cliente_por_email(db, email)
        if not cliente:
            db.close()
            return None, "Cliente no registrado."

        for item in carrito:
            pedido = Pedido(
                descripcion=f"Pedido de {item['menu'].nombre} para {cliente.nombre}",
                total=item["total"],
                cantidad_menus=item["cantidad"],
                fecha_creacion=datetime.now(),
                cliente_id=cliente.id
            )
            db.add(pedido)

        if not PedidoCRUD._try_commit(db):
            db.close()
            return None, "Error al guardar el pedido."

        generar_pdf_boleta(cliente, carrito)
        db.close()
        return cliente, "Éxito"

    @staticmethod
    def registrar_cliente(nombre, email, edad):
        """Registra un nuevo cliente en la base de datos."""
        db = next(get_session())
        cliente = ClienteCRUD.crear_cliente(db, nombre, email, edad)
        db.close()
        return cliente
