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
    consulta_id: int
) -> list[ArchivoClinico]:
    """
    Devuelve todos los archivos activos de una consulta.
    """

    return (
        db.query(ArchivoClinico)
        .filter(
            ArchivoClinico.consulta_id == consulta_id,
            ArchivoClinico.activo.is_(True)
        )
        .order_by(ArchivoClinico.fecha_subida)
        .all()
    )


# ---------------------------------------------------------
# SOFT DELETE DE ARCHIVO CLÍNICO
# ---------------------------------------------------------
def desactivar_archivo_clinico(
    db: Session,
    archivo: ArchivoClinico
) -> None:
    """
    Marca un archivo clínico como inactivo (soft delete).
    """

    archivo.activo = False
