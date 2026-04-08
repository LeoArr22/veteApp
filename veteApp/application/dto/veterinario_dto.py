from pydantic import BaseModel, Field, ConfigDict

class VeterinarioCreateDTO(BaseModel):
    """Datos obligatorios para registrar un veterinario nuevo."""
    nombre: str = Field(..., min_length=2, max_length=100)
    matricula: str = Field(..., min_length=3, max_length=50)    
    # Opcionales al final
    especialidad: str | None = Field(default=None, max_length=100)
    telefono: str | None = Field(default=None, max_length=20)

class VeterinarioUpdateDTO(BaseModel):
    """
    Datos modificables de un veterinario.
    Se usan tipos opcionales para permitir actualizaciones parciales.
    """
    nombre: str | None = Field(None, min_length=2, max_length=100)
    matricula: str | None = Field(None, min_length=3, max_length=50)
    especialidad: str | None = Field(None, max_length=100)
    telefono: str | None = Field(None, max_length=20)

class VeterinarioReadDTO(VeterinarioCreateDTO):
    """
    Representación completa que hereda las validaciones de CreateDTO 
    y suma los campos generados por el sistema.
    """
    id: int
    activo: bool

    model_config = ConfigDict(from_attributes=True)