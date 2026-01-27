# services/tratamiento_service.py
from datetime import date
from sqlalchemy.orm import Session
from database.crud.tratamiento import (
    crear_tratamiento,
    obtener_tratamiento_por_id,
    obtener_tratamiento_completo,
    listar_tratamientos_por_consulta,
    finalizar_tratamiento,
    cambiar_estado_tratamiento
)
from database.crud.consulta import obtener_consulta_por_id
from application.dto.tratamiento_dto import (
    TratamientoCreateDTO,
    TratamientoReadDTO,
    TratamientoFinalizarDTO
)
from exceptions.domain import (
    TratamientoNotFoundError,
    ConsultaNotFoundError
)

# ---------------------------------------------------------
# AGREGAR TRATAMIENTO
# ---------------------------------------------------------
def agregar_tratamiento_service(db: Session, data: TratamientoCreateDTO) -> TratamientoReadDTO:
    """
    Registra un nuevo tratamiento vinculado a una consulta médica.
    """
    # Si el veterinario eligió una fecha (ayer, por ejemplo), se usa esa.
    # Si lo dejó vacío, el sistema asume que es hoy.
    fecha_a_guardar = data.fecha_inicio if data.fecha_inicio is not None else date.today()
    
    consulta = obtener_consulta_por_id(db, data.consulta_id)
    if not consulta:
        raise ConsultaNotFoundError(f"No se puede registrar: La consulta {data.consulta_id} no existe")

    tratamiento = crear_tratamiento(
        db,
        nombre=data.nombre,
        dosis=data.dosis,
        frecuencia=data.frecuencia,
        duracion=data.duracion,
        observaciones=data.observaciones,
        fecha_inicio=fecha_a_guardar,
        fecha_fin=data.fecha_fin,
        consulta_id=data.consulta_id
    )
    return TratamientoReadDTO.model_validate(tratamiento)


# ---------------------------------------------------------
# OBTENER TRATAMIENTO
# ---------------------------------------------------------
def obtener_tratamiento_service(db: Session, tratamiento_id: int) -> TratamientoReadDTO:
    """
    Recupera un tratamiento activo por ID.
    """
    tratamiento = obtener_treatment_por_id(db, tratamiento_id)
    if not tratamiento:
        raise TratamientoNotFoundError(f"Tratamiento con ID {tratamiento_id} no encontrado")
    
    return TratamientoReadDTO.model_validate(tratamiento)


# ---------------------------------------------------------
# LISTAR POR CONSULTA
# ---------------------------------------------------------
def listar_tratamientos_por_consulta_service(db: Session, consulta_id: int) -> list[TratamientoReadDTO]:
    """
    Lista todos los tratamientos activos de una consulta específica.
    """
    # Validamos que la consulta exista
    if not obtener_consulta_por_id(db, consulta_id):
        raise ConsultaNotFoundError(f"Consulta {consulta_id} no encontrada")
        
    tratamientos = listar_tratamientos_por_consulta(db, consulta_id)
    return [TratamientoReadDTO.model_validate(t) for t in tratamientos]


# ---------------------------------------------------------
# FINALIZAR TRATAMIENTO
# ---------------------------------------------------------
def finalizar_tratamiento_service(
    db: Session, 
    tratamiento_id: int, 
    data: TratamientoFinalizarDTO
) -> TratamientoReadDTO:
    """
    Establece la fecha de fin de un tratamiento activo.
    """
    tratamiento = obtener_tratamiento_por_id(db, tratamiento_id)
    if not tratamiento:
        raise TratamientoNotFoundError(f"No se puede finalizar: Tratamiento {tratamiento_id} no encontrado")

    # Llamamos al CRUD usando el separador * (keyword argument)
    finalizar_tratamiento(db, tratamiento, fecha_fin=data.fecha_fin)
    return TratamientoReadDTO.model_validate(tratamiento)


# ---------------------------------------------------------
# ANULAR / REACTIVAR TRATAMIENTO
# ---------------------------------------------------------
def desactivar_tratamiento_service(db: Session, tratamiento_id: int) -> None:
    """
    Anula un tratamiento (borrado lógico) por error de carga.
    """
    tratamiento = obtener_tratamiento_por_id(db, tratamiento_id)
    if not tratamiento:
        raise TratamientoNotFoundError(f"No se puede anular: Tratamiento {tratamiento_id} no encontrado")

    cambiar_estado_tratamiento(db, tratamiento, estado=False)


def reactivar_tratamiento_service(db: Session, tratamiento_id: int) -> TratamientoReadDTO:
    """
    Restaura un tratamiento anulado previamente.
    """
    tratamiento = obtener_tratamiento_completo(db, tratamiento_id)
    if not tratamiento:
        raise TratamientoNotFoundError(f"Registro de tratamiento {tratamiento_id} no encontrado")
    
    cambiar_estado_tratamiento(db, tratamiento, estado=True)
    return TratamientoReadDTO.model_validate(tratamiento)