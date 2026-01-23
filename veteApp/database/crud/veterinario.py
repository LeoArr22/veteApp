# database/crud/veterinario.py

from sqlalchemy.orm import Session
from database.models import Veterinario

# ---------------------------------------------------------
# CREAR VETERINARIO
# ---------------------------------------------------------
def crear_veterinario(
    db: Session,
    *,
    nombre: str,
    matricula: str,
    especialidad: str | None = None,
    telefono: str | None = None
) -> Veterinario:
    """
    Registra un nuevo profesional en la base de datos.
    El uso de '*' obliga a pasar los argumentos por nombre.
    """
    veterinario = Veterinario(
        nombre=nombre,
        matricula=matricula,
        especialidad=especialidad,
        telefono=telefono,
        activo=True
    )
    db.add(veterinario)
    return veterinario


# ---------------------------------------------------------
# OBTENER VETERINARIO (ACTIVO)
# ---------------------------------------------------------
def obtener_veterinario_por_id(db: Session, veterinario_id: int) -> Veterinario | None:
    """
    Busca un veterinario activo por su ID.
    """
    return db.query(Veterinario).filter(
        Veterinario.id == veterinario_id, 
        Veterinario.activo.is_(True)
    ).one_or_none()


# ---------------------------------------------------------
# BUSCAR POR MATRÍCULA
# ---------------------------------------------------------
def obtener_veterinario_por_matricula(db: Session, matricula: str) -> Veterinario | None:
    """
    Busca un veterinario por su matrícula profesional.
    """
    return db.query(Veterinario).filter(Veterinario.matricula == matricula).one_or_none()


# ---------------------------------------------------------
# OBTENER VETERINARIO COMPLETO (INCLUYE INACTIVOS)
# ---------------------------------------------------------
def obtener_veterinario_completo(db: Session, veterinario_id: int) -> Veterinario | None:
    """
    Busca un veterinario por ID sin filtrar por estado (historial).
    """
    return db.query(Veterinario).filter(Veterinario.id == veterinario_id).one_or_none()


# ---------------------------------------------------------
# LISTAR VETERINARIOS
# ---------------------------------------------------------
def listar_veterinarios_activos(db: Session) -> list[Veterinario]:
    """
    Retorna la lista de profesionales que trabajan actualmente.
    """
    return db.query(Veterinario).filter(Veterinario.activo.is_(True)).all()


def listar_todos_los_veterinarios(db: Session) -> list[Veterinario]:
    """
    Retorna el padrón completo de veterinarios (activos y bajas).
    """
    return db.query(Veterinario).all()


# ---------------------------------------------------------
# PERSISTENCIA: CAMBIAR ESTADO Y ACTUALIZAR
# ---------------------------------------------------------
def cambiar_estado_veterinario(db: Session, veterinario: Veterinario, *, estado: bool):
    """
    Modifica el atributo activo del modelo.
    """
    veterinario.activo = estado


def actualizar_veterinario(db: Session, veterinario: Veterinario, **kwargs) -> Veterinario:
    """
    Actualiza los campos permitidos del profesional.
    """
    for key, value in kwargs.items():
        if value is not None:
            setattr(veterinario, key, value)
    return veterinario