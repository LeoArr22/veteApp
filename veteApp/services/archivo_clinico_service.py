from sqlalchemy.orm import Session
from database.repository.archivo_clinico_repository import ArchivoClinicoRepository
from database.repository.consulta_repository import ConsultaRepository
from database.models import ArchivoClinico
from application.dto.archivo_clinico_dto import ArchivoClinicoCreateDTO, ArchivoClinicoReadDTO
from exceptions.domain import ArchivoClinicoNotFoundError, ConsultaNotFoundError

class ArchivoClinicoService:
    def __init__(self):
        self.archivo_repo = ArchivoClinicoRepository()
        self.consulta_repo = ConsultaRepository()

    def subir_archivo(self, db: Session, data: ArchivoClinicoCreateDTO) -> ArchivoClinicoReadDTO:
        """
        Registra un documento vinculado a una consulta validando existencia.
        """
        # 1. Validación de integridad
        if not self.consulta_repo.obtener_por_id(db, data.consulta_id):
            raise ConsultaNotFoundError(f"La consulta {data.consulta_id} no existe o fue anulada")

        # 2. Mapeo Automático (Senior Style)
        # No importa si mañana agregas 'tamaño' o 'extension', el servicio no cambia.
        nueva_entidad = ArchivoClinico(
            **data.model_dump(),
            activo=True
        )

        # 3. Persistencia y retorno
        archivo_db = self.archivo_repo.crear(db, nueva_entidad)
        return ArchivoClinicoReadDTO.model_validate(archivo_db)

    def listar_por_consulta(self, db: Session, consulta_id: int, solo_activos: bool = True) -> list[ArchivoClinicoReadDTO]:
        """
        Recupera todos los documentos de una consulta específica.
        """
        # Verificamos la consulta primero
        if not self.consulta_repo.obtener_por_id(db, consulta_id, solo_activa=solo_activos):
            raise ConsultaNotFoundError(f"Consulta {consulta_id} no encontrada o inactiva")
        
        archivos = self.archivo_repo.listar_por_consulta(db, consulta_id, solo_activos=solo_activos)
        return [ArchivoClinicoReadDTO.model_validate(a) for a in archivos]

    def cambiar_disponibilidad(self, db: Session, archivo_id: int, estado: bool) -> ArchivoClinicoReadDTO:
        """
        Maneja tanto la anulación como la reactivación (DRY - Don't Repeat Yourself).
        """
        # Buscamos sin importar el estado actual (solo_activa=False)
        archivo = self.archivo_repo.obtener_por_id(db, archivo_id, solo_activa=False)
        if not archivo:
            raise ArchivoClinicoNotFoundError(f"Archivo ID {archivo_id} no encontrado")

        archivo_editado = self.archivo_repo.cambiar_estado(db, archivo, estado=estado)
        return ArchivoClinicoReadDTO.model_validate(archivo_editado)