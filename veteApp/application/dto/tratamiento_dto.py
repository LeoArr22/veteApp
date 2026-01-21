# application/dto/tratamiento_dto.py

from datetime import date
from pydantic import BaseModel, Field


# =========================================================
# DTOs DE ENTRADA
# =========================================================

class TratamientoCreateDTO(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    dosis: str = Field(..., min_length=1, max_length=100)
    frecuencia: str | None = Field(None, max_length=100)
    duracion: str | None = Field(None, max_length=100)
    observaciones: str | None = None
    fecha_inicio: date
    consulta_id: int


class TratamientoFinalizarDTO(BaseModel):
    fecha_fin: date


# =========================================================
# DTOs DE SALIDA
# =========================================================

class TratamientoReadDTO(BaseModel):
    id: int
    nombre: str
    dosis: str
    frecuencia: str | None
    duracion: str | None
    observaciones: str | None
    fecha_inicio: date
    fecha_fin: date | None
    consulta_id: int
    activo: bool


class TratamientoListDTO(BaseModel):
    id: int
    nombre: str
    activo: bool
