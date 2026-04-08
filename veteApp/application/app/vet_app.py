from database.connection import SessionLocal
from services.dueno_service import DuenoService
from services.paciente_service import PacienteService
from services.veterinario_service import VeterinarioService
from services.consulta_service import ConsultaService
from services.tratamiento_service import TratamientoService
from services.archivo_clinico_service import ArchivoClinicoService

class VeterinariaApp:
    def __init__(self):
        self.db = SessionLocal()
        self.dueno_s = DuenoService()
        self.paciente_s = PacienteService()
        self.vet_s = VeterinarioService()
        self.consulta_s = ConsultaService()
        self.tratamiento_s = TratamientoService()
        self.archivo_s = ArchivoClinicoService()

    def _save(self, result):
        """Método interno para persistir cambios de forma segura."""
        try:
            self.db.commit()
            return result
        except Exception as e:
            self.db.rollback()
            raise e

    # =========================================================
    # VETERINARIOS
    # =========================================================
    def registrar_veterinario(self, dto):
        return self._save(self.vet_s.registrar_profesional(self.db, dto))

    def obtener_veterinario(self, vet_id: int):
        return self.vet_s.obtener_por_id(self.db, vet_id)

    def listar_veterinarios(self, solo_activos: bool = True):
        return self.vet_s.listar_profesionales(self.db, solo_activos)

    def actualizar_veterinario(self, vet_id: int, dto):
        return self._save(self.vet_s.actualizar_datos(self.db, vet_id, dto))

    def cambiar_estado_veterinario(self, vet_id: int, activo: bool):
        return self._save(self.vet_s.cambiar_disponibilidad(self.db, vet_id, activo))

    # =========================================================
    # DUEÑOS
    # =========================================================
    def registrar_dueno(self, dto):
        return self._save(self.dueno_s.registrar_dueno(self.db, dto))

    def obtener_dueno(self, dueno_id: int):
        return self.dueno_s.obtener_por_id(self.db, dueno_id)

    def listar_duenos(self, solo_activos: bool = True):
        return self.dueno_s.listar(self.db, solo_activos)

    def actualizar_dueno(self, dueno_id: int, dto):
        return self._save(self.dueno_s.actualizar_datos(self.db, dueno_id, dto))

    def cambiar_estado_dueno(self, dueno_id: int, activo: bool):
        return self._save(self.dueno_s.cambiar_disponibilidad(self.db, dueno_id, activo))

    # =========================================================
    # PACIENTES (MASCOTAS)
    # =========================================================
    def registrar_paciente(self, dto):
        return self._save(self.paciente_s.registrar_paciente(self.db, dto))
    
    def obtener_paciente(self, paciente_id: int):
        return self.paciente_s.obtener_por_id(self.db, paciente_id)

    def listar_pacientes_por_dueno(self, dueno_id: int, solo_activos: bool = True):
        return self.paciente_s.listar_por_dueno(self.db, dueno_id, solo_activos)

    def actualizar_paciente(self, paciente_id: int, dto):
        return self._save(self.paciente_s.actualizar_datos(self.db, paciente_id, dto))

    def cambiar_estado_paciente(self, paciente_id: int, activo: bool):
        return self._save(self.paciente_s.cambiar_disponibilidad(self.db, paciente_id, activo))

    def transferir_mascota(self, paciente_id: int, nuevo_dueno_id: int):
        return self._save(self.paciente_s.transferir_titularidad(self.db, paciente_id, nuevo_dueno_id))

    # =========================================================
    # CONSULTAS MÉDICAS
    # =========================================================
    def registrar_consulta(self, dto):
        return self._save(self.consulta_s.registrar_consulta(self.db, dto))
    
    def obtener_consulta_detalle(self, consulta_id: int):
        return self.consulta_s.obtener_detalle(self.db, consulta_id)

    def obtener_historial_clinico(self, paciente_id: int):
        return self.consulta_s.obtener_historial_paciente(self.db, paciente_id)

    def cambiar_estado_consulta(self, consulta_id: int, activo: bool):
        return self._save(self.consulta_s.cambiar_disponibilidad(self.db, consulta_id, activo))

    # =========================================================
    # TRATAMIENTOS
    # =========================================================
    def registrar_tratamiento(self, dto):
        return self._save(self.tratamiento_s.agregar_tratamiento(self.db, dto))
    
    def finalizar_tratamiento(self, tratamiento_id: int, dto):
        return self._save(self.tratamiento_s.finalizar_tratamiento(self.db, tratamiento_id, dto))

    def listar_tratamientos_consulta(self, consulta_id: int):
        return self.tratamiento_s.listar_por_consulta(self.db, consulta_id)

    def cambiar_estado_tratamiento(self, tratamiento_id: int, activo: bool):
        return self._save(self.tratamiento_s.cambiar_disponibilidad(self.db, tratamiento_id, activo))

    # =========================================================
    # ARCHIVOS Y ADJUNTOS
    # =========================================================
    def adjuntar_archivo(self, dto):
        return self._save(self.archivo_s.subir_archivo(self.db, dto))
    
    def listar_archivos_consulta(self, consulta_id: int):
        return self.archivo_s.listar_por_consulta(self.db, consulta_id)

    def cambiar_estado_archivo(self, archivo_id: int, activo: bool):
        return self._save(self.archivo_s.cambiar_disponibilidad(self.db, archivo_id, activo))


    def cerrar(self):
        self.db.close()