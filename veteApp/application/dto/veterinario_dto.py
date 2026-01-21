# application/dto/veterinario_dto.py

from pydantic import BaseModel, Field


# =========================================================
# DTOs DE ENTRADA
# =========================================================

class VeterinarioCreateDTO(BaseModel):
    """
    Datos necesarios para crear un veterinario.
    """

    nombre: str = Field(..., min_length=2, max_length=100)
    matricula: str = Field(..., min_length=3, max_length=50)


class VeterinarioUpdateDTO(BaseModel):
    """
    Datos modificables de un veterinario.
    Todos son opcionales.
    """

    nombre: str | None = Field(None, min_length=2, max_length=100)
    matricula: str | None = Field(None, min_length=3, max_length=50)


# =========================================================
# DTOs DE SALIDA
# =========================================================

class VeterinarioReadDTO(BaseModel):
    """
    Representación completa de un veterinario.
    """

    id: int
    nombre: str
    matricula: str
    activo: bool


class VeterinarioListDTO(BaseModel):
    """
    Representación reducida para listados.
    """

    id: int
    nombre: str
    matricula: str
