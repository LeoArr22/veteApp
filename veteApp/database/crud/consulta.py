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
    diagnostico: str,
    observaciones: str | None = None
) -> Consulta:
    """
    Registra una nueva consulta médica en estado activo.
    El uso de '*' garantiza que no se confundan los IDs de paciente y vet.
    """
    nueva_consulta = Consulta(
        paciente_id=paciente_id,
        veterinario_id=veterinario_id,
        motivo=motivo,
        diagnostico=diagnostico,
        observaciones=observaciones,
        activo=True
    )
    db.add(nueva_consulta)
    return nueva_consulta


# ---------------------------------------------------------
# OBTENER CONSULTA
# ---------------------------------------------------------
def obtener_consulta_por_id(db: Session, consulta_id: int) -> Consulta | None:
    """
    Busca una consulta activa por su ID.
    """
    return db.query(Consulta).filter(
        Consulta.id == consulta_id, 
        Consulta.activo.is_(True)
    ).one_or_none()


# ---------------------------------------------------------
# OBTENER CONSULTA COMPLETA
# ---------------------------------------------------------
def obtener_consulta_completa(db: Session, consulta_id: int) -> Consulta | None:
    """
    Busca una consulta por ID sin importar si está anulada.
    """
    return db.query(Consulta).filter(Consulta.id == consulta_id).one_or_none()


# ---------------------------------------------------------
# LISTAR CONSULTAS POR PACIENTE
# ---------------------------------------------------------
def listar_consultas_paciente(db: Session, paciente_id: int, solo_activas: bool = True) -> list[Consulta]:
    """
    Retorna el historial médico de un paciente, ordenado por fecha descendente.
    """
    query = db.query(Consulta).filter(Consulta.paciente_id == paciente_id)
    
    if solo_activas:
        query = query.filter(Consulta.activo.is_(True))
        
    return query.order_by(Consulta.fecha.desc()).all()


# ---------------------------------------------------------
# PERSISTENCIA: CAMBIAR ESTADO
# ---------------------------------------------------------
def cambiar_estado_consulta(db: Session, consulta: Consulta, *, estado: bool):
    """
    Permite anular o reactivar una consulta (borrado lógico).
    """
    consulta.activo = estado