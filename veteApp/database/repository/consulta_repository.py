from sqlalchemy.orm import Session
from database.models import Consulta

class ConsultaRepository:
    def crear(self, db: Session, consulta: Consulta) -> Consulta:
        """
        Guarda una entidad Consulta en la base de datos.
        Recibe el objeto ya construido desde el servicio.
        """
        db.add(consulta)
        db.flush()
        db.refresh(consulta)
        return consulta

    def obtener_por_id(self, db: Session, consulta_id: int, solo_activa: bool = True) -> Consulta | None:
        query = db.query(Consulta).filter(Consulta.id == consulta_id)
        if solo_activa:
            query = query.filter(Consulta.activo.is_(True))
        return query.one_or_none()

    def listar_por_paciente(self, db: Session, paciente_id: int, solo_activas: bool = True) -> list[Consulta]:
        query = db.query(Consulta).filter(Consulta.paciente_id == paciente_id)
        if solo_activas:
            query = query.filter(Consulta.activo.is_(True))
        return query.order_by(Consulta.fecha.desc()).all()

    def cambiar_estado(self, db: Session, consulta: Consulta, estado: bool) -> Consulta:
        consulta.activo = estado
        db.flush()
        db.refresh(consulta)
        return consulta