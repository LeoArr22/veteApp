from sqlalchemy.orm import Session
from database.models import Paciente

class PacienteRepository:
    def crear(self, db: Session, paciente: Paciente) -> Paciente:
        """Persiste una nueva mascota ya instanciada por el servicio."""
        db.add(paciente)
        db.flush()
        db.refresh(paciente)
        return paciente

    def obtener_por_id(self, db: Session, paciente_id: int, solo_activo: bool = True) -> Paciente | None:
        """Busca un paciente con opción de filtrar por estado."""
        query = db.query(Paciente).filter(Paciente.id == paciente_id)
        if solo_activo:
            query = query.filter(Paciente.activo.is_(True))
        return query.one_or_none()

    def listar_por_dueno(self, db: Session, dueno_id: int, solo_activos: bool = True) -> list[Paciente]:
        """Retorna las mascotas de un dueño, ordenadas por nombre."""
        query = db.query(Paciente).filter(Paciente.dueno_id == dueno_id)
        if solo_activos:
            query = query.filter(Paciente.activo.is_(True))
        
        return query.order_by(Paciente.nombre).all()

    def actualizar(self, db: Session, paciente: Paciente, datos_nuevos: dict) -> Paciente:
        """Actualiza campos dinámicamente desde un diccionario (DTO.model_dump)."""
        for key, value in datos_nuevos.items():
            if hasattr(paciente, key):
                setattr(paciente, key, value)
        db.flush()
        db.refresh(paciente)
        return paciente

    def cambiar_estado(self, db: Session, paciente: Paciente, estado: bool) -> Paciente:
        """Maneja el alta/baja lógica del paciente."""
        paciente.activo = estado
        db.flush()
        db.refresh(paciente)
        return paciente

    def trasladar_dueno(self, db: Session, paciente: Paciente, nuevo_dueno_id: int) -> Paciente:
        """Reasigna la mascota a otro dueño."""
        paciente.dueno_id = nuevo_dueno_id
        db.flush()
        db.refresh(paciente)
        return paciente