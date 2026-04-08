from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path

# 1. Obtenemos la ruta de la carpeta donde está este archivo (database/)
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. Definimos la ruta de la base de datos en la raíz del proyecto
DB_PATH = BASE_DIR / "vete.db"

# El motor que habla con SQLite usando la ruta absoluta
engine = create_engine(
    f"sqlite:///{DB_PATH}",
    echo=False,
    future=True,
    connect_args={"check_same_thread": False} 
)

# El generador de sesiones
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)