# application/dto/paciente_dto.py

from datetime import date
from pydantic import BaseModel, Field


# =========================================================
# DTOs DE ENTRADA
# =========================================================

class PacienteCreateDTO(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    especie: str = Field(..., min_length=3, max_length=50)
    raza: str | None = Field(None, max_length=50)
    sexo: str | None = Field(None, max_length=20)
    fecha_nacimiento: date | None = None
    dueno_id: int


class PacienteUpdateDTO(BaseModel):
    nombre: str | None = Field(None, min_length=2, max_length=100)
    raza: str | None = Field(None, max_length=50)
    sexo: str | None = Field(None, max_length=20)
    fecha_nacimiento: date | None = None


# =========================================================
# DTOs DE SALIDA
# =========================================================

class PacienteReadDTO(BaseModel):
    id: int
    nombre: str
    especie: str
    raza: str | None
    sexo: str | None
    fecha_nacimiento: date | None
    dueno_id: int
    activo: bool


class PacienteListDTO(BaseModel):
    id: int
    nombre: str
    especie: str
