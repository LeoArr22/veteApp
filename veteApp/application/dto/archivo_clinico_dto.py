# application/dto/archivo_clinico_dto.py

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


# =========================================================
# DTOs DE ENTRADA
# =========================================================

class ArchivoClinicoCreateDTO(BaseModel):
    nombre_original: str = Field(..., min_length=1, max_length=200)
    ruta_archivo: str = Field(..., min_length=1, max_length=300)
    tipo: str = Field(..., min_length=3, max_length=50)
    consulta_id: int


# =========================================================
# DTOs DE SALIDA
# =========================================================

class ArchivoClinicoReadDTO(BaseModel):
    id: int
    nombre_original: str
    ruta_archivo: str
    tipo: str
    fecha_subida: datetime
    consulta_id: int
    activo: bool
    model_config = ConfigDict(from_attributes=True)

class ArchivoClinicoListDTO(BaseModel):
    id: int
    nombre_original: str
    tipo: str
    model_config = ConfigDict(from_attributes=True)