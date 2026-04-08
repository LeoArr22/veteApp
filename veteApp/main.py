from fastapi import FastAPI, HTTPException
from typing import List

# --- Infraestructura de Base de Datos ---
from database.connection import engine
from database.models import Base 

# --- Tu Lógica de Negocio Real ---
from application.app.vet_app import VeterinariaApp 

# --- DTOs (Asegurate que estos nombres de archivo existan en application/dto/) ---
from application.dto.dueno_dto import DuenoCreateDTO
from application.dto.paciente_dto import PacienteCreateDTO
from application.dto.veterinario_dto import VeterinarioCreateDTO
from application.dto.consulta_dto import ConsultaCreateDTO

# Inicialización automática de tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistema Veterinaria API",
    description="Backend conectado a VeterinariaApp",
    version="1.3.0"
)

# Instancia única de tu lógica
vet_system = VeterinariaApp()

@app.get("/", tags=["Inicio"])
def read_root():
    return {"status": "Online", "mensaje": "Conectado a VeterinariaApp"}

# --- DUEÑOS ---
@app.post("/duenos", tags=["Dueños"])
def registrar_dueno(dto: DuenoCreateDTO):
    try:
        return vet_system.registrar_dueno(dto)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/duenos", tags=["Dueños"])
def listar_duenos(solo_activos: bool = True):
    # Usamos tu método: listar_duenos(self.db, solo_activos)
    return vet_system.listar_duenos(solo_activos)

# --- PACIENTES ---
@app.post("/pacientes", tags=["Pacientes"])
def registrar_paciente(dto: PacienteCreateDTO):
    try:
        return vet_system.registrar_paciente(dto)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# --- VETERINARIOS ---
@app.post("/veterinarios", tags=["Veterinarios"])
def registrar_veterinario(dto: VeterinarioCreateDTO):
    try:
        return vet_system.registrar_veterinario(dto)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/veterinarios", tags=["Veterinarios"])
def listar_veterinarios(solo_activos: bool = True):
    return vet_system.listar_veterinarios(solo_activos)

# --- CONSULTAS Y HISTORIAL ---
@app.post("/consultas", tags=["Consultas Médicas"])
def registrar_consulta(dto: ConsultaCreateDTO):
    try:
        return vet_system.registrar_consulta(dto)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/pacientes/{paciente_id}/historial", tags=["Historial Clínico"])
def obtener_historial(paciente_id: int):
    """Llama a tu método obtener_historial_clinico"""
    try:
        historial = vet_system.obtener_historial_clinico(paciente_id)
        if not historial:
            return {"mensaje": "Sin historial para este paciente"}
        return historial
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))