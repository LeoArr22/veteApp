# database/crud/tratamiento.py

from datetime import date
from sqlalchemy.orm import Session

from database.models import Tratamiento


# ---------------------------------------------------------
# CREAR TRATAMIENTO
# ---------------------------------------------------------
def crear_tratamiento(
    db: Session,
    *,
    nombre: str,
    dosis: str,
    frecuencia: str | None = None,
    duracion: str | None = None,
    observaciones: str | None = None,
    fecha_inicio: date,
    fecha_fin: date | None = None,
    consulta_id: int
) -> Tratamiento:
    """
    Crea un nuevo tratamiento.
    """

    tratamiento = Tratamiento(
        nombre=nombre,
        dosis=dosis,
        frecuencia=frecuencia,
        duracion=duracion,
        observaciones=observaciones,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        consulta_id=consulta_id,
        activo=True
    )

    db.add(tratamiento)
    return tratamiento


# ---------------------------------------------------------
# OBTENER TRATAMIENTO POR ID
# ---------------------------------------------------------
def obtener_tratamiento_por_id(
    db: Session,
    tratamiento_id: int
) -> Tratamiento | None:
    """
    Devuelve un tratamiento activo por ID o None si no existe.
    """

    return (
        db.query(Tratamiento)
        .filter(
            Tratamiento.id == tratamiento_id,
            Tratamiento.activo.is_(True)
        )
        .one_or_none()
    )


# ---------------------------------------------------------
# LISTAR TRATAMIENTOS POR CONSULTA
# ---------------------------------------------------------
def listar_tratamientos_por_consulta(
    db: Session,
    consulta_id: int
) -> list[Tratamiento]:
    """
    Devuelve todos los tratamientos activos de una consulta.
    """

    return (
        db.query(Tratamiento)
        .filter(
            Tratamiento.consulta_id == consulta_id,
            Tratamiento.activo.is_(True)
        )
        .order_by(Tratamiento.fecha_inicio)
        .all()
    )


# ---------------------------------------------------------
# LISTAR TRATAMIENTOS ACTIVOS
# ---------------------------------------------------------
def listar_tratamientos_activos(
    db: Session
) -> list[Tratamiento]:
    """
    Devuelve todos los tratamientos activos.
    """

    return (
        db.query(Tratamiento)
        .filter(Tratamiento.activo.is_(True))
        .order_by(Tratamiento.fecha_inicio)
        .all()
    )


# ---------------------------------------------------------
# ACTUALIZAR TRATAMIENTO
# ---------------------------------------------------------
def actualizar_tratamiento(
    db: Session,
    tratamiento: Tratamiento,
    *,
    nombre: str | None = None,
    dosis: str | None = None,
    frecuencia: str | None = None,
    duracion: str | None = None,
    observaciones: str | None = None,
    fecha_inicio: date | None = None,
    fecha_fin: date | None = None
) -> Tratamiento:
    """
    Actualiza los datos de un tratamiento existente.
    Recibe la entidad ya cargada.
    """

    if nombre is not None:
        tratamiento.nombre = nombre
    if dosis is not None:
        tratamiento.dosis = dosis
    if frecuencia is not None:
        tratamiento.frecuencia = frecuencia
    if duracion is not None:
        tratamiento.duracion = duracion
    if observaciones is not None:
        tratamiento.observaciones = observaciones
    if fecha_inicio is not None:
        tratamiento.fecha_inicio = fecha_inicio
    if fecha_fin is not None:
        tratamiento.fecha_fin = fecha_fin

    return tratamiento


# ---------------------------------------------------------
# FINALIZAR TRATAMIENTO (SET FECHA FIN)
# ---------------------------------------------------------
def finalizar_tratamiento(
    db: Session,
    tratamiento: Tratamiento,
    *,
    fecha_fin: date
) -> Tratamiento:
    """
    Marca un tratamiento como finalizado estableciendo fecha_fin.
    """

    tratamiento.fecha_fin = fecha_fin
    return tratamiento


# ---------------------------------------------------------
# SOFT DELETE DE TRATAMIENTO
# ---------------------------------------------------------
def desactivar_tratamiento(
    db: Session,
    tratamiento: Tratamiento
) -> None:
    """
    Marca un tratamiento como inactivo (soft delete).
    """

    tratamiento.activo = False
