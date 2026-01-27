# application/app/vet_app.py

from sqlalchemy.orm import Session
from database.connection import SessionLocal

# Importación de todos los servicios
from services import (
    dueno_service,
    paciente_service,
    veterinario_service,
    consulta_service,
    tratamiento_service,
    archivo_clinico_service
)

class VeterinariaApp:
    def __init__(self):
        """Inicia la sesión principal que usará la interfaz gráfica."""
        self.db: Session = SessionLocal()

    # =========================================================
    # MÓDULO: DUEÑOS
    # =========================================================
    def registrar_dueno(self, dto):
        try:
            res = dueno_service.crear_dueno_service(self.db, dto)
            self.db.commit()
            return res
        except Exception as e:
            self.db.rollback()
            raise e

    def actualizar_dueno(self, dueno_id: int, dto):
        try:
            res = dueno_service.actualizar_dueno_service(self.db, dueno_id, dto)
            self.db.commit()
            return res
        except Exception as e:
            self.db.rollback()
            raise e

    def obtener_dueno(self, dueno_id: int):
        return dueno_service.obtener_dueno_por_id_service(self.db, dueno_id)

    def listar_duenos(self, solo_activos: bool = True):
        return dueno_service.listar_duenos_service(self.db, solo_activos)

    def cambiar_estado_dueno(self, dueno_id: int, activo: bool):
        try:
            if activo:
                res = dueno_service.reactivar_dueno_service(self.db, dueno_id)
            else:
                res = dueno_service.desactivar_dueno_service(self.db, dueno_id)
            self.db.commit()
            return res
        except Exception as e:
            self.db.rollback()
            raise e

    # =========================================================
    # MÓDULO: PACIENTES (MASCOTAS)
    # =========================================================
    def registrar_paciente(self, dto):
        try:
            res = paciente_service.crear_paciente_service(self.db, dto)
            self.db.commit()
            return res
        except Exception as e:
            self.db.rollback()
            raise e

    def actualizar_paciente(self, paciente_id: int, dto):
        try:
            res = paciente_service.actualizar_paciente_service(self.db, paciente_id, dto)
            self.db.commit()
            return res
        except Exception as e:
            self.db.rollback()
            raise e

    def obtener_paciente(self, paciente_id: int):
        return paciente_service.obtener_paciente_por_id_service(self.db, paciente_id)

    def listar_pacientes_por_dueno(self, dueno_id: int, solo_activos: bool = True):
        return paciente_service.listar_pacientes_por_dueno_service(self.db, dueno_id, solo_activos)

    def transferir_mascota(self, paciente_id: int, nuevo_dueno_id: int):
        try:
            res = paciente_service.transferir_paciente_service(self.db, paciente_id, nuevo_dueno_id)
            self.db.commit()
            return res
        except Exception as e:
            self.db.rollback()
            raise e

    

    # =========================================================
    # MÓDULO: VETERINARIOS
    # =========================================================
    def registrar_veterinario(self, dto):
        try:
            res = veterinario_service.crear_veterinario_service(self.db, dto)
            self.db.commit()
            return res
        except Exception as e:
            self.db.rollback()
            raise e

    def obtener_veterinario(self, veterinario_id: int):
        return veterinario_service.obtener_veterinario_service(self.db, veterinario_id)

    def listar_veterinarios(self, solo_activos: bool = True):
        return veterinario_service.listar_veterinarios_service(self.db, solo_activos)

    # =========================================================
    # MÓDULO: CONSULTAS E HISTORIAL
    # =========================================================
    def registrar_consulta(self, dto):
        try:
            res = consulta_service.crear_consulta_service(self.db, dto)
            self.db.commit()
            return res
        except Exception as e:
            self.db.rollback()
            raise e

    def obtener_consulta(self, consulta_id: int):
        return consulta_service.obtener_consulta_service(self.db, consulta_id)

    def obtener_historial_clinico(self, paciente_id: int):
        """Devuelve todas las consultas de una mascota."""
        return consulta_service.obtener_historial_service(self.db, paciente_id)

    def anular_consulta(self, consulta_id: int):
        try:
            consulta_service.anular_consulta_service(self.db, consulta_id)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e

    # =========================================================
    # MÓDULO: TRATAMIENTOS
    # =========================================================
    def registrar_tratamiento(self, dto):
        try:
            res = tratamiento_service.agregar_tratamiento_service(self.db, dto)
            self.db.commit()
            return res
        except Exception as e:
            self.db.rollback()
            raise e

    def finalizar_tratamiento(self, tratamiento_id: int, dto):
        try:
            res = tratamiento_service.finalizar_tratamiento_service(self.db, tratamiento_id, dto)
            self.db.commit()
            return res
        except Exception as e:
            self.db.rollback()
            raise e

    def listar_tratamientos_consulta(self, consulta_id: int):
        return tratamiento_service.listar_tratamientos_por_consulta_service(self.db, consulta_id)

    # =========================================================
    # MÓDULO: ARCHIVOS ADJUNTOS
    # =========================================================
    def adjuntar_archivo(self, dto):
        try:
            res = archivo_clinico_service.subir_archivo_clinico_service(self.db, dto)
            self.db.commit()
            return res
        except Exception as e:
            self.db.rollback()
            raise e

    def listar_archivos_consulta(self, consulta_id: int):
        return archivo_clinico_service.listar_archivos_consulta_service(self.db, consulta_id)

    # =========================================================
    # CONTROL DE SESIÓN
    # =========================================================
    def cerrar(self):
        """Cierra la conexión. Llamar al cerrar la ventana principal."""
        self.db.close()