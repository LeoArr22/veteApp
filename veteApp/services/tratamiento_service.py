from datetime import date
from sqlalchemy.orm import Session
from database.repository.tratamiento_repository import TratamientoRepository
from database.repository.consulta_repository import ConsultaRepository
from database.models import Tratamiento
from application.dto.tratamiento_dto import (
    TratamientoCreateDTO,
    TratamientoReadDTO,
    TratamientoFinalizarDTO
)
from exceptions.domain import TratamientoNotFoundError, ConsultaNotFoundError

class TratamientoService:
    def __init__(self):
        self.tratamiento_repo = TratamientoRepository()
        self.consulta_repo = ConsultaRepository()

    def agregar_tratamiento(self, db: Session, data: TratamientoCreateDTO) -> TratamientoReadDTO:
        """
        Registra un tratamiento vinculado a una consulta.
        Gestiona la fecha de inicio por defecto si no se provee.
        """
        # 1. Validación de integridad
        if not self.consulta_repo.obtener_por_id(db, data.consulta_id):
            raise ConsultaNotFoundError(f"La consulta {data.consulta_id} no existe")

        # 2. Lógica de negocio para fechas
        # Si el DTO no trae fecha, el servicio decide que es hoy.
        fecha_inicio = data.fecha_inicio or date.today()

        # 3. Mapeo Automático
        nuevo_tratamiento = Tratamiento(
            **data.model_dump(exclude={"fecha_inicio"}), # Sacamos la original
            fecha_inicio=fecha_inicio,                    # Ponemos la procesada
            activo=True
        )

        # 4. Persistencia
        persistido = self.tratamiento_repo.crear(db, nuevo_tratamiento)
        return TratamientoReadDTO.model_validate(persistido)

    def obtener_por_id(self, db: Session, tratamiento_id: int) -> TratamientoReadDTO:
        tratamiento = self.tratamiento_repo.obtener_por_id(db, tratamiento_id)
        if not tratamiento:
            raise TratamientoNotFoundError(f"Tratamiento {tratamiento_id} no encontrado")
        return TratamientoReadDTO.model_validate(tratamiento)

    def listar_por_consulta(self, db: Session, consulta_id: int) -> list[TratamientoReadDTO]:
        if not self.consulta_repo.obtener_por_id(db, consulta_id):
            raise ConsultaNotFoundError(f"Consulta {consulta_id} no encontrada")
            
        tratamientos = self.tratamiento_repo.listar_por_consulta(db, consulta_id)
        return [TratamientoReadDTO.model_validate(t) for t in tratamientos]

    def finalizar_tratamiento(self, db: Session, tratamiento_id: int, data: TratamientoFinalizarDTO) -> TratamientoReadDTO:
        """Establece la fecha de conclusión de un tratamiento."""
        tratamiento = self.tratamiento_repo.obtener_por_id(db, tratamiento_id)
        if not tratamiento:
            raise TratamientoNotFoundError(f"Tratamiento {tratamiento_id} no encontrado")

        # Usamos el repositorio para actualizar solo la fecha de fin
        actualizado = self.tratamiento_repo.actualizar_fin(db, tratamiento, data.fecha_fin)
        return TratamientoReadDTO.model_validate(actualizado)

    def cambiar_disponibilidad(self, db: Session, tratamiento_id: int, estado: bool) -> TratamientoReadDTO:
        """Anula o reactiva un tratamiento."""
        tratamiento = self.tratamiento_repo.obtener_por_id(db, tratamiento_id, solo_activo=False)
        if not tratamiento:
            raise TratamientoNotFoundError(f"Registro de tratamiento {tratamiento_id} no encontrado")

        editado = self.tratamiento_repo.cambiar_estado(db, tratamiento, estado=estado)
        return TratamientoReadDTO.model_validate(editado)