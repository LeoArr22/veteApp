# database/repository/paciente.py

from sqlalchemy.orm import Session
from database.models import Paciente

# ---------------------------------------------------------
# CREAR PACIENTE (MASCOTA)
# ---------------------------------------------------------
def crear_paciente(
    db: Session,
    *,
    nombre: str,
    especie: str,
    dueno_id: int,
    raza: str | None = None,
    sexo: str | None = None,
    fecha_nacimiento=None
) -> Paciente:
    """
    Crea una nueva mascota (paciente) en estado activo.
    """
    paciente = Paciente(
        nombre=nombre,
        especie=especie,
        raza=raza,
        sexo=sexo,
        fecha_nacimiento=fecha_nacimiento,
        dueno_id=dueno_id,
        activo=True
    )
    db.add(paciente)
    # Sincroniza con la DB para obtener el ID y validar restricciones
    db.flush()
    # Recarga el objeto para obtener valores generados por el motor (ej. fechas)
    db.refresh(paciente)
    return paciente


# ---------------------------------------------------------
# OBTENER PACIENTE POR ID
# ---------------------------------------------------------
def obtener_paciente_por_id(db: Session, paciente_id: int) -> Paciente | None:
    """
    Busca un paciente activo por su ID.
    """
    return (
        db.query(Paciente)
        .filter(Paciente.id == paciente_id, Paciente.activo.is_(True))
        .one_or_none()
    )


# ---------------------------------------------------------
# OBTENER PACIENTE COMPLETO (INCLUYE INACTIVOS)
# ---------------------------------------------------------
def obtener_paciente_completo(db: Session, paciente_id: int) -> Paciente | None:
    """
    Busca un paciente por ID sin importar su estado. 
    Útil para reactivación o auditoría.
    """
    return db.query(Paciente).filter(Paciente.id == paciente_id).one_or_none()


# ---------------------------------------------------------
# LISTAR PACIENTES (POR DUEÑO O GENERAL)
# ---------------------------------------------------------
def listar_pacientes_por_dueno(db: Session, dueno_id: int, solo_activos: bool = True) -> list[Paciente]:
    """
    Retorna las mascotas de un dueño, ordenadas por nombre.
    """
    query = db.query(Paciente).filter(Paciente.dueno_id == dueno_id)
    if solo_activos:
        query = query.filter(Paciente.activo.is_(True))
    
    return query.order_by(Paciente.nombre).all()


# ---------------------------------------------------------
# ACTUALIZAR PACIENTE
# ---------------------------------------------------------
def actualizar_paciente(db: Session, paciente: Paciente, **kwargs) -> Paciente:
    """
    Actualiza datos mediante keywords (nombre, raza, peso, etc).
    """
    for key, value in kwargs.items():
        if value is not None:
            setattr(paciente, key, value)
    # Sincroniza con la DB para obtener el ID y validar restricciones
    db.flush()
    # Recarga el objeto para obtener valores generados por el motor (ej. fechas)
    db.refresh(paciente)
    return paciente


# ---------------------------------------------------------
# PERSISTENCIA: CAMBIAR ESTADO
# ---------------------------------------------------------
def cambiar_estado_paciente(db: Session, paciente: Paciente, *, estado: bool):
    """
    Maneja el alta/baja lógica del paciente. 
    Se usa para desactivar o reactivar.
    """
    paciente.activo = estado
    # Sincroniza con la DB para obtener el ID y validar restricciones
    db.flush()
    # Recarga el objeto para obtener valores generados por el motor (ej. fechas)
    db.refresh(estado)
    return paciente


# ---------------------------------------------------------
# CAMBIAR DUEÑO (CASO ESPECIAL)
# ---------------------------------------------------------
def cambiar_dueno_paciente(db: Session, paciente: Paciente, *, nuevo_dueno_id: int) -> Paciente:
    """
    Reasigna la mascota a otro dueño (ej. adopción o venta).
    """
    paciente.dueno_id = nuevo_dueno_id
    # Sincroniza con la DB para obtener el ID y validar restricciones
    db.flush()
    # Recarga el objeto para obtener valores generados por el motor (ej. fechas)
    db.refresh(paciente)
    return paciente