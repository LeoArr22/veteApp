# services/veterinario_service.py

from sqlalchemy.orm import Session
from veteApp.database.repository.veterinario_repository import (
    crear_veterinario,
    obtener_veterinario_por_id,
    obtener_veterinario_por_matricula,
    obtener_veterinario_completo,
    listar_veterinarios_activos,
    listar_todos_los_veterinarios,
    actualizar_veterinario,
    cambiar_estado_veterinario
)
from application.dto.veterinario_dto import (
    VeterinarioCreateDTO,
    VeterinarioReadDTO,
    VeterinarioUpdateDTO
)
from exceptions.domain import (
    VeterinarioNotFoundError,
    VeterinarioAlreadyExistsError
)

# ---------------------------------------------------------
# REGISTRAR PROFESIONAL
# ---------------------------------------------------------
def crear_veterinario_service(db: Session, data: VeterinarioCreateDTO) -> VeterinarioReadDTO:
    """
    Crea un veterinario verificando que la matrícula sea única.
    """
    if obtener_veterinario_por_matricula(db, data.matricula):
        raise VeterinarioAlreadyExistsError(f"La matrícula {data.matricula} ya está registrada")
    
    nuevo = crear_veterinario(
        db,
        nombre=data.nombre,
        matricula=data.matricula,
        especialidad=data.especialidad,
        telefono=data.telefono
    )
    return VeterinarioReadDTO.model_validate(nuevo)


# ---------------------------------------------------------
# OBTENER VETERINARIO
# ---------------------------------------------------------
def obtener_veterinario_service(db: Session, veterinario_id: int) -> VeterinarioReadDTO:
    """
    Busca un veterinario activo.
    """
    vet = obtener_veterinario_por_id(db, veterinario_id)
    if not vet:
        raise VeterinarioNotFoundError(f"Veterinario con ID {veterinario_id} no encontrado")
    
    return VeterinarioReadDTO.model_validate(vet)


# ---------------------------------------------------------
# LISTAR VETERINARIOS
# ---------------------------------------------------------
def listar_veterinarios_service(db: Session, solo_activos: bool = True) -> list[VeterinarioReadDTO]:
    """
    Lista profesionales según el filtro de actividad (para el combo de selección o administración).
    """
    vets = listar_veterinarios_activos(db) if solo_activos else listar_todos_los_veterinarios(db)
    return [VeterinarioReadDTO.model_validate(v) for v in vets]


# ---------------------------------------------------------
# ACTUALIZAR VETERINARIO
# ---------------------------------------------------------
def actualizar_veterinario_service(db: Session, veterinario_id: int, data: VeterinarioUpdateDTO) -> VeterinarioReadDTO:
    """
    Actualiza datos de contacto o especialidad.
    """
    vet = obtener_veterinario_por_id(db, veterinario_id)
    if not vet:
        raise VeterinarioNotFoundError(f"No se puede actualizar: Veterinario {veterinario_id} no existe")
    
    # Pasamos los datos del DTO como un diccionario al repository
    vet_actualizado = actualizar_veterinario(db, vet, **data.model_dump(exclude_unset=True))
    return VeterinarioReadDTO.model_validate(vet_actualizado)


# ---------------------------------------------------------
# CAMBIAR ESTADO (BAJA/ALTA)
# ---------------------------------------------------------
def desactivar_veterinario_service(db: Session, veterinario_id: int) -> None:
    """
    Baja lógica del profesional.
    """
    vet = obtener_veterinario_por_id(db, veterinario_id)
    if not vet:
        raise VeterinarioNotFoundError(f"No se encontró el veterinario {veterinario_id}")
    
    cambiar_estado_veterinario(db, vet, estado=False)


def reactivar_veterinario_service(db: Session, veterinario_id: int) -> VeterinarioReadDTO:
    """
    Restaura a un profesional inactivo.
    """
    vet = obtener_veterinario_completo(db, veterinario_id)
    if not vet:
        raise VeterinarioNotFoundError(f"El registro del veterinario {veterinario_id} no existe")
    
    cambiar_estado_veterinario(db, vet, estado=True)
    return VeterinarioReadDTO.model_validate(vet)