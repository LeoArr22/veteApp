# database/crud/archivo_clinico.py

from sqlalchemy.orm import Session
from database.models import ArchivoClinico


# ---------------------------------------------------------
# CREAR ARCHIVO CLÍNICO
# ---------------------------------------------------------
def crear_archivo_clinico(
    db: Session,
    *,
    consulta_id: int,
    nombre_original: str,
    ruta_archivo: str,
    tipo: str
) -> ArchivoClinico:
    """
    Crea un nuevo archivo clínico asociado a una consulta.
    """

    archivo = ArchivoClinico(
        consulta_id=consulta_id,
        nombre_original=nombre_original,
        ruta_archivo=ruta_archivo,
        tipo=tipo,
        activo=True
    )

    db.add(archivo)
    # Sincroniza con la DB para obtener el ID y validar restricciones
    db.flush()
    # Recarga el objeto para obtener valores generados por el motor (ej. fechas)
    db.refresh(archivo)
    return archivo


# ---------------------------------------------------------
# OBTENER ARCHIVO POR ID
# ---------------------------------------------------------
def obtener_archivo_por_id(
    db: Session,
    archivo_id: int
) -> ArchivoClinico | None:
    """
    Devuelve un archivo clínico activo por ID o None si no existe.
    """

    return (
        db.query(ArchivoClinico)
        .filter(
            ArchivoClinico.id == archivo_id,
            ArchivoClinico.activo.is_(True)
        )
        .one_or_none()
    )


# ---------------------------------------------------------
# LISTAR ARCHIVOS DE UNA CONSULTA
# ---------------------------------------------------------
def listar_archivos_por_consulta(
    db: Session, 
    consulta_id: int, 
    solo_activos: bool = True  # <--- AGREGAMOS ESTE PARÁMETRO
) -> list[ArchivoClinico]:
    """
    Devuelve los archivos de una consulta, permitiendo filtrar por estado.
    """
    query = db.query(ArchivoClinico).filter(ArchivoClinico.consulta_id == consulta_id)
    
    if solo_activos:
        query = query.filter(ArchivoClinico.activo.is_(True))
    
    return query.order_by(ArchivoClinico.fecha_subida).all()

# ---------------------------------------------------------
# LISTAR ARCHIVOS DE UNA CONSULTA INCLUYENDO INACTIVOS
# ---------------------------------------------------------

def obtener_archivo_completo(db: Session, archivo_id: int) -> ArchivoClinico | None:
    """Busca el archivo sin importar si está activo o no."""
    return db.query(ArchivoClinico).filter(ArchivoClinico.id == archivo_id).first()

# ---------------------------------------------------------
# SOFT DELETE DE ARCHIVO CLÍNICO
# ---------------------------------------------------------
def cambiar_estado_archivo(db: Session, archivo: ArchivoClinico, estado: bool):
    """Para anular o reactivar."""
    archivo.activo = estado
    # Sincroniza con la DB para obtener el ID y validar restricciones
    db.flush()
    # Recarga el objeto para obtener valores generados por el motor (ej. fechas)
    db.refresh(archivo)    
    return archivo
