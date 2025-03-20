from sqlalchemy.orm import Session
from models import Menu, MenuIngrediente, Ingrediente

class MenuCRUD:
    @staticmethod
    def crear_menu(db: Session, nombre: str, descripcion: str, precio: float, ingredientes_con_cantidades: dict):
        # Verificar si el menú ya existe
        menu_existente = db.query(Menu).filter_by(nombre=nombre).first()
        if menu_existente:
            print(f"El menú '{nombre}' ya existe.")
            return menu_existente

        # Crear el nuevo menú
        nuevo_menu = Menu(nombre=nombre, descripcion=descripcion, precio=precio)
        db.add(nuevo_menu)
        db.commit()  # Primero guardamos el menú en la base de datos

        # Agregar ingredientes al menú
        for ingrediente_nombre, cantidad in ingredientes_con_cantidades.items():
            ingrediente = db.query(Ingrediente).filter_by(nombre=ingrediente_nombre).first()
            if ingrediente:
                # Crear la relación entre el menú y el ingrediente
                menu_ingrediente = MenuIngrediente(menu_nombre=nuevo_menu.nombre, ingrediente_nombre=ingrediente.nombre, cantidad=cantidad)
                db.add(menu_ingrediente)

        db.commit()  # Guardar las relaciones de ingredientes
        db.refresh(nuevo_menu)  # Actualizar el menú después de guardar los ingredientes
        return nuevo_menu

    @staticmethod
    def leer_menus(db: Session):
        # Obtener todos los menús con sus ingredientes
        menus = db.query(Menu).all()
        for menu in menus:
            print(f"Menú: {menu.nombre} - Descripción: {menu.descripcion}")
            for menu_ingrediente in menu.menu_ingredientes:
                ingrediente = db.query(Ingrediente).filter_by(nombre=menu_ingrediente.ingrediente_nombre).first()
                print(f"- Ingrediente: {ingrediente.nombre}, Cantidad: {menu_ingrediente.cantidad}")
        return menus

    @staticmethod
    def leer_menu_por_nombre(db: Session, nombre: str):
        # Buscar un menú específico por nombre
        menu = db.query(Menu).filter_by(nombre=nombre).first()
        if menu:
            print(f"Menú: {menu.nombre} - Descripción: {menu.descripcion}")
            for menu_ingrediente in menu.menu_ingredientes:
                ingrediente = db.query(Ingrediente).filter_by(nombre=menu_ingrediente.ingrediente_nombre).first()
                print(f"- Ingrediente: {ingrediente.nombre}, Cantidad: {menu_ingrediente.cantidad}")
            return menu
        print(f"Menú con nombre '{nombre}' no encontrado.")
        return None

    @staticmethod
    def actualizar_menu(db: Session, nombre_actual: str, nuevo_nombre: str, nueva_descripcion: str, ingredientes_con_cantidades: dict):
        # Buscar el menú existente
        menu = db.query(Menu).filter_by(nombre=nombre_actual).first()
        if not menu:
            print(f"Menú con nombre '{nombre_actual}' no encontrado.")
            return None

        # Actualizar el menú
        menu.nombre = nuevo_nombre if nuevo_nombre else menu.nombre
        menu.descripcion = nueva_descripcion if nueva_descripcion else menu.descripcion

        # Eliminar ingredientes actuales asociados al menú
        db.query(MenuIngrediente).filter_by(menu_nombre=menu.nombre).delete()

        # Agregar los nuevos ingredientes
        for ingrediente_nombre, cantidad in ingredientes_con_cantidades.items():
            ingrediente = db.query(Ingrediente).filter_by(nombre=ingrediente_nombre).first()
            if ingrediente:
                menu_ingrediente = MenuIngrediente(menu_nombre=menu.nombre, ingrediente_nombre=ingrediente.nombre, cantidad=cantidad)
                db.add(menu_ingrediente)

        db.commit()  # Guardar los cambios
        db.refresh(menu)
        print(f"Menú '{nombre_actual}' actualizado exitosamente.")
        return menu

    @staticmethod
    def eliminar_menu(db: Session, nombre: str):
        # Buscar el menú
        menu = db.query(Menu).filter_by(nombre=nombre).first()
        if not menu:
            print(f"Menú con nombre '{nombre}' no encontrado.")
            return None

        # Eliminar las relaciones de ingredientes
        db.query(MenuIngrediente).filter_by(menu_nombre=menu.nombre).delete()

        # Eliminar el menú
        db.delete(menu)
        db.commit()
        print(f"Menú '{nombre}' eliminado exitosamente.")
        return menu

    