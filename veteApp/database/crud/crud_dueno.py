# database/crud/dueno.py

from sqlalchemy.orm import Session
from database.models import Dueno


# ---------------------------------------------------------
# CREAR DUEÑO
# ---------------------------------------------------------
def crear_dueno(
    db: Session,
    dni: str,
    nombre: str,
    telefono: str | None = None,
    email: str | None = None,
    direccion: str | None = None
) -> Dueno:
    """
    Crea un nuevo dueño.
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
# OBTENER DUEÑO POR ID
# ---------------------------------------------------------
def obtener_dueno_por_id(
    db: Session,
    dueno_id: int
) -> Dueno | None: # -> Dueno | None indica el tipo de retorno esperado (Type Hint)
    """
    Devuelve un dueño por ID o None si no existe.
    """

    return (
        db.query(Dueno)
        .filter(
            Dueno.id == dueno_id,
            Dueno.activo.is_(True)
        )
        .one_or_none()
    )


# ---------------------------------------------------------
# OBTENER DUEÑO POR DNI
# ---------------------------------------------------------
def obtener_dueno_por_dni(
    db: Session,
    dni: str
) -> Dueno | None:
    """
    Devuelve un dueño activo por DNI o None si no existe.
    """

    return (
        db.query(Dueno)
        .filter(
            Dueno.dni == dni,
            Dueno.activo.is_(True)
        )
        .one_or_none()
    )


# ---------------------------------------------------------
# LISTAR DUEÑOS ACTIVOS
# ---------------------------------------------------------
def listar_duenos(
    db: Session
) -> list[Dueno]: # -> list[Dueno] indica el tipo de retorno esperado (Type Hint)
    """
    Devuelve todos los dueños activos ordenados por nombre.
    """

    return (
        db.query(Dueno)
        .filter(Dueno.activo.is_(True))
        .order_by(Dueno.nombre)
        .all()
    )


# ---------------------------------------------------------
# ACTUALIZAR DUEÑO
# ---------------------------------------------------------
def actualizar_dueno(
    db: Session,
    dueno: Dueno,
    *, # * → a partir de aca los parámetros son keyword-only
    nombre: str | None = None,
    telefono: str | None = None,
    email: str | None = None,
    direccion: str | None = None
) -> Dueno:  # -> Dueno indica el tipo de retorno esperado (Type Hint)

    """
    Actualiza los datos de un dueño existente.
    Recibe la entidad ya cargada.
    """

    if nombre is not None:
        dueno.nombre = nombre
    if telefono is not None:
        dueno.telefono = telefono
    if email is not None:
        dueno.email = email
    if direccion is not None:
        dueno.direccion = direccion

    return dueno



# ---------------------------------------------------------
# ACTUALIZAR DNI DE DUEÑO (CASO ESPECIAL)
# ---------------------------------------------------------
def actualizar_dni_dueno(
    db: Session,
    dueno: Dueno,
    *,
    nuevo_dni: str
) -> Dueno:
    """
    Corrige el DNI de un dueño.
    Caso de uso excepcional.
    """

    dueno.dni = nuevo_dni
    return dueno

# ---------------------------------------------------------
# SOFT DELETE DE DUEÑO
# ---------------------------------------------------------
def desactivar_dueno(
    db: Session,
    dueno: Dueno
) -> None: # -> None indica el tipo de retorno esperado (Type Hint)
    """
    Marca un dueño como inactivo (soft delete).
    """

    dueno.activo = False
