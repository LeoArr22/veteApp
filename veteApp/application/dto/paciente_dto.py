from datetime import date
from pydantic import BaseModel, ConfigDict, Field

# =========================================================
# DTOs DE ENTRADA
# =========================================================

class PacienteCreateDTO(BaseModel):
    dueno_id: int
    nombre: str = Field(..., min_length=2, max_length=100)
    especie: str = Field(..., min_length=3, max_length=50)
    # Opcionales al final
    raza: str | None = Field(default=None, max_length=50)
    sexo: str | None = Field(default=None, max_length=20)
    fecha_nacimiento: date | None = Field(default=None)

class PacienteUpdateDTO(BaseModel):
    """
    Permite actualizaciones parciales. 
    Incluir dueno_id aquí facilita las transferencias de dueño.
    """
    nombre: str | None = Field(None, min_length=2, max_length=100)
    especie: str | None = Field(None, min_length=3, max_length=50) 
    raza: str | None = Field(None, max_length=50)
    sexo: str | None = Field(None, max_length=20)
    fecha_nacimiento: date | None = None
    dueno_id: int | None = None #

# =========================================================
# DTOs DE SALIDA
# =========================================================

class PacienteReadDTO(PacienteCreateDTO):
    """Hereda todo de CreateDTO y agrega los campos de sistema."""
    id: int
    activo: bool
    model_config = ConfigDict(from_attributes=True)

class PacienteListDTO(BaseModel):
    """Versión optimizada para listados masivos."""
    id: int
    nombre: str
    especie: str
    activo: bool # Es útil saber si está activo en una lista
    model_config = ConfigDict(from_attributes=True)