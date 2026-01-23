# services/dueno_service.py

from sqlalchemy.orm import Session
from database.crud.dueno import (
    crear_dueno,
    obtener_dueno_por_id,
    obtener_dueno_por_dni,
    obtener_dueno_por_id_completo,
    listar_duenos_activos,
    listar_todos_los_duenos,
    actualizar_dueno,
    cambiar_estado_dueno
)
from database.crud.paciente import listar_pacientes_por_dueno
from application.dto.dueno_dto import (
    DuenoCreateDTO, 
    DuenoReadDTO, 
    DuenoUpdateDTO
)
from exceptions.domain import (
    DuenoNotFoundError, 
    DuenoAlreadyExistsError, 
    DuenoConditionError
)

# ---------------------------------------------------------
# CREAR DUEÑO
# ---------------------------------------------------------
def crear_dueno_service(db: Session, data: DuenoCreateDTO) -> DuenoReadDTO:
    """
    Registra un nuevo dueño validando que el DNI no esté duplicado.
    """
    if obtener_dueno_por_dni(db, data.dni):
        raise DuenoAlreadyExistsError(f"El DNI {data.dni} ya está registrado")
    
    # Llamada al CRUD usando argumentos nombrados (obligatorios por el *)
    nuevo = crear_dueno(
        db, 
        dni=data.dni, 
        nombre=data.nombre, 
        telefono=data.telefono, 
        email=data.email, 
        direccion=data.direccion
    )
    return DuenoReadDTO.model_validate(nuevo)


# ---------------------------------------------------------
# ACTUALIZAR DUEÑO
# ---------------------------------------------------------
def actualizar_dueno_service(db: Session, dueno_id: int, data: DuenoUpdateDTO) -> DuenoReadDTO:
    """
    Modifica los datos de contacto de un dueño activo.
    """
    dueno = obtener_dueno_por_id(db, dueno_id)
    if not dueno:
        raise DuenoNotFoundError(f"No se puede actualizar: El dueño ID {dueno_id} no existe")
    
    # Actualización dinámica: solo se modifican los campos enviados en el DTO
    actualizar_dueno(db, dueno, **data.model_dump(exclude_unset=True))
    
    return DuenoReadDTO.model_validate(dueno)


# ---------------------------------------------------------
# OBTENER DUEÑO POR ID
# ---------------------------------------------------------
def obtener_dueno_por_id_service(db: Session, dueno_id: int) -> DuenoReadDTO:
    """
    Recupera un dueño activo por su ID.
    """
    dueno = obtener_dueno_por_id(db, dueno_id)
    if not dueno:
        raise DuenoNotFoundError(f"El dueño ID {dueno_id} no existe o está inactivo")
    
    return DuenoReadDTO.model_validate(dueno)


# ---------------------------------------------------------
# LISTAR DUEÑOS
# ---------------------------------------------------------
def listar_duenos_service(db: Session, solo_activos: bool = True) -> list[DuenoReadDTO]:
    """
    Lista los dueños registrados en el sistema.
    """
    duenos = listar_duenos_activos(db) if solo_activos else listar_todos_los_duenos(db)
    return [DuenoReadDTO.model_validate(d) for d in duenos]


# ---------------------------------------------------------
# CAMBIAR ESTADO (DESACTIVAR / REACTIVAR)
# ---------------------------------------------------------
def desactivar_dueno_service(db: Session, dueno_id: int) -> None:
    """
    Baja lógica del dueño, validando que no tenga mascotas activas.
    """
    dueno = obtener_dueno_por_id(db, dueno_id)
    if not dueno:
        raise DuenoNotFoundError(f"No se encontró el dueño con ID {dueno_id}")

    # Regla de Negocio: No se puede desactivar si tiene pacientes activos
    pacientes = listar_pacientes_por_dueno(db, dueno_id, solo_activos=True)
    if pacientes:
        raise DuenoConditionError(
            f"El dueño tiene {len(pacientes)} mascota(s) activa(s). "
            "Debe desactivar o transferir las mascotas primero."
        )

    cambiar_estado_dueno(db, dueno, estado=False)


def reactivar_dueno_service(db: Session, dueno_id: int) -> DuenoReadDTO:
    """
    Restaura el acceso a un dueño desactivado.
    """
    dueno = obtener_dueno_por_id_completo(db, dueno_id)
    if not dueno:
        raise DuenoNotFoundError(f"Registro del dueño ID {dueno_id} no encontrado")
    
    cambiar_estado_dueno(db, dueno, estado=True)
    return DuenoReadDTO.model_validate(dueno)