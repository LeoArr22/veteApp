# database/crud/dueno.py

from sqlalchemy.orm import Session
from database.models import Dueno

# ---------------------------------------------------------
# CREAR DUEÑO
# ---------------------------------------------------------
def crear_dueno(
    db: Session,
    *,
    dni: str,
    nombre: str,
    telefono: str | None = None,
    email: str | None = None,
    direccion: str | None = None
) -> Dueno:
    """
    Crea un nuevo dueño en estado activo.
    El uso de '*' obliga a pasar los datos como pares clave-valor.
    """
    dueno = Dueno(
        dni=dni,
        nombre=nombre,
        telefono=telefono,
        email=email,
        direccion=direccion,
        activo=True
    )
    db.add(dueno)
    return dueno


# ---------------------------------------------------------
# OBTENER DUEÑO (ACTIVO)
# ---------------------------------------------------------
def obtener_dueno_por_id(db: Session, dueno_id: int) -> Dueno | None:
    """
    Busca un dueño por ID que esté activo en el sistema.
    """
    return db.query(Dueno).filter(
        Dueno.id == dueno_id, 
        Dueno.activo.is_(True)
    ).one_or_none()


# ---------------------------------------------------------
# BUSCAR DUEÑO POR DNI
# ---------------------------------------------------------
def obtener_dueno_por_dni(db: Session, dni: str) -> Dueno | None:
    """
    Busca un dueño por su número de DNI para validaciones de unicidad.
    """
    return db.query(Dueno).filter(Dueno.dni == dni).one_or_none()


# ---------------------------------------------------------
# OBTENER DUEÑO COMPLETO (INCLUYE INACTIVOS)
# ---------------------------------------------------------
def obtener_dueno_por_id_completo(db: Session, dueno_id: int) -> Dueno | None:
    """
    Busca un dueño por ID sin filtrar por estado (historial completo).
    """
    return db.query(Dueno).filter(Dueno.id == dueno_id).one_or_none()


# ---------------------------------------------------------
# LISTAR DUEÑOS
# ---------------------------------------------------------
def listar_duenos_activos(db: Session) -> list[Dueno]:
    """
    Retorna todos los dueños con estado activo.
    """
    return db.query(Dueno).filter(Dueno.activo.is_(True)).all()


def listar_todos_los_duenos(db: Session) -> list[Dueno]:
    """
    Retorna la totalidad de dueños registrados (auditoría).
    """
    return db.query(Dueno).all()


# ---------------------------------------------------------
# PERSISTENCIA: CAMBIAR ESTADO Y ACTUALIZAR
# ---------------------------------------------------------
def cambiar_estado_dueno(db: Session, dueno: Dueno, *, estado: bool):
    """
    Modifica el atributo activo del modelo.
    """
    dueno.activo = estado


def actualizar_dueno(db: Session, dueno: Dueno, **kwargs) -> Dueno:
    """
    Aplica cambios parciales a un registro de dueño mediante keywords.
    """
    for key, value in kwargs.items():
        if value is not None:
            setattr(dueno, key, value)
    return dueno