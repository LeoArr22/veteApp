from sqlalchemy.orm import Session
from database.repository.paciente_repository import PacienteRepository
from database.repository.dueno_repository import DuenoRepository
from database.models import Paciente
from application.dto.paciente_dto import (
    PacienteCreateDTO,
    PacienteReadDTO,
    PacienteUpdateDTO
)
from exceptions.domain import PacienteNotFoundError, DuenoNotFoundError

class PacienteService:
    def __init__(self):
        # Inyectamos los repositorios necesarios
        self.paciente_repo = PacienteRepository()
        self.dueno_repo = DuenoRepository()

    def registrar_paciente(self, db: Session, data: PacienteCreateDTO) -> PacienteReadDTO:
        """Registra una mascota validando que el dueño exista y esté activo."""
        if not self.dueno_repo.obtener_por_id(db, data.dueno_id):
            raise DuenoNotFoundError(f"Dueño {data.dueno_id} no encontrado o inactivo")

        # Mapeo automático (Senior Style)
        nuevo_paciente = Paciente(**data.model_dump(), activo=True)
        
        persistido = self.paciente_repo.crear(db, nuevo_paciente)
        return PacienteReadDTO.model_validate(persistido)

    def obtener_por_id(self, db: Session, paciente_id: int) -> PacienteReadDTO:
        paciente = self.paciente_repo.obtener_por_id(db, paciente_id)
        if not paciente:
            raise PacienteNotFoundError(f"Paciente ID {paciente_id} no encontrado")
        return PacienteReadDTO.model_validate(paciente)

    def listar_por_dueno(self, db: Session, dueno_id: int, solo_activos: bool = True) -> list[PacienteReadDTO]:
        # Validamos existencia del dueño
        if not self.dueno_repo.obtener_por_id(db, dueno_id, solo_activo=False):
             raise DuenoNotFoundError(f"Dueño {dueno_id} no existe")

        pacientes = self.paciente_repo.listar_por_dueno(db, dueno_id, solo_activos=solo_activos)
        return [PacienteReadDTO.model_validate(p) for p in pacientes]

    def actualizar_datos(self, db: Session, paciente_id: int, data: PacienteUpdateDTO) -> PacienteReadDTO:
        paciente = self.paciente_repo.obtener_por_id(db, paciente_id)
        if not paciente:
            raise PacienteNotFoundError(f"Paciente ID {paciente_id} no existe")

        # Actualización dinámica con exclude_unset para evitar borrar datos existentes
        actualizado = self.paciente_repo.actualizar(db, paciente, data.model_dump(exclude_unset=True))
        return PacienteReadDTO.model_validate(actualizado)

    def cambiar_disponibilidad(self, db: Session, paciente_id: int, estado: bool) -> PacienteReadDTO:
        """Maneja tanto la baja lógica como la reactivación."""
        paciente = self.paciente_repo.obtener_por_id(db, paciente_id, solo_activo=False)
        if not paciente:
            raise PacienteNotFoundError(f"Paciente {paciente_id} no encontrado")

        editado = self.paciente_repo.cambiar_estado(db, paciente, estado=estado)
        return PacienteReadDTO.model_validate(editado)

    def transferir_titularidad(self, db: Session, paciente_id: int, nuevo_dueno_id: int) -> PacienteReadDTO:
        """Cambia legalmente el dueño de una mascota."""
        # 1. Validar paciente
        paciente = self.paciente_repo.obtener_por_id(db, paciente_id)
        if not paciente:
            raise PacienteNotFoundError(f"Paciente {paciente_id} no encontrado")
            
        # 2. Validar nuevo dueño
        if not self.dueno_repo.obtener_por_id(db, nuevo_dueno_id):
            raise DuenoNotFoundError(f"Nuevo dueño {nuevo_dueno_id} no existe")
            
        # 3. Aplicar cambio
        trasladado = self.paciente_repo.trasladar_dueno(db, paciente, nuevo_dueno_id)
        return PacienteReadDTO.model_validate(trasladado)