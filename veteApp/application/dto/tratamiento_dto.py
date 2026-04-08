from datetime import date
from pydantic import BaseModel, ConfigDict, Field

# =========================================================
# DTOs DE ENTRADA
# =========================================================

class TratamientoCreateDTO(BaseModel):
    consulta_id: int
    nombre: str = Field(..., min_length=2, max_length=100)
    dosis: str = Field(..., min_length=1, max_length=100)
    frecuencia: str | None = Field(default=None, max_length=100)
    duracion: str | None = Field(default=None, max_length=100)
    # Opciones al final
    observaciones: str | None = Field(default=None)
    fecha_inicio: date | None = Field(default=None)
    fecha_fin: date | None = Field(default=None)

class TratamientoFinalizarDTO(BaseModel):
    """Específico para marcar el fin de un tratamiento."""
    fecha_fin: date

# =========================================================
# DTOs DE SALIDA
# =========================================================

class TratamientoReadDTO(TratamientoCreateDTO):
    """
    Representación completa de un tratamiento.
    Hereda todas las validaciones de CreateDTO.
    """
    id: int
    activo: bool
    
    model_config = ConfigDict(from_attributes=True)

class TratamientoListDTO(BaseModel):
    """Resumen para listados rápidos."""
    id: int
    nombre: str
    activo: bool
    
    model_config = ConfigDict(from_attributes=True)