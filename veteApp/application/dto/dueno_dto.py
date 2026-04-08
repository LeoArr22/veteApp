# application/dto/dueno_dto.py

from pydantic import BaseModel, ConfigDict, Field


# =========================================================
# DTOs DE ENTRADA
# =========================================================

class DuenoCreateDTO(BaseModel):
    """
    Datos necesarios para crear un dueño.
    """
    dni: str = Field(..., min_length=7, max_length=15)
    nombre: str = Field(..., min_length=2, max_length=100)
    # Opcionales al final
    telefono: str | None = Field(default=None, max_length=50)
    email: str | None = Field(default=None, max_length=100)
    direccion: str | None = Field(default=None, max_length=150)


class DuenoUpdateDTO(BaseModel):
    """
    Datos modificables del dueño.
    No incluye DNI.
    """

    nombre: str | None = Field(None, min_length=2, max_length=100)
    telefono: str | None = Field(None, max_length=50)
    email: str | None = Field(None, max_length=100)
    direccion: str | None = Field(None, max_length=150)


class DuenoActualizarDniDTO(BaseModel):
    """
    Caso de uso excepcional: corrección de DNI.
    """

    nuevo_dni: str = Field(..., min_length=7, max_length=15)


# =========================================================
# DTOs DE SALIDA
# =========================================================

class DuenoReadDTO(DuenoCreateDTO):
    """
    Representación completa de un dueño, heredando de CreateDTO.
    """
    id: int
    activo: bool

    model_config = ConfigDict(from_attributes=True)

class DuenoListDTO(BaseModel):
    """
    Representación reducida para listados.
    """

    id: int
    dni: str
    nombre: str
    model_config = ConfigDict(from_attributes=True)