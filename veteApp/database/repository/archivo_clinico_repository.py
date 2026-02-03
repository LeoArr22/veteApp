# database/repository/archivo_clinico.py

from sqlalchemy.orm import Session
from database.models import ArchivoClinico


class ArchivoClinicoRepository:
    def crear(self, db: Session, archivo: ArchivoClinico) -> ArchivoClinico:
        db.add(archivo)
        db.flush()
        db.refresh(archivo)
        return archivo

    def obtener_por_id(self, db: Session, archivo_id: int, solo_activa: bool = True) -> ArchivoClinico | None:
        query = db.query(ArchivoClinico).filter(ArchivoClinico.id == archivo_id)
        if solo_activa:
            query = query.filter(ArchivoClinico.activo.is_(True))
        return query.one_or_none()

    def listar_por_consulta(self, db: Session, consulta_id: int, solo_activos: bool = True) -> list[ArchivoClinico]:
        query = db.query(ArchivoClinico).filter(ArchivoClinico.consulta_id == consulta_id)
        if solo_activos:
            query = query.filter(ArchivoClinico.activo.is_(True))
        return query.all()

    def cambiar_estado(self, db: Session, archivo: ArchivoClinico, estado: bool) -> ArchivoClinico:
        archivo.activo = estado
        db.flush()
        db.refresh(archivo)
        return archivo