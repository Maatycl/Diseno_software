from sqlalchemy.orm import Session
from models import Cliente

class ClienteCRUD:
    @staticmethod

    def crear_cliente(db: Session, nombre: str, email: str, edad: int):
        cliente_existente = db.query(Cliente).filter_by(email=email).first()
        if cliente_existente:
            print(f"El cliente con correo '{email}' ya existe.")
            return None

        cliente = Cliente(nombre=nombre, email=email, edad=edad)
        db.add(cliente)
        db.commit()
        db.refresh(cliente)
        print(f"Cliente '{nombre}' agregado exitosamente.")
        return cliente

    @staticmethod
    def leer_clientes(db: Session):
        return db.query(Cliente).all()
    
    @staticmethod
    def leer_cliente_por_email(db: Session, email: str):
        return db.query(Cliente).filter(Cliente.email == email).first()

    @staticmethod
    def actualizar_cliente(db: Session, cliente_email: str, nuevo_nombre: str = None, nuevo_correo: str = None, edad: int = None):
        # Buscar al cliente por el correo electrónico
        cliente = db.query(Cliente).filter_by(email=cliente_email).first()
        if not cliente:
            print(f"Cliente con correo '{cliente_email}' no encontrado.")
            return None

        # Actualizar nombre si se proporciona
        if nuevo_nombre:
            cliente.nombre = nuevo_nombre

        # Actualizar correo si se proporciona y no está en uso por otro cliente
        if nuevo_correo:
            cliente_existente = db.query(Cliente).filter_by(email=nuevo_correo).first()
            if cliente_existente and cliente_existente.email != cliente_email:
                print(f"El correo '{nuevo_correo}' ya está en uso por otro cliente.")
                return None
            cliente.email = nuevo_correo

        # Actualizar edad si se proporciona
        if edad is not None:
            cliente.edad = edad

        # Confirmar cambios en la base de datos
        try:
            db.commit()
            db.refresh(cliente)
            print(f"Cliente con correo '{cliente_email}' actualizado exitosamente.")
            return cliente
        except Exception as e:
            db.rollback()
            print(f"Error al actualizar cliente: {e}")
            return None

    @staticmethod
    def eliminar_cliente(db: Session, cliente_email: str):
        cliente = db.query(Cliente).filter_by(email=cliente_email).first()
        if not cliente:
            print(f"Cliente con email '{cliente_email}' no encontrado.")
            return None
        # Si se encuentra el cliente, se puede proceder a eliminarlo
        db.delete(cliente)
        db.commit()
        print(f"Cliente con email '{cliente_email}' ha sido eliminado.")
        return cliente