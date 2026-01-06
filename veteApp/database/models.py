from datetime import datetime, date

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Date,
    DateTime,
    Boolean,
    ForeignKey
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


# ---------------------------------------------------------
# DUEÑO
# ---------------------------------------------------------
class Dueno(Base):
    __tablename__ = "duenos"

    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    telefono = Column(String)
    email = Column(String)
    direccion = Column(String)

    pacientes = relationship(
        "Paciente",
        back_populates="dueno",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Dueno(id={self.id}, nombre='{self.nombre}')>"


# ---------------------------------------------------------
# PACIENTE (MASCOTA)
# ---------------------------------------------------------
class Paciente(Base):
    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    especie = Column(String, nullable=False)      # gato, perro
    raza = Column(String)
    sexo = Column(String)                         # macho / hembra
    fecha_nacimiento = Column(Date)

    dueno_id = Column(Integer, ForeignKey("duenos.id"), nullable=False)

    dueno = relationship(
        "Dueno",
        back_populates="pacientes"
    )

    consultas = relationship(
        "Consulta",
        back_populates="paciente",
        cascade="all, delete-orphan",
        order_by="Consulta.fecha"
    )

    def __repr__(self):
        return (
            f"<Paciente(id={self.id}, nombre='{self.nombre}', "
            f"especie='{self.especie}')>"
        )


# ---------------------------------------------------------
# VETERINARIO
# ---------------------------------------------------------
class Veterinario(Base):
    __tablename__ = "veterinarios"

    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    matricula = Column(String, unique=True)
    activo = Column(Boolean, default=True)

    consultas = relationship(
        "Consulta",
        back_populates="veterinario"
    )

    def __repr__(self):
        return f"<Veterinario(id={self.id}, nombre='{self.nombre}')>"


# ---------------------------------------------------------
# CONSULTA
# ---------------------------------------------------------
class Consulta(Base):
    __tablename__ = "consultas"

    id = Column(Integer, primary_key=True)
    fecha = Column(DateTime, default=datetime.utcnow, nullable=False)

    motivo = Column(String, nullable=False)
    diagnostico = Column(Text)
    observaciones = Column(Text)

    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=False)
    veterinario_id = Column(Integer, ForeignKey("veterinarios.id"))

    paciente = relationship(
        "Paciente",
        back_populates="consultas"
    )

    veterinario = relationship(
        "Veterinario",
        back_populates="consultas"
    )

    archivos = relationship(
        "ArchivoClinico",
        back_populates="consulta",
        cascade="all, delete-orphan"
    )

    medicamentos = relationship(
        "Medicacion",
        back_populates="consulta",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return (
            f"<Consulta(id={self.id}, fecha={self.fecha.date()}, "
            f"motivo='{self.motivo}')>"
        )


# ---------------------------------------------------------
# ARCHIVO CLÍNICO
# ---------------------------------------------------------
class ArchivoClinico(Base):
    __tablename__ = "archivos_clinicos"

    id = Column(Integer, primary_key=True)
    nombre_original = Column(String, nullable=False)
    ruta_archivo = Column(String, nullable=False)

    tipo = Column(String, nullable=False)
    # imagen, radiografia, estudio, analisis, pdf

    fecha_subida = Column(DateTime, default=datetime.utcnow, nullable=False)
    existe = Column(Boolean, default=True)

    consulta_id = Column(
        Integer,
        ForeignKey("consultas.id"),
        nullable=False
    )

    consulta = relationship(
        "Consulta",
        back_populates="archivos"
    )

    def __repr__(self):
        return (
            f"<ArchivoClinico(id={self.id}, "
            f"nombre='{self.nombre_original}', tipo='{self.tipo}')>"
        )


# ---------------------------------------------------------
# MEDICACIÓN RECETADA
# ---------------------------------------------------------
class Medicacion(Base):
    __tablename__ = "medicaciones"

    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    dosis = Column(String, nullable=False)
    frecuencia = Column(String)
    duracion = Column(String)
    observaciones = Column(Text)

    consulta_id = Column(
        Integer,
        ForeignKey("consultas.id"),
        nullable=False
    )

    consulta = relationship(
        "Consulta",
        back_populates="medicamentos"
    )

    def __repr__(self):
        return (
            f"<Medicacion(id={self.id}, nombre='{self.nombre}', "
            f"dosis='{self.dosis}')>"
        )
