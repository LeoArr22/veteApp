from datetime import datetime, date, timezone
from sqlalchemy import String, Text, ForeignKey, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

# 1. Definición de la Base Moderna
class Base(DeclarativeBase):
    pass

# ---------------------------------------------------------
# DUEÑO
# ---------------------------------------------------------
class Dueno(Base):
    __tablename__ = "duenos"

    id: Mapped[int] = mapped_column(primary_key=True)
    dni: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    nombre: Mapped[str] = mapped_column(nullable=False)
    telefono: Mapped[str | None]
    email: Mapped[str | None]
    direccion: Mapped[str | None]
    activo: Mapped[bool] = mapped_column(default=True)

    # Relaciones
    pacientes: Mapped[list["Paciente"]] = relationship(back_populates="dueno")

    def __repr__(self):
        return f"<Dueno(id={self.id}, dni='{self.dni}', nombre='{self.nombre}', activo={self.activo})>"


# ---------------------------------------------------------
# PACIENTE
# ---------------------------------------------------------
class Paciente(Base):
    __tablename__ = "pacientes"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(nullable=False)
    especie: Mapped[str] = mapped_column(nullable=False)
    raza: Mapped[str | None]
    sexo: Mapped[str | None]
    fecha_nacimiento: Mapped[date | None]
    activo: Mapped[bool] = mapped_column(default=True)

    dueno_id: Mapped[int] = mapped_column(ForeignKey("duenos.id"), nullable=False)

    # Relaciones
    dueno: Mapped["Dueno"] = relationship(back_populates="pacientes")
    consultas: Mapped[list["Consulta"]] = relationship(
        back_populates="paciente",
        order_by="Consulta.fecha"
    )

    def __repr__(self):
        return f"<Paciente(id={self.id}, nombre='{self.nombre}', activo={self.activo})>"


# ---------------------------------------------------------
# VETERINARIO
# ---------------------------------------------------------
class Veterinario(Base):
    __tablename__ = "veterinarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(nullable=False)
    matricula: Mapped[str | None] = mapped_column(unique=True)
    especialidad: Mapped[str | None]
    telefono: Mapped[str | None]
    activo: Mapped[bool] = mapped_column(default=True)

    # Relaciones
    consultas: Mapped[list["Consulta"]] = relationship(back_populates="veterinario")

    def __repr__(self):
        return f"<Veterinario(id={self.id}, nombre='{self.nombre}', activo={self.activo})>"


# ---------------------------------------------------------
# CONSULTA
# ---------------------------------------------------------
class Consulta(Base):
    __tablename__ = "consultas"

    id: Mapped[int] = mapped_column(primary_key=True)
    
    # Usamos func.now() para que la DB ponga la hora
    fecha: Mapped[datetime] = mapped_column(server_default=func.now())

    motivo: Mapped[str] = mapped_column(nullable=False)
    diagnostico: Mapped[str | None] = mapped_column(Text)
    peso: Mapped[float | None] = mapped_column(nullable=True)
    observaciones: Mapped[str | None] = mapped_column(Text)
    activo: Mapped[bool] = mapped_column(default=True)

    paciente_id: Mapped[int] = mapped_column(ForeignKey("pacientes.id"), nullable=False)
    veterinario_id: Mapped[int] = mapped_column(ForeignKey("veterinarios.id"), nullable=False)

    # Relaciones
    paciente: Mapped["Paciente"] = relationship(back_populates="consultas")
    veterinario: Mapped["Veterinario"] = relationship(back_populates="consultas")
    archivos: Mapped[list["ArchivoClinico"]] = relationship(back_populates="consulta")
    tratamientos: Mapped[list["Tratamiento"]] = relationship(back_populates="consulta")

    def __repr__(self):
        # Usamos .date() solo para el repr para que sea más legible
        return f"<Consulta(id={self.id}, motivo='{self.motivo[:20]}...', activo={self.activo})>"


# ---------------------------------------------------------
# ARCHIVO CLÍNICO
# ---------------------------------------------------------
class ArchivoClinico(Base):
    __tablename__ = "archivos_clinicos"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre_original: Mapped[str]
    ruta_archivo: Mapped[str]
    tipo: Mapped[str]
    fecha_subida: Mapped[datetime] = mapped_column(server_default=func.now())
    activo: Mapped[bool] = mapped_column(default=True)

    consulta_id: Mapped[int] = mapped_column(ForeignKey("consultas.id"), nullable=False)

    # Relaciones
    consulta: Mapped["Consulta"] = relationship(back_populates="archivos")

    def __repr__(self):
        return f"<ArchivoClinico(id={self.id}, nombre='{self.nombre_original}')>"


# ---------------------------------------------------------
# TRATAMIENTO
# ---------------------------------------------------------
class Tratamiento(Base):
    __tablename__ = "tratamientos"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str]
    dosis: Mapped[str]
    frecuencia: Mapped[str | None]
    duracion: Mapped[str | None]
    observaciones: Mapped[str | None] = mapped_column(Text)

    fecha_inicio: Mapped[date] = mapped_column(default=date.today)
    fecha_fin: Mapped[date | None]
    activo: Mapped[bool] = mapped_column(default=True)

    consulta_id: Mapped[int] = mapped_column(ForeignKey("consultas.id"), nullable=False)

    # Relaciones
    consulta: Mapped["Consulta"] = relationship(back_populates="tratamientos")

    def __repr__(self):
        return f"<Tratamiento(id={self.id}, nombre='{self.nombre}', inicio={self.fecha_inicio})>"