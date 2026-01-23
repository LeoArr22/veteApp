# database/connection.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_NAME = "vete.db"

# El motor que habla con SQLite
engine = create_engine(
    f"sqlite:///{DB_NAME}",
    echo=False,  # Ponelo en True para debugear SQL
    future=True,
    connect_args={"check_same_thread": False} # Necesario para Apps de escritorio (GUI)
)

# El generador de sesiones
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)