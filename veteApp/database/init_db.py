# database/init_db.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base  # solo Base, limpio
from database import models       # importa models y registra todas las tablas

# ---------------------------
# CONFIGURACIÓN DE LA BASE
# ---------------------------

DB_NAME = "vete.db"

# Engine de SQLite
engine = create_engine(
    f"sqlite:///{DB_NAME}",
    echo=False,           # Cambialo a True si querés ver el SQL en consola
    future=True
)

# Sesión
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

# ---------------------------
# FUNCIÓN PARA CREAR LA BASE
# ---------------------------

def init_db():
    """Crea todas las tablas definidas en los modelos."""
    Base.metadata.create_all(bind=engine)
    print("Base de datos inicializada correctamente.")
