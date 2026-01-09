# database/crud/paciente.py

from sqlalchemy.orm import Session
from database.models import Paciente

# -> dato
# indica el tipo de retorno esperado (Type Hint)

# ---------------------------------------------------------
# CREAR PACIENTE (MASCOTA)
# ---------------------------------------------------------
def crear_paciente(
    db: Session,
    *,
    nombre: str,
    especie: str,
    dueno_id: int,
    raza: str | None = None,
    sexo: str | None = None,
    fecha_nacimiento=None
) -> Paciente:
    """
    Crea una nueva mascota (paciente).
    """

    paciente = Paciente(
        nombre=nombre,
        especie=especie,
        raza=raza,
        sexo=sexo,
        fecha_nacimiento=fecha_nacimiento,
        dueno_id=dueno_id,
        activo=True
    )

    db.add(paciente)
    return paciente


# ---------------------------------------------------------
# OBTENER PACIENTE POR ID
# ---------------------------------------------------------
def obtener_paciente_por_id(
    db: Session,
    paciente_id: int
) -> Paciente | None:
    """
    Devuelve un paciente activo por ID o None si no existe.
    """

    return (
        db.query(Paciente)
        .filter(
            Paciente.id == paciente_id,
            Paciente.activo.is_(True)
        )
        .one_or_none()
    )


# ---------------------------------------------------------
# LISTAR PACIENTES ACTIVOS
# ---------------------------------------------------------
def listar_pacientes(
    db: Session
) -> list[Paciente]:
    """
    Devuelve todos los pacientes activos ordenados por nombre.
    """

    return (
        db.query(Paciente)
        .filter(Paciente.activo.is_(True))
        .order_by(Paciente.nombre)
        .all()
    )


# ---------------------------------------------------------
# LISTAR PACIENTES POR DUEÑO
# ---------------------------------------------------------
def listar_pacientes_por_dueno(
    db: Session,
    dueno_id: int
) -> list[Paciente]:
    """
    Devuelve todos los pacientes activos de un dueño.
    """

    return (
        db.query(Paciente)
        .filter(
            Paciente.dueno_id == dueno_id,
            Paciente.activo.is_(True)
        )
        .order_by(Paciente.nombre)
        .all()
    )


# ---------------------------------------------------------
# ACTUALIZAR PACIENTE
# ---------------------------------------------------------
def actualizar_paciente(
    db: Session,
    paciente: Paciente,
    *,
    nombre: str | None = None,
    especie: str | None = None,
    raza: str | None = None,
    sexo: str | None = None,
    fecha_nacimiento=None
) -> Paciente:
    """
    Actualiza los datos de una mascota existente.
    Recibe la entidad ya cargada.
    """

    if nombre is not None:
        paciente.nombre = nombre
    if especie is not None:
        paciente.especie = especie
    if raza is not None:
        paciente.raza = raza
    if sexo is not None:
        paciente.sexo = sexo
    if fecha_nacimiento is not None:
        paciente.fecha_nacimiento = fecha_nacimiento

    return paciente


# ---------------------------------------------------------
# CAMBIAR DUEÑO DE PACIENTE (CASO ESPECIAL)
# ---------------------------------------------------------
def cambiar_dueno_paciente(
    db: Session,
    paciente: Paciente,
    *,
    nuevo_dueno_id: int
) -> Paciente:
    """
    Reasigna una mascota a otro dueño.
    Caso excepcional y controlado.
    """

    paciente.dueno_id = nuevo_dueno_id
    return paciente


# ---------------------------------------------------------
# SOFT DELETE DE PACIENTE
# ---------------------------------------------------------
def desactivar_paciente(
    db: Session,
    paciente: Paciente
) -> None:
    """
    Marca un paciente como inactivo (soft delete).
    """

    paciente.activo = False
