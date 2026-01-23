# database/init_db.py

from database.connection import engine
from database.models import Base

def init_db():
    """Crea las tablas físicamente en el archivo .db"""
  
    from database import models
    
    Base.metadata.create_all(bind=engine)
    print("Base de datos e infraestructura de tablas inicializada.")

if __name__ == "__main__":
    init_db()