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
    matricula: str
) -> Veterinario:
    """
    Crea un nuevo veterinario.
    No hace commit.
    """

    veterinario = Veterinario(
        nombre=nombre,
        matricula=matricula,
        activo=True
    )

    db.add(veterinario)
    return veterinario


# ---------------------------------------------------------
# OBTENER VETERINARIO POR ID
# ---------------------------------------------------------
def obtener_veterinario_por_id(
    db: Session,
    veterinario_id: int
) -> Veterinario | None:
    """
    Devuelve un veterinario activo por ID o None si no existe.
    """

    return (
        db.query(Veterinario)
        .filter(
            Veterinario.id == veterinario_id,
            Veterinario.activo.is_(True)
        )
        .one_or_none()
    )


# ---------------------------------------------------------
# OBTENER VETERINARIO POR MATRÍCULA
# ---------------------------------------------------------
def obtener_veterinario_por_matricula(
    db: Session,
    matricula: str
) -> Veterinario | None:
    """
    Devuelve un veterinario activo por matrícula o None si no existe.
    """

    return (
        db.query(Veterinario)
        .filter(
            Veterinario.matricula == matricula,
            Veterinario.activo.is_(True)
        )
        .one_or_none()
    )


# ---------------------------------------------------------
# LISTAR VETERINARIOS ACTIVOS
# ---------------------------------------------------------
def listar_veterinarios(
    db: Session
) -> list[Veterinario]:
    """
    Devuelve todos los veterinarios activos ordenados por nombre.
    """

    return (
        db.query(Veterinario)
        .filter(Veterinario.activo.is_(True))
        .order_by(Veterinario.nombre)
        .all()
    )


# ---------------------------------------------------------
# ACTUALIZAR VETERINARIO
# ---------------------------------------------------------
def actualizar_veterinario(
    db: Session,
    veterinario: Veterinario,
    *,
    nombre: str | None = None
) -> Veterinario:
    """
    Actualiza los datos de un veterinario existente.
    Recibe la entidad ya cargada.
    """

    if nombre is not None:
        veterinario.nombre = nombre

    return veterinario


# ---------------------------------------------------------
# ACTUALIZAR MATRÍCULA (CASO ESPECIAL)
# ---------------------------------------------------------
def actualizar_matricula_veterinario(
    db: Session,
    veterinario: Veterinario,
    *,
    nueva_matricula: str
) -> Veterinario:
    """
    Corrige la matrícula de un veterinario.
    Caso de uso excepcional.
    """

    veterinario.matricula = nueva_matricula
    return veterinario


# ---------------------------------------------------------
# SOFT DELETE DE VETERINARIO
# ---------------------------------------------------------
def desactivar_veterinario(
    db: Session,
    veterinario: Veterinario
) -> None:
    """
    Marca un veterinario como inactivo (soft delete).
    """

    veterinario.activo = False
