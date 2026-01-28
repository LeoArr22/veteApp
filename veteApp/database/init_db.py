# database/init_db.py
from database.connection import engine
from database.models import Base 
# Al importar Base de models.py, ya se cargan todas tus clases (Paciente, Consulta, etc.)

def init_db():
    """Crea las tablas físicamente en el archivo .db"""
    # create_all busca todo lo que heredó de Base y genera el SQL
    Base.metadata.create_all(bind=engine)
    print("✅ Base de datos e infraestructura de tablas inicializada correctamente.")

if __name__ == "__main__":
    init_db()