from sqlalchemy import Table, Column, Integer, ForeignKey, String, Float, Date
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy.orm import Session
from datetime import datetime

class MenuIngrediente(Base):
    __tablename__ = "menu_ingrediente"
    menu_nombre = Column(String, ForeignKey("menus.nombre"), primary_key=True)
    ingrediente_nombre = Column(String, ForeignKey("ingredientes.nombre"), primary_key=True)
    cantidad = Column(Integer, nullable=False)  # Cantidad de ingrediente

    # Relación inversa para facilitar acceso
    menu = relationship("Menu", back_populates="menu_ingredientes")
    ingrediente = relationship("Ingrediente", back_populates="ingrediente_menus")


class Menu(Base):
    __tablename__ = "menus"
    nombre = Column(String, primary_key=True, nullable=False, unique=True)
    descripcion = Column(String, nullable=True)
    precio = Column(Float, nullable=False)

    # Relación con la tabla intermedia
    menu_ingredientes = relationship("MenuIngrediente", back_populates="menu")

class Ingrediente(Base):
    __tablename__ = "ingredientes"
    nombre = Column(String, primary_key=True, nullable=False, unique=True)
    tipo = Column(String, nullable=True)
    cantidad = Column(Integer, nullable=False)
    unidad = Column(String, nullable=True)

    # Relación con la tabla intermedia
    ingrediente_menus = relationship("MenuIngrediente", back_populates="ingrediente")

    @classmethod
    def obtener_ingrediente_por_nombre(cls, db: Session, nombre: str):
        return db.query(cls).filter(cls.nombre == nombre).first()

    @classmethod
    def actualizar_cantidad_ingrediente(cls, db: Session, nombre: str, nueva_cantidad: int):
        ingrediente = db.query(cls).filter(cls.nombre == nombre).first()
        if ingrediente:
            ingrediente.cantidad = nueva_cantidad
            db.commit()
            db.refresh(ingrediente)
        return ingrediente
    
class Cliente(Base):
    __tablename__ = 'clientes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    edad = Column(Integer, nullable=False)

    pedidos = relationship("Pedido", back_populates="cliente", cascade="all, delete-orphan")

class Pedido(Base):
    __tablename__ = 'pedidos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    descripcion = Column(String(255), nullable=False)
    total = Column(Float, nullable=False)
    fecha_creacion = Column(Date, default=datetime.now())
    cantidad_menus = Column(Integer, nullable=False)

    # Relación con el cliente
    cliente_id = Column(Integer, ForeignKey('clientes.id'), nullable=False)
    cliente = relationship("Cliente", back_populates="pedidos")

    
