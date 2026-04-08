from sqlalchemy.orm import Session
from database.repository.veterinario_repository import VeterinarioRepository
from database.models import Veterinario
from application.dto.veterinario_dto import (
    VeterinarioCreateDTO,
    VeterinarioReadDTO,
    VeterinarioUpdateDTO
)
from exceptions.domain import (
    VeterinarioNotFoundError,
    VeterinarioAlreadyExistsError
)

class VeterinarioService:
    def __init__(self):
        # Inyectamos el repositorio
        self.repository = VeterinarioRepository()

    def registrar_profesional(self, db: Session, data: VeterinarioCreateDTO) -> VeterinarioReadDTO:
        """Registra un veterinario verificando matrícula única."""
        if self.repository.obtener_por_matricula(db, data.matricula):
            raise VeterinarioAlreadyExistsError(f"La matrícula {data.matricula} ya existe")
        
        # Mapeo automático limpio
        nuevo_vet = Veterinario(**data.model_dump(), activo=True)
        
        persistido = self.repository.crear(db, nuevo_vet)
        return VeterinarioReadDTO.model_validate(persistido)

    def obtener_por_id(self, db: Session, veterinario_id: int) -> VeterinarioReadDTO:
        vet = self.repository.obtener_por_id(db, veterinario_id)
        if not vet:
            raise VeterinarioNotFoundError(f"Veterinario ID {veterinario_id} no encontrado")
        return VeterinarioReadDTO.model_validate(vet)

    def listar_profesionales(self, db: Session, solo_activos: bool = True) -> list[VeterinarioReadDTO]:
        vets = self.repository.listar(db, solo_activos=solo_activos)
        return [VeterinarioReadDTO.model_validate(v) for v in vets]

    def actualizar_datos(self, db: Session, veterinario_id: int, data: VeterinarioUpdateDTO) -> VeterinarioReadDTO:
        vet = self.repository.obtener_por_id(db, veterinario_id)
        if not vet:
            raise VeterinarioNotFoundError(f"No se puede actualizar el veterinario {veterinario_id}")
        
        # Actualización dinámica usando el diccionario del DTO
        actualizado = self.repository.actualizar(db, vet, data.model_dump(exclude_unset=True))
        return VeterinarioReadDTO.model_validate(actualizado)

    def cambiar_disponibilidad(self, db: Session, veterinario_id: int, estado: bool) -> VeterinarioReadDTO:
        """Maneja el alta y baja lógica del profesional."""
        # Buscamos sin filtro de activo para permitir reactivación
        vet = self.repository.obtener_por_id(db, veterinario_id, solo_activo=False)
        if not vet:
            raise VeterinarioNotFoundError(f"Registro de veterinario {veterinario_id} no encontrado")
        
        editado = self.repository.cambiar_estado(db, vet, estado=estado)
        return VeterinarioReadDTO.model_validate(editado)