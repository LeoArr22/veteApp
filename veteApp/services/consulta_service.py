from sqlalchemy.orm import Session
from database.repository.consulta_repository import ConsultaRepository
from database.repository.paciente_repository import PacienteRepository
from database.repository.veterinario_repository import VeterinarioRepository
from database.models import Consulta
from application.dto.consulta_dto import ConsultaCreateDTO, ConsultaReadDTO
from exceptions.domain import (
    ConsultaNotFoundError, 
    PacienteNotFoundError, 
    VeterinarioNotFoundError
)

class ConsultaService:
    def __init__(self):
        self.consulta_repo = ConsultaRepository()
        self.paciente_repo = PacienteRepository()
        self.vet_repo = VeterinarioRepository()

    def registrar_consulta(self, db: Session, data: ConsultaCreateDTO) -> ConsultaReadDTO:
        if not self.paciente_repo.obtener_por_id(db, data.paciente_id):
            raise PacienteNotFoundError(f"Paciente ID {data.paciente_id} no encontrado.")
        
        if not self.vet_repo.obtener_por_id(db, data.veterinario_id):
            raise VeterinarioNotFoundError(f"Veterinario ID {data.veterinario_id} no encontrado.")

        nueva_entidad = Consulta(**data.model_dump(), activo=True)
        persistida = self.consulta_repo.crear(db, nueva_entidad)
        return ConsultaReadDTO.model_validate(persistida)

    def obtener_detalle(self, db: Session, consulta_id: int) -> ConsultaReadDTO:
        consulta = self.consulta_repo.obtener_por_id(db, consulta_id)
        if not consulta:
            raise ConsultaNotFoundError(f"La consulta {consulta_id} no existe.")
        return ConsultaReadDTO.model_validate(consulta)

    def obtener_historial_paciente(self, db: Session, paciente_id: int) -> list[ConsultaReadDTO]:
        if not self.paciente_repo.obtener_por_id(db, paciente_id):
            raise PacienteNotFoundError(f"Paciente {paciente_id} inexistente.")
            
        consultas = self.consulta_repo.listar_por_paciente(db, paciente_id)
        return [ConsultaReadDTO.model_validate(c) for c in consultas]

    def cambiar_disponibilidad(self, db: Session, consulta_id: int, estado: bool) -> None:
        """
        Versión mejorada de anular_consulta. 
        Permite activar (True) o desactivar (False).
        """
        # Buscamos con solo_activo=False para poder reactivar registros
        consulta = self.consulta_repo.obtener_por_id(db, consulta_id, solo_activo=False)
        if not consulta:
            raise ConsultaNotFoundError(f"Registro de consulta {consulta_id} no encontrado.")
        
        self.consulta_repo.cambiar_estado(db, consulta, estado=estado)