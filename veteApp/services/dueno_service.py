from sqlalchemy.orm import Session
from database.repository.dueno_repository import DuenoRepository
from database.repository.paciente_repository import PacienteRepository
from database.models import Dueno
from application.dto.dueno_dto import DuenoCreateDTO, DuenoReadDTO, DuenoUpdateDTO
from exceptions.domain import (
    DuenoNotFoundError, 
    DuenoAlreadyExistsError, 
    DuenoConditionError
)

class DuenoService:
    def __init__(self):
        # Inyectamos los repositorios necesarios
        self.dueno_repo = DuenoRepository()
        self.paciente_repo = PacienteRepository()

    def registrar_dueno(self, db: Session, data: DuenoCreateDTO) -> DuenoReadDTO:
        """Registra un nuevo dueño validando DNI único."""
        if self.dueno_repo.obtener_por_dni(db, data.dni):
            raise DuenoAlreadyExistsError(f"El DNI {data.dni} ya está registrado")
        
        # Mapeo automático profesional (DTO -> Entidad)
        nuevo_dueno = Dueno(**data.model_dump(), activo=True)
        
        persistido = self.dueno_repo.crear(db, nuevo_dueno)
        return DuenoReadDTO.model_validate(persistido)

    def actualizar_datos(self, db: Session, dueno_id: int, data: DuenoUpdateDTO) -> DuenoReadDTO:
        """Actualiza datos de contacto de forma dinámica."""
        dueno = self.dueno_repo.obtener_por_id(db, dueno_id)
        if not dueno:
            raise DuenoNotFoundError(f"Dueño ID {dueno_id} no encontrado")
        
        # model_dump(exclude_unset=True) evita sobreescribir con Nones campos no enviados
        datos_actualizar = data.model_dump(exclude_unset=True)
        actualizado = self.dueno_repo.actualizar(db, dueno, datos_actualizar)
        
        return DuenoReadDTO.model_validate(actualizado)

    def obtener_por_id(self, db: Session, dueno_id: int) -> DuenoReadDTO:
        dueno = self.dueno_repo.obtener_por_id(db, dueno_id)
        if not dueno:
            raise DuenoNotFoundError(f"Dueño ID {dueno_id} no encontrado o inactivo")
        return DuenoReadDTO.model_validate(dueno)

    def listar(self, db: Session, solo_activos: bool = True) -> list[DuenoReadDTO]:
        duenos = self.dueno_repo.listar(db, solo_activos=solo_activos)
        return [DuenoReadDTO.model_validate(d) for d in duenos]

    def cambiar_disponibilidad(self, db: Session, dueno_id: int, estado: bool) -> DuenoReadDTO:
        """
        Maneja el alta (True) o baja (False) lógica.
        Incluye validación de integridad para bajas.
        """
        # Buscamos con solo_activo=False para poder reactivar
        dueno = self.dueno_repo.obtener_por_id(db, dueno_id, solo_activo=False)
        if not dueno:
            raise DuenoNotFoundError(f"Dueño ID {dueno_id} no encontrado")

        # REGLA DE NEGOCIO: Si se intenta desactivar (estado=False)
        if estado is False:
            pacientes = self.paciente_repo.listar_por_dueno(db, dueno_id, solo_activos=True)
            if pacientes:
                raise DuenoConditionError(
                    f"El dueño tiene {len(pacientes)} mascota(s) activa(s). No se puede dar de baja."
                )

        # Aplicamos el cambio (sea True o False)
        actualizado = self.dueno_repo.cambiar_estado(db, dueno, estado=estado)
        return DuenoReadDTO.model_validate(actualizado)