# services/archivo_clinico_service.py

from sqlalchemy.orm import Session
from database.crud.archivo_clinico import (
    crear_archivo_clinico,
    obtener_archivo_por_id,
    obtener_archivo_completo,
    listar_archivos_por_consulta,
    cambiar_estado_archivo  # Cambiamos desactivar por la función genérica de estado
)
from database.crud.consulta import obtener_consulta_por_id
from application.dto.archivo_clinico_dto import (
    ArchivoClinicoCreateDTO,
    ArchivoClinicoReadDTO
)
from exceptions.domain import (
    ArchivoClinicoNotFoundError,
    ConsultaNotFoundError
)

# ---------------------------------------------------------
# SUBIR ARCHIVO CLÍNICO
# ---------------------------------------------------------
def subir_archivo_clinico_service(db: Session, data: ArchivoClinicoCreateDTO) -> ArchivoClinicoReadDTO:
    """
    Registra un documento (estudio, imagen, receta) vinculado a una consulta.
    """
    consulta = obtener_consulta_por_id(db, data.consulta_id)
    if not consulta:
        raise ConsultaNotFoundError(f"Error: La consulta {data.consulta_id} no existe o fue anulada")

    # Usamos argumentos nombrados para evitar errores de posición
    archivo = crear_archivo_clinico(
        db,
        consulta_id=data.consulta_id,
        nombre_original=data.nombre_original,
        ruta_archivo=data.ruta_archivo,
        tipo=data.tipo
    )
    return ArchivoClinicoReadDTO.model_validate(archivo)


# ---------------------------------------------------------
# LISTAR ARCHIVOS DE UNA CONSULTA
# ---------------------------------------------------------
def listar_archivos_consulta_service(
    db: Session, 
    consulta_id: int, 
    solo_activos: bool = True
) -> list[ArchivoClinicoReadDTO]:
    
    # Verificamos la consulta (si es solo_activos=True, la consulta debe existir)
    if solo_activos and not obtener_consulta_por_id(db, consulta_id):
        raise ConsultaNotFoundError(f"Consulta {consulta_id} no encontrada")
    
    archivos = listar_archivos_por_consulta(db, consulta_id, solo_activos=solo_activos)
    return [ArchivoClinicoReadDTO.model_validate(a) for a in archivos]

# ---------------------------------------------------------
# ESTADO (ANULAR / REACTIVAR)
# ---------------------------------------------------------
def desactivar_archivo_service(db: Session, archivo_id: int) -> None:
    """
    Anula lógicamente un archivo y devuelve el estado actualizado.
    """
    archivo = obtener_archivo_por_id(db, archivo_id)
    if not archivo:
        raise ArchivoClinicoNotFoundError(f"Archivo ID {archivo_id} no encontrado")

    archivo_editado = cambiar_estado_archivo(db, archivo, estado=False)
    return ArchivoClinicoReadDTO.model_validate(archivo_editado)

def reactivar_archivo_service(db: Session, archivo_id: int) -> ArchivoClinicoReadDTO:
    """
    Restaura un archivo que fue desactivado.
    """
    archivo = obtener_archivo_completo(db, archivo_id)
    if not archivo:
        raise ArchivoClinicoNotFoundError(f"No existe registro del archivo ID {archivo_id}")
    
    cambiar_estado_archivo(db, archivo, estado=True)
    return ArchivoClinicoReadDTO.model_validate(archivo)