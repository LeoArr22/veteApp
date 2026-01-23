# services/paciente_service.py

from sqlalchemy.orm import Session
from database.crud.paciente import (
    crear_paciente,
    obtener_paciente_por_id,
    obtener_paciente_completo,
    listar_pacientes_por_dueno,
    actualizar_paciente,
    cambiar_estado_paciente,
    cambiar_dueno_paciente
)
from database.crud.dueno import obtener_dueno_por_id
from application.dto.paciente_dto import (
    PacienteCreateDTO,
    PacienteReadDTO,
    PacienteUpdateDTO
)
from exceptions.domain import (
    PacienteNotFoundError,
    DuenoNotFoundError
)

# ---------------------------------------------------------
# CREAR PACIENTE
# ---------------------------------------------------------
def crear_paciente_service(db: Session, data: PacienteCreateDTO) -> PacienteReadDTO:
    """
    Registra una mascota validando que el dueño exista y esté activo.
    """
    dueno = obtener_dueno_por_id(db, data.dueno_id)
    if not dueno:
        raise DuenoNotFoundError(f"No se puede crear el paciente: El dueño {data.dueno_id} no existe o está inactivo")

    paciente = crear_paciente(
        db,
        nombre=data.nombre,
        especie=data.especie,
        dueno_id=data.dueno_id,
        raza=data.raza,
        sexo=data.sexo,
        fecha_nacimiento=data.fecha_nacimiento
    )
    return PacienteReadDTO.model_validate(paciente)


# ---------------------------------------------------------
# OBTENER PACIENTE POR ID
# ---------------------------------------------------------
def obtener_paciente_por_id_service(db: Session, paciente_id: int) -> PacienteReadDTO:
    """
    Busca un paciente activo por su ID.
    """
    paciente = obtener_paciente_por_id(db, paciente_id)
    if not paciente:
        raise PacienteNotFoundError(f"El paciente con ID {paciente_id} no fue encontrado")
    
    return PacienteReadDTO.model_validate(paciente)


# ---------------------------------------------------------
# LISTAR PACIENTES POR DUEÑO
# ---------------------------------------------------------
def listar_pacientes_por_dueno_service(db: Session, dueno_id: int, solo_activos: bool = True) -> list[PacienteReadDTO]:
    """
    Retorna las mascotas asociadas a un dueño.
    """
    # Validamos que el dueño exista (aunque sea inactivo para ver su histórico)
    if not obtener_dueno_por_id(db, dueno_id) and solo_activos:
         raise DuenoNotFoundError(f"No se pueden listar pacientes: Dueño {dueno_id} no existe")

    pacientes = listar_pacientes_por_dueno(db, dueno_id, solo_activos=solo_activos)
    return [PacienteReadDTO.model_validate(p) for p in pacientes]


# ---------------------------------------------------------
# ACTUALIZAR PACIENTE
# ---------------------------------------------------------
def actualizar_paciente_service(
    db: Session, 
    paciente_id: int, 
    data: PacienteUpdateDTO
) -> PacienteReadDTO:
    """
    Actualiza los datos de una mascota activa.
    """
    paciente = obtener_paciente_por_id(db, paciente_id)
    if not paciente:
        raise PacienteNotFoundError(f"No se puede actualizar: El paciente con ID {paciente_id} no existe")

    # Usamos model_dump para pasar solo los campos que vienen en el DTO
    actualizar_paciente(db, paciente, **data.model_dump(exclude_unset=True))
    
    return PacienteReadDTO.model_validate(paciente)


# ---------------------------------------------------------
# CAMBIAR ESTADO (DESACTIVAR / REACTIVAR)
# ---------------------------------------------------------
def desactivar_paciente_service(db: Session, paciente_id: int) -> None:
    """
    Baja lógica de la mascota.
    """
    paciente = obtener_paciente_por_id(db, paciente_id)
    if not paciente:
        raise PacienteNotFoundError(f"No se puede desactivar: El paciente {paciente_id} no existe")

    cambiar_estado_paciente(db, paciente, estado=False)


def reactivar_paciente_service(db: Session, paciente_id: int) -> PacienteReadDTO:
    """
    Restaura una mascota inactiva.
    """
    paciente = obtener_paciente_completo(db, paciente_id)
    if not paciente:
        raise PacienteNotFoundError(f"El registro de la mascota {paciente_id} no existe")
    
    cambiar_estado_paciente(db, paciente, estado=True)
    return PacienteReadDTO.model_validate(paciente)

# ---------------------------------------------------------
# TRANSFERIR MASCOTA (CAMBIO DE DUEÑO)
# ---------------------------------------------------------
def transferir_paciente_service(db: Session, paciente_id: int, nuevo_dueno_id: int) -> PacienteReadDTO:
    """
    Cambia la titularidad de una mascota a otro dueño.
    """
    # 1. Buscamos al paciente
    paciente = obtener_paciente_por_id(db, paciente_id)
    if not paciente:
        raise PacienteNotFoundError(f"Paciente con ID {paciente_id} no encontrado")
        
    # 2. Validamos que el nuevo dueño exista
    if not obtener_dueno_por_id(db, nuevo_dueno_id):
        raise DuenoNotFoundError(f"El nuevo dueño con ID {nuevo_dueno_id} no existe o está inactivo")
        
    # 3. Aplicamos el cambio mediante el CRUD
    cambiar_dueno_paciente(db, paciente, nuevo_dueno_id=nuevo_dueno_id)
    
    return PacienteReadDTO.model_validate(paciente)