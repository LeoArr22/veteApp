# application/dto/consulta_dto.py

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


# =========================================================
# DTOs DE ENTRADA
# =========================================================

class ConsultaCreateDTO(BaseModel):
    paciente_id: int
    veterinario_id: int
    motivo: str = Field(..., min_length=3, max_length=200)
    diagnostico: str
    # Opcionales al final
    peso: float | None = Field(default=None, ge=0)
    observaciones: str | None = Field(default=None)



# =========================================================
# DTOs DE SALIDA
# =========================================================

class ConsultaReadDTO(ConsultaCreateDTO):
    id: int
    fecha: datetime
    model_config = ConfigDict(from_attributes=True)
    
class ConsultaListDTO(BaseModel):
    id: int
    fecha: datetime
    motivo: str
    model_config = ConfigDict(from_attributes=True)