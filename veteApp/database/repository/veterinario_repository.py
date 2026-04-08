from sqlalchemy.orm import Session
from database.models import Veterinario

class VeterinarioRepository:
    def crear(self, db: Session, veterinario: Veterinario) -> Veterinario:
        """Persiste un veterinario instanciado por el servicio."""
        db.add(veterinario)
        db.flush()
        db.refresh(veterinario)
        return veterinario

    def obtener_por_id(self, db: Session, veterinario_id: int, solo_activo: bool = True) -> Veterinario | None:
        """Busca un profesional con filtro opcional de estado."""
        query = db.query(Veterinario).filter(Veterinario.id == veterinario_id)
        if solo_activo:
            query = query.filter(Veterinario.activo.is_(True))
        return query.one_or_none()

    def obtener_por_matricula(self, db: Session, matricula: str) -> Veterinario | None:
        """Búsqueda por matrícula para validación de duplicados."""
        return db.query(Veterinario).filter(Veterinario.matricula == matricula).one_or_none()

    def listar(self, db: Session, solo_activos: bool = True) -> list[Veterinario]:
        """Retorna el padrón de profesionales (activos o todos)."""
        query = db.query(Veterinario)
        if solo_activos:
            query = query.filter(Veterinario.activo.is_(True))
        return query.all()

    def actualizar(self, db: Session, vet: Veterinario, datos: dict) -> Veterinario:
        """Aplica cambios dinámicos desde un diccionario de DTO."""
        for key, value in datos.items():
            if hasattr(vet, key):
                setattr(vet, key, value)
        db.flush()
        db.refresh(vet)
        return vet

    def cambiar_estado(self, db: Session, vet: Veterinario, estado: bool) -> Veterinario:
        """Gestiona el alta o baja lógica."""
        vet.activo = estado
        db.flush()
        db.refresh(vet)
        return vet