# services/consulta_service.py

from sqlalchemy.orm import Session
from database.crud.consulta import (
    crear_consulta,
    obtener_consulta_por_id,
    obtener_consulta_completa,
    listar_consultas_paciente,
    cambiar_estado_consulta
)
from database.crud.paciente import obtener_paciente_por_id
from database.crud.veterinario import obtener_veterinario_por_id
from application.dto.consulta_dto import ConsultaCreateDTO, ConsultaReadDTO
from exceptions.domain import (
    ConsultaNotFoundError, 
    PacienteNotFoundError, 
    VeterinarioNotFoundError
)

# ---------------------------------------------------------
# REGISTRAR CONSULTA
# ---------------------------------------------------------
def crear_consulta_service(db: Session, data: ConsultaCreateDTO) -> ConsultaReadDTO:
    """
    Registra un acto médico. Valida que el paciente y el veterinario
    estén activos en el sistema al momento de la carga.
    """
    if not obtener_paciente_por_id(db, data.paciente_id):
        raise PacienteNotFoundError(f"Error: El paciente ID {data.paciente_id} no existe o está inactivo")
    
    if not obtener_veterinario_por_id(db, data.veterinario_id):
        raise VeterinarioNotFoundError(f"Error: El veterinario ID {data.veterinario_id} no existe o está inactivo")

    # Creamos la consulta usando argumentos nombrados (obligatorios por el *)
    nueva = crear_consulta(
        db,
        paciente_id=data.paciente_id,
        veterinario_id=data.veterinario_id,
        motivo=data.motivo,
        diagnostico=data.diagnostico,
        observaciones=data.observaciones
    )
    return ConsultaReadDTO.model_validate(nueva)


# ---------------------------------------------------------
# OBTENER CONSULTA
# ---------------------------------------------------------
def obtener_consulta_service(db: Session, consulta_id: int) -> ConsultaReadDTO:
    """
    Recupera los detalles de una consulta activa.
    """
    consulta = obtener_consulta_por_id(db, consulta_id)
    if not consulta:
        raise ConsultaNotFoundError(f"Consulta ID {consulta_id} no encontrada o anulada")
    
    return ConsultaReadDTO.model_validate(consulta)


# ---------------------------------------------------------
# OBTENER HISTORIAL CLÍNICO
# ---------------------------------------------------------
def obtener_historial_service(db: Session, paciente_id: int, solo_activas: bool = True) -> list[ConsultaReadDTO]:
    """
    Retorna la cronología médica de un paciente.
    """
    if not obtener_paciente_por_id(db, paciente_id) and solo_activas:
        raise PacienteNotFoundError(f"No se puede obtener historial: Paciente {paciente_id} no encontrado")
        
    consultas = listar_consultas_paciente(db, paciente_id, solo_activas=solo_activas)
    return [ConsultaReadDTO.model_validate(c) for c in consultas]


# ---------------------------------------------------------
# ESTADO (ANULAR / REACTIVAR)
# ---------------------------------------------------------
def anular_consulta_service(db: Session, consulta_id: int) -> None:
    """
    Anula una consulta (borrado lógico). Se usa para corregir errores de carga.
    """
    consulta = obtener_consulta_por_id(db, consulta_id)
    if not consulta:
        raise ConsultaNotFoundError(f"No se puede anular: La consulta {consulta_id} no existe")
    
    cambiar_estado_consulta(db, consulta, estado=False)


def reactivar_consulta_service(db: Session, consulta_id: int) -> ConsultaReadDTO:
    """
    Restaura una consulta que fue anulada previamente.
    """
    consulta = obtener_consulta_completa(db, consulta_id)
    if not consulta:
        raise ConsultaNotFoundError(f"No existe registro de la consulta ID {consulta_id}")
    
    cambiar_estado_consulta(db, consulta, estado=True)
    return ConsultaReadDTO.model_validate(consulta)