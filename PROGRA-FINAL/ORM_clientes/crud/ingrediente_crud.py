from sqlalchemy.orm import Session
from models import Ingrediente

class IngredienteCRUD:
    @staticmethod
    def crear_ingrediente(db: Session, nombre: str, tipo: str, cantidad: int, unidad: str):
        ingrediente_existente = db.query(Ingrediente).filter_by(nombre=nombre).first()
        if ingrediente_existente:
            print(f"El ingrediente '{nombre}' ya existe")
            return ingrediente_existente

        ingrediente = Ingrediente(nombre=nombre, tipo=tipo, cantidad=cantidad, unidad=unidad)
        db.add(ingrediente)
        db.commit()
        db.refresh(ingrediente)
        return ingrediente

    @staticmethod
    def leer_ingredientes(db: Session):
        return db.query(Ingrediente).all()

    @staticmethod
    def actualizar_ingrediente(db: Session, nombre_actual: str, nuevo_nombre: str, nuevo_tipo: str, nuevo_cantidad: int, nuevo_unidad: str):
        ingrediente = db.query(Ingrediente).filter_by(nombre=nombre_actual).first()
        if not ingrediente:
            print(f"No se encontró el ingrediente con el nombre: {nombre_actual}.")
            return None

        # Si el nuevo nombre es diferente al actual y no está vacío, crear un nuevo ingrediente
        if nuevo_nombre and nuevo_nombre != nombre_actual:
            nuevo_ingrediente = Ingrediente(nombre=nuevo_nombre, tipo=nuevo_tipo, cantidad=nuevo_cantidad, unidad=nuevo_unidad)
            db.add(nuevo_ingrediente)
            db.commit()

            db.delete(ingrediente)
            db.commit()

            return nuevo_ingrediente
        else:
            # Actualizar los datos del ingrediente actual
            ingrediente.tipo = nuevo_tipo
            ingrediente.cantidad = nuevo_cantidad
            ingrediente.unidad = nuevo_unidad
            db.commit()
            db.refresh(ingrediente)
            return ingrediente
        
    @staticmethod
    def borrar_ingrediente(db: Session, nombre: str):
        ingrediente = db.query(Ingrediente).filter_by(nombre=nombre).first()
        if ingrediente:
            db.delete(ingrediente)
            db.commit()
            return ingrediente
        return None
