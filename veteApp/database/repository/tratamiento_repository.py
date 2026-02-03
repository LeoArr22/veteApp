# database/repository/tratamiento.py

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
    Registra un nuevo tratamiento vinculado a una consulta.
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
    # Sincroniza con la DB para obtener el ID y validar restricciones
    db.flush()
    # Recarga el objeto para obtener valores generados por el motor (ej. fechas)
    db.refresh(tratamiento)
    return tratamiento


# ---------------------------------------------------------
# OBTENER TRATAMIENTO POR ID
# ---------------------------------------------------------
def obtener_tratamiento_por_id(db: Session, tratamiento_id: int) -> Tratamiento | None:
    """
    Busca un tratamiento activo por su ID.
    """
    return (
        db.query(Tratamiento)
        .filter(Tratamiento.id == tratamiento_id, Tratamiento.activo.is_(True))
        .one_or_none()
    )


def obtener_tratamiento_completo(db: Session, tratamiento_id: int) -> Tratamiento | None:
    """
    Busca un tratamiento sin filtrar por estado (para auditoría).
    """
    return db.query(Tratamiento).filter(Tratamiento.id == tratamiento_id).one_or_none()


# ---------------------------------------------------------
# LISTAR TRATAMIENTOS
# ---------------------------------------------------------
def listar_tratamientos_por_consulta(db: Session, consulta_id: int) -> list[Tratamiento]:
    """
    Retorna todos los tratamientos de una consulta específica.
    """
    return (
        db.query(Tratamiento)
        .filter(Tratamiento.consulta_id == consulta_id, Tratamiento.activo.is_(True))
        .order_by(Tratamiento.fecha_inicio)
        .all()
    )


# ---------------------------------------------------------
# FINALIZAR TRATAMIENTO (ACTUALIZACIÓN DE CICLO)
# ---------------------------------------------------------
def finalizar_tratamiento(db: Session, tratamiento: Tratamiento, *, fecha_fin: date) -> Tratamiento:
    """
    Establece la fecha de finalización de un tratamiento.
    Este es el único cambio permitido sobre un tratamiento existente.
    """
    tratamiento.fecha_fin = fecha_fin
    return tratamiento


# ---------------------------------------------------------
# PERSISTENCIA: CAMBIAR ESTADO
# ---------------------------------------------------------
def cambiar_estado_tratamiento(db: Session, tratamiento: Tratamiento, *, estado: bool):
    """
    Anula o reactiva un tratamiento (borrado lógico).
    """
    tratamiento.activo = estado
    # Sincroniza con la DB para obtener el ID y validar restricciones
    db.flush()
    # Recarga el objeto para obtener valores generados por el motor (ej. fechas)
    db.refresh(tratamiento)
    return tratamiento