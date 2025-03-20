import time
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from models import Pedido, Cliente

class PedidoCRUD:
    @staticmethod
    def _try_commit(db: Session, max_retries=3, delay=0.5):
        """Intentar hacer commit con reintentos en caso de errores de bloqueo."""
        retries = 0
        while retries < max_retries:
            try:
                db.commit()
                return True
            except OperationalError as e:
                if "database is locked" in str(e):
                    db.rollback()
                    print(f"Intento {retries+1}/{max_retries}: la base de datos está bloqueada, reintentando en {delay} segundos...")
                    time.sleep(delay)
                    retries += 1
                else:
                    print(f"Error de base de datos: {e}")
                    db.rollback()
                    return False
            except SQLAlchemyError as e:
                print(f"Error al hacer commit: {e}")
                db.rollback()
                return False
        print("Error: no se pudo hacer commit después de varios intentos.")
        return False

    @staticmethod
    def crear_pedido(db: Session, cliente_id: int, descripcion: str):
        cliente = db.query(Cliente).get(cliente_id)
        if cliente:
            pedido = Pedido(descripcion=descripcion, cliente=cliente)
            db.add(pedido)
            if not PedidoCRUD._try_commit(db):
                return None
            db.refresh(pedido)
            return pedido
        print(f"No se encontró el cliente con ID '{cliente_id}'.")
        return None

    @staticmethod
    def leer_pedidos(db: Session):
        return db.query(Pedido).all()

    @staticmethod
    def actualizar_pedido(db: Session, pedido_id: int, nueva_descripcion: str):
        pedido = db.query(Pedido).get(pedido_id)
        if pedido:
            pedido.descripcion = nueva_descripcion
            if not PedidoCRUD._try_commit(db):
                return None
            db.refresh(pedido)
            return pedido
        print(f"No se encontró el pedido con ID '{pedido_id}'.")
        return None

    @staticmethod
    def borrar_pedido(db: Session, pedido_id: int):
        pedido = db.query(Pedido).get(pedido_id)
        if pedido:
            db.delete(pedido)
            if not PedidoCRUD._try_commit(db):
                return None
            return pedido
        print(f"No se encontró el pedido con ID '{pedido_id}'.")
        return None
    
    @staticmethod
    def leer_pedidos_por_cliente(db, cliente_email):
        """Obtiene los pedidos asociados a un cliente específico por su email"""
        # Obtener el cliente por email
        cliente = db.query(Cliente).filter(Cliente.email == cliente_email).first()

        if cliente:
            # Filtrar pedidos por el id del cliente
            return db.query(Pedido).filter(Pedido.cliente_id == cliente.id).all()
        
        # Si no se encuentra el cliente, retornar una lista vacía
        # Puede ser útil registrar un mensaje de log aquí si necesitas seguimiento
        print(f"No se encontró el cliente con email: {cliente_email}")
        return []



    @staticmethod
    def leer_pedidos_por_cliente(db, cliente_email, page=1, page_size=10):
        """Obtiene los pedidos asociados a un cliente específico por su email, con soporte de paginación"""
        cliente = db.query(Cliente).filter(Cliente.email == cliente_email).first()

        if cliente:
            return db.query(Pedido).filter(Pedido.cliente_id == cliente.id).limit(page_size).offset((page - 1) * page_size).all()
        
        print(f"No se encontró el cliente con email: {cliente_email}")
        return []

