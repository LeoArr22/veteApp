# database/crud/consulta.py

from sqlalchemy.orm import Session
from database.models import Consulta


# ---------------------------------------------------------
# CREAR CONSULTA
# ---------------------------------------------------------
def crear_consulta(
    db: Session,
    *,
    paciente_id: int,
    veterinario_id: int,
    motivo: str,
    diagnostico: str | None = None,
    observaciones: str | None = None
) -> Consulta:
    """
    Crea una nueva consulta.
    """

    consulta = Consulta(
        paciente_id=paciente_id,
        veterinario_id=veterinario_id,
        motivo=motivo,
        diagnostico=diagnostico,
        observaciones=observaciones,
        activo=True
    )

    db.add(consulta)
    return consulta


# ---------------------------------------------------------
# OBTENER CONSULTA POR ID
# ---------------------------------------------------------
def obtener_consulta_por_id(
    db: Session,
    consulta_id: int
) -> Consulta | None:
    """
    Devuelve una consulta activa por ID o None si no existe.
    """

    return (
        db.query(Consulta)
        .filter(
            Consulta.id == consulta_id,
            Consulta.activo.is_(True)
        )
        .one_or_none()
    )


# ---------------------------------------------------------
# LISTAR CONSULTAS DE UN PACIENTE
# ---------------------------------------------------------
def listar_consultas_por_paciente(
    db: Session,
    paciente_id: int
) -> list[Consulta]:
    """
    Devuelve todas las consultas activas de un paciente,
    ordenadas por fecha.
    """

    return (
        db.query(Consulta)
        .filter(
            Consulta.paciente_id == paciente_id,
            Consulta.activo.is_(True)
        )
        .order_by(Consulta.fecha)
        .all()
    )


# ---------------------------------------------------------
# ACTUALIZAR CONSULTA
# ---------------------------------------------------------
def actualizar_consulta(
    db: Session,
    consulta: Consulta,
    *,
    motivo: str | None = None,
    diagnostico: str | None = None,
    observaciones: str | None = None
) -> Consulta:
    """
    Actualiza los datos clínicos de una consulta existente.
    """

    if motivo is not None:
        consulta.motivo = motivo
    if diagnostico is not None:
        consulta.diagnostico = diagnostico
    if observaciones is not None:
        consulta.observaciones = observaciones

    return consulta


# ---------------------------------------------------------
# SOFT DELETE DE CONSULTA
# ---------------------------------------------------------
def desactivar_consulta(
    db: Session,
    consulta: Consulta
) -> None:
    """
    Marca una consulta como inactiva (soft delete).
    """

    consulta.activo = False
