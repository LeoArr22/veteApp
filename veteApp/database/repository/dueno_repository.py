from sqlalchemy.orm import Session
from database.models import Dueno

class DuenoRepository:
    def crear(self, db: Session, dueno: Dueno) -> Dueno:
        """
        Recibe la entidad ya armada por el servicio y la persiste.
        """
        db.add(dueno)
        db.flush()
        db.refresh(dueno)
        return dueno

    def obtener_por_id(self, db: Session, dueno_id: int, solo_activo: bool = True) -> Dueno | None:
        """
        Busca un dueño por ID. Permite filtrar por estado.
        """
        query = db.query(Dueno).filter(Dueno.id == dueno_id)
        if solo_activo:
            query = query.filter(Dueno.activo.is_(True))
        return query.one_or_none()

    def obtener_por_dni(self, db: Session, dni: str) -> Dueno | None:
        """
        Búsqueda por DNI para validaciones de unicidad.
        """
        return db.query(Dueno).filter(Dueno.dni == dni).one_or_none()

    def listar(self, db: Session, solo_activos: bool = True) -> list[Dueno]:
        """
        Lista dueños con opción de incluir inactivos.
        """
        query = db.query(Dueno)
        if solo_activos:
            query = query.filter(Dueno.activo.is_(True))
        return query.all()

    def actualizar(self, db: Session, dueno: Dueno, datos_nuevos: dict) -> Dueno:
        """
        Actualiza campos dinámicamente desde un diccionario.
        """
        for key, value in datos_nuevos.items():
            if hasattr(dueno, key):
                setattr(dueno, key, value)
        db.flush()
        db.refresh(dueno)
        return dueno

    def cambiar_estado(self, db: Session, dueno: Dueno, estado: bool) -> Dueno:
        """
        Maneja borrado lógico y reactivación.
        """
        dueno.activo = estado
        db.flush()
        db.refresh(dueno)
        return dueno