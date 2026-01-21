# services/veterinario_service.py

from sqlalchemy.orm import Session

from database.crud.veterinario import (
    crear_veterinario,
    obtener_veterinario_por_id,
    obtener_veterinario_por_matricula,
    listar_veterinarios,
    desactivar_veterinario,
    actualizar_veterinario,
)

from application.dto.veterinario_dto import (
    VeterinarioCreateDTO,
    VeterinarioUpdateDTO,
    VeterinarioReadDTO,
)

from exceptions.domain import (
    VeterinarioNotFoundError,
    VeterinarioDuplicadoError,
)


# ---------------------------------------------------------
# CREAR VETERINARIO
# ---------------------------------------------------------
def crear_veterinario_service(
    db: Session,
    data: VeterinarioCreateDTO
) -> VeterinarioReadDTO:
    """
    Crea un veterinario validando reglas de negocio.
    """

    # Regla de negocio: matrícula única
    existente = obtener_veterinario_por_matricula(db, data.matricula)
    if existente:
        raise VeterinarioDuplicadoError(
            f"Ya existe un veterinario con matrícula {data.matricula}"
        )

    veterinario = crear_veterinario(
        db,
        nombre=data.nombre,
        matricula=data.matricula
    )

    return VeterinarioReadDTO.model_validate(veterinario)


# ---------------------------------------------------------
# OBTENER VETERINARIO POR ID
# ---------------------------------------------------------
def obtener_veterinario_por_id_service(
    db: Session,
    veterinario_id: int
) -> VeterinarioReadDTO:
    """
    Devuelve un veterinario por ID.
    """

    veterinario = obtener_veterinario_por_id(db, veterinario_id)
    if not veterinario:
        raise VeterinarioNotFoundError(
            f"No existe veterinario con id={veterinario_id}"
        )

    return VeterinarioReadDTO.model_validate(veterinario)


# ---------------------------------------------------------
# LISTAR VETERINARIOS
# ---------------------------------------------------------
def listar_veterinarios_service(
    db: Session
) -> list[VeterinarioReadDTO]:
    """
    Devuelve todos los veterinarios activos.
    """

    veterinarios = listar_veterinarios(db)

    return [
        VeterinarioReadDTO.model_validate(v)
        for v in veterinarios
    ]


# ---------------------------------------------------------
# ACTUALIZAR VETERINARIO
# ---------------------------------------------------------
def actualizar_veterinario_service(
    db: Session,
    veterinario_id: int,
    data: VeterinarioUpdateDTO
) -> VeterinarioReadDTO:
    """
    Actualiza los datos de un veterinario.
    """

    veterinario = obtener_veterinario_por_id(db, veterinario_id)
    if not veterinario:
        raise VeterinarioNotFoundError(
            f"No existe veterinario con id={veterinario_id}"
        )

    actualizar_veterinario(
        db,
        veterinario,
        nombre=data.nombre
    )

    return VeterinarioReadDTO.model_validate(veterinario)


# ---------------------------------------------------------
# DESACTIVAR VETERINARIO (SOFT DELETE)
# ---------------------------------------------------------
def desactivar_veterinario_service(
    db: Session,
    veterinario_id: int
) -> None:
    """
    Marca un veterinario como inactivo.
    """

    veterinario = obtener_veterinario_por_id(db, veterinario_id)
    if not veterinario:
        raise VeterinarioNotFoundError(
            f"No existe veterinario con id={veterinario_id}"
        )

    desactivar_veterinario(db, veterinario)
