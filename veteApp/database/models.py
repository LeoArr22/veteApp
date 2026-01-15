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

    dni = Column(String(20), nullable=False, unique=True)

    nombre = Column(String, nullable=False)
    telefono = Column(String)
    email = Column(String)
    direccion = Column(String)

    activo = Column(Boolean, default=True, nullable=False)

    pacientes = relationship(
        "Paciente",
        back_populates="dueno"
    )

    def __repr__(self):
        return (
            f"<Dueno(id={self.id}, dni='{self.dni}', "
            f"nombre='{self.nombre}', activo={self.activo})>"
        )



# ---------------------------------------------------------
# PACIENTE
# ---------------------------------------------------------
class Paciente(Base):
    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    especie = Column(String, nullable=False)
    raza = Column(String)
    sexo = Column(String)
    fecha_nacimiento = Column(Date)

    activo = Column(Boolean, default=True, nullable=False)

    dueno_id = Column(Integer, ForeignKey("duenos.id"), nullable=False)

    dueno = relationship(
        "Dueno",
        back_populates="pacientes"
    )

    consultas = relationship(
        "Consulta",
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

    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    matricula = Column(String, unique=True)
    activo = Column(Boolean, default=True, nullable=False)

    consultas = relationship(
        "Consulta",
        back_populates="veterinario"
    )

    def __repr__(self):
        return f"<Veterinario(id={self.id}, nombre='{self.nombre}', activo={self.activo})>"


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

    activo = Column(Boolean, default=True, nullable=False)

    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=False)
    veterinario_id = Column(Integer, ForeignKey("veterinarios.id"), nullable=False)

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
        back_populates="consulta"
    )

    tratamientos = relationship(
        "Tratamiento",
        back_populates="consulta"
    )

    def __repr__(self):
        return f"<Consulta(id={self.id}, fecha={self.fecha.date()}, activo={self.activo})>"


# ---------------------------------------------------------
# ARCHIVO CLÍNICO
# ---------------------------------------------------------
class ArchivoClinico(Base):
    __tablename__ = "archivos_clinicos"

    id = Column(Integer, primary_key=True)
    nombre_original = Column(String, nullable=False)
    ruta_archivo = Column(String, nullable=False)
    tipo = Column(String, nullable=False)

    fecha_subida = Column(DateTime, default=datetime.utcnow, nullable=False)

    activo = Column(Boolean, default=True, nullable=False)

    consulta_id = Column(Integer, ForeignKey("consultas.id"), nullable=False)

    consulta = relationship(
        "Consulta",
        back_populates="archivos"
    )

    def __repr__(self):
        return f"<ArchivoClinico(id={self.id}, nombre='{self.nombre_original}', activo={self.activo})>"


# ---------------------------------------------------------
# TRATAMIENTO
# ---------------------------------------------------------
class Tratamiento(Base):
    __tablename__ = "tratamientos"

    id = Column(Integer, primary_key=True)

    nombre = Column(String, nullable=False)
    dosis = Column(String, nullable=False)
    frecuencia = Column(String)
    duracion = Column(String)
    observaciones = Column(Text)

    fecha_inicio = Column(Date, nullable=False, default=date.today)
    fecha_fin = Column(Date)

    activo = Column(Boolean, default=True, nullable=False)

    consulta_id = Column(Integer, ForeignKey("consultas.id"), nullable=False)

    consulta = relationship(
        "Consulta",
        back_populates="tratamientos"
    )

    def __repr__(self):
        return (
            f"<Tratamiento(id={self.id}, nombre='{self.nombre}', "
            f"inicio={self.fecha_inicio}, fin={self.fecha_fin}, activo={self.activo})>"
        )

