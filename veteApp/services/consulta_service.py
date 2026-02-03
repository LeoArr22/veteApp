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
        # Inyectamos los repositorios
        self.consulta_repo = ConsultaRepository()
        self.paciente_repo = PacienteRepository()
        self.vet_repo = VeterinarioRepository()

    def registrar_consulta(self, db: Session, data: ConsultaCreateDTO) -> ConsultaReadDTO:
        """
        Orquesta la creación de una consulta: valida actores,
        mapea datos y persiste.
        """
        # 1. Validaciones de Regla de Negocio
        # Usamos los repositorios para verificar que existan antes de operar
        if not self.paciente_repo.obtener_por_id(db, data.paciente_id):
            raise PacienteNotFoundError(f"Paciente con ID {data.paciente_id} no encontrado.")
        
        if not self.vet_repo.obtener_por_id(db, data.veterinario_id):
            raise VeterinarioNotFoundError(f"Veterinario con ID {data.veterinario_id} no encontrado.")

        # 2. Mapeo Profesional (DTO -> Entidad)
        # El ** extrae todo del DTO (motivo, diagnostico, observaciones, ids)
        # El linter está feliz porque 'diagnostico' en el DTO es 'str' obligatorio.
        nueva_entidad = Consulta(
            **data.model_dump(),
            activo=True
        )

        # 3. Persistencia
        # El repo recibe la entidad armada y la guarda
        persistida = self.consulta_repo.crear(db, nueva_entidad)
        
        # 4. Retorno (Entidad -> DTO de Salida)
        return ConsultaReadDTO.model_validate(persistida)

    def obtener_detalle(self, db: Session, consulta_id: int) -> ConsultaReadDTO:
        """Busca una consulta y la transforma para la vista."""
        consulta = self.consulta_repo.obtener_por_id(db, consulta_id)
        if not consulta:
            raise ConsultaNotFoundError(f"La consulta {consulta_id} no existe o fue eliminada.")
        
        return ConsultaReadDTO.model_validate(consulta)

    def obtener_historial_paciente(self, db: Session, paciente_id: int) -> list[ConsultaReadDTO]:
        """Obtiene todas las consultas de un paciente."""
        # Primero validamos que el paciente exista
        if not self.paciente_repo.obtener_por_id(db, paciente_id):
            raise PacienteNotFoundError(f"No se puede obtener historial: Paciente {paciente_id} inexistente.")
            
        consultas = self.consulta_repo.listar_por_paciente(db, paciente_id)
        return [ConsultaReadDTO.model_validate(c) for c in consultas]

    def anular_consulta(self, db: Session, consulta_id: int) -> None:
        """Borrado lógico de la consulta."""
        consulta = self.consulta_repo.obtener_por_id(db, consulta_id)
        if not consulta:
            raise ConsultaNotFoundError(f"No se puede anular la consulta {consulta_id}.")
        
        self.consulta_repo.cambiar_estado(db, consulta, estado=False)