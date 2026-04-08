from datetime import date
from sqlalchemy.orm import Session
from database.models import Tratamiento

class TratamientoRepository:
    def crear(self, db: Session, tratamiento: Tratamiento) -> Tratamiento:
        """Persiste un tratamiento ya instanciado por el servicio."""
        db.add(tratamiento)
        db.flush()
        db.refresh(tratamiento)
        return tratamiento

    def obtener_por_id(self, db: Session, tratamiento_id: int, solo_activo: bool = True) -> Tratamiento | None:
        """Busca un tratamiento con filtro de estado opcional."""
        query = db.query(Tratamiento).filter(Tratamiento.id == tratamiento_id)
        if solo_activo:
            query = query.filter(Tratamiento.activo.is_(True))
        return query.one_or_none()

    def listar_por_consulta(self, db: Session, consulta_id: int, solo_activos: bool = True) -> list[Tratamiento]:
        """Lista tratamientos vinculados a una consulta específica."""
        query = db.query(Tratamiento).filter(Tratamiento.consulta_id == consulta_id)
        if solo_activos:
            query = query.filter(Tratamiento.activo.is_(True))
        return query.order_by(Tratamiento.fecha_inicio).all()

    def actualizar_fin(self, db: Session, tratamiento: Tratamiento, fecha_fin: date) -> Tratamiento:
        """Actualiza la fecha de finalización del ciclo de tratamiento."""
        tratamiento.fecha_fin = fecha_fin
        db.flush()
        db.refresh(tratamiento)
        return tratamiento

    def cambiar_estado(self, db: Session, tratamiento: Tratamiento, estado: bool) -> Tratamiento:
        """Maneja el borrado lógico o reactivación."""
        tratamiento.activo = estado
        db.flush()
        db.refresh(tratamiento)
        return tratamiento