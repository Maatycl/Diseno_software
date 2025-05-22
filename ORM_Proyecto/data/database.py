# Configuración de la base de datos y sesión
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Configuración del motor y la sesión
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "mi_base_de_datos.db")  
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarativa
Base = declarative_base()  # Definimos Base aquí

# Función para obtener la sesión de base de datos
def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
