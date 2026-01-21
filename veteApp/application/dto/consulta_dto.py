# application/dto/consulta_dto.py

from datetime import datetime
from pydantic import BaseModel, Field


# =========================================================
# DTOs DE ENTRADA
# =========================================================

class ConsultaCreateDTO(BaseModel):
    motivo: str = Field(..., min_length=3, max_length=200)
    diagnostico: str | None = None
    observaciones: str | None = None
    paciente_id: int
    veterinario_id: int


class ConsultaUpdateDTO(BaseModel):
    diagnostico: str | None = None
    observaciones: str | None = None


# =========================================================
# DTOs DE SALIDA
# =========================================================

class ConsultaReadDTO(BaseModel):
    id: int
    fecha: datetime
    motivo: str
    diagnostico: str | None
    observaciones: str | None
    paciente_id: int
    veterinario_id: int
    activo: bool


class ConsultaListDTO(BaseModel):
    id: int
    fecha: datetime
    motivo: str
