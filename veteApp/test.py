import os
import time
from application.app.vet_app import VeterinariaApp
from application.dto.dueno_dto import DuenoCreateDTO
from application.dto.paciente_dto import PacienteCreateDTO
from application.dto.veterinario_dto import VeterinarioCreateDTO
from application.dto.consulta_dto import ConsultaCreateDTO
from application.dto.archivo_clinico_dto import ArchivoClinicoCreateDTO
from application.dto.tratamiento_dto import TratamientoCreateDTO
from database.init_db import init_db

def limpiar_base_de_datos():
    if os.path.exists("vete.db"):
        try:
            os.remove("vete.db")
            print("🗑️ Base de datos antigua eliminada.")
        except PermissionError:
            print("⚠️ No se pudo eliminar la DB porque está en uso.")

def probar_sistema():
    print("\n🚀 [1] PRUEBA DE INTEGRACIÓN: Registro Inicial")
    init_db()
    app = VeterinariaApp()
    
    try:
        # Registrar Dueños
        nuevo_dueno = DuenoCreateDTO(
            dni="12345678", nombre="Juan Perez", telefono="11223344",
            email="juan@mail.com", direccion="Calle Falsa 123"
        )
        nuevo_dueno2 = DuenoCreateDTO(
            dni="12245678", nombre="Marta Perez", telefono="11123344",
            email="marta@mail.com", direccion="Calle Falsa 123"
        )
        
        dueno1 = app.registrar_dueno(nuevo_dueno)
        dueno2 = app.registrar_dueno(nuevo_dueno2)
        print(f"✅ Dueños guardados: {dueno1.nombre} (ID: {dueno1.id}) y {dueno2.nombre}")

        # Registrar Mascota para Juan (ID 1)
        nueva_mascota = PacienteCreateDTO(
            nombre="Firulais", especie="Perro", raza="Labrador",
            sexo="Macho", dueno_id=dueno1.id
        )
        mascota = app.registrar_paciente(nueva_mascota)
        print(f"✅ Mascota guardada: {mascota.nombre} (Dueño ID: {mascota.dueno_id})")

        # Verificar lista
        pacientes = app.listar_pacientes_por_dueno(dueno1.id)
        if len(pacientes) > 0:
            print(f"✅ Verificación: Se encontró a {pacientes[0].nombre} en la DB.")

    except Exception as e:
        print(f"❌ ERROR EN PRUEBA 1: {e}")
    finally:
        app.cerrar()

def test_historial_completo():
    print("\n🚀 [2] TEST: Registro de Consulta")
    app = VeterinariaApp()
    try:
        # Registramos mascota para el Dueño 1
        nueva_mascota = PacienteCreateDTO(
            nombre="Luna", especie="Gato", raza="Siamés", sexo="Hembra", dueno_id=1
        )
        mascota = app.registrar_paciente(nueva_mascota)
        
        # Registramos consulta para Luna usando el Vet 1
        dto_consulta = ConsultaCreateDTO(
            paciente_id=mascota.id,
            veterinario_id=1,
            motivo="Chequeo anual",
            diagnostico="Sana",
            peso=3.5
        )
        consulta = app.registrar_consulta(dto_consulta)
        print(f"✅ Consulta registrada ID: {consulta.id} para {mascota.nombre}")
    finally:
        app.cerrar()

def test_archivos_y_consultas():
    print("\n🚀 [3] TEST: Adjuntar Estudios")
    app = VeterinariaApp()
    try:
        # Creamos consulta para Firulais (ID 1)
        dto_con = ConsultaCreateDTO(
            paciente_id=1, veterinario_id=1,
            motivo="Ingesta de objeto extraño",
            diagnostico="Obstrucción leve", peso=12.5
        )
        consulta = app.registrar_consulta(dto_con)

        # Adjuntar archivo (usando el nombre subir_archivo de tu App)
        dto_archivo = ArchivoClinicoCreateDTO(
            consulta_id=consulta.id,
            nombre_original="radiografia_x1.png",
            ruta_archivo="/uploads/radiografia_x1.png",
            tipo="Imagen"
        )
        archivo = app.adjuntar_archivo(dto_archivo)
        print(f"✅ Archivo '{archivo.nombre_original}' vinculado a Consulta #{consulta.id}")

        # Verificar
        archivos = app.listar_archivos_consulta(consulta.id)
        assert len(archivos) > 0
        print(f"✅ Éxito: La consulta tiene {len(archivos)} archivo(s).")
    finally:
        app.cerrar()

def test_tratamientos_multiples():
    print("\n🚀 [4] TEST: Tratamientos")
    app = VeterinariaApp()
    try:
        # Usamos la consulta anterior (ID 3 aproximadamente en este flujo)
        # Para asegurar, creamos una nueva
        dto_con = ConsultaCreateDTO(paciente_id=1, veterinario_id=1, motivo="Gripe", diagnostico="Virus", peso=10.0)
        consulta = app.registrar_consulta(dto_con)

        t1 = TratamientoCreateDTO(consulta_id=consulta.id, nombre="Antibiótico", dosis="1ml")
        t2 = TratamientoCreateDTO(consulta_id=consulta.id, nombre="Vitaminas", dosis="1 tableta")
        
        app.registrar_tratamiento(t1)
        app.registrar_tratamiento(t2)
        
        tratamientos = app.listar_tratamientos_consulta(consulta.id)
        print(f"✅ Consulta #{consulta.id} tiene {len(tratamientos)} tratamientos registrados.")
    finally:
        app.cerrar()

def test_historial_post_transferencia():
    print("\n🚀 [5] TEST: Transferencia de Mascota")
    app = VeterinariaApp()
    try:
        historial_antes = app.obtener_historial_clinico(1)
        cant_antes = len(historial_antes)
        
        # Transferimos a Firulais (1) a Marta (2)
        app.transferir_mascota(paciente_id=1, nuevo_dueno_id=2)
        
        historial_despues = app.obtener_historial_clinico(1)
        
        if len(historial_despues) == cant_antes:
            print(f"✅ Éxito: Firulais mantiene sus {cant_antes} consultas tras cambio de dueño.")
        else:
            print("❌ ERROR: Historial inconsistente.")
    finally:
        app.cerrar()

def test_carga_masiva_historial():
    print("\n🚀 [6] TEST: Carga Masiva")
    app = VeterinariaApp()
    try:
        inicio = time.time()
        for i in range(50):
            dto = ConsultaCreateDTO(
                paciente_id=1, veterinario_id=1, 
                motivo=f"Revisión #{i}", diagnostico="Sano", peso=10.5
            )
            app.registrar_consulta(dto)
        
        fin = time.time()
        historial = app.obtener_historial_clinico(1)
        print(f"✅ Éxito: 50 consultas en {fin - inicio:.2f}s. Total: {len(historial)} registros.")
    finally:
        app.cerrar()

if __name__ == "__main__":
    limpiar_base_de_datos()
    
    # 1. Flujo inicial
    probar_sistema()
    
    # 2. Setup Veterinario (Requerido para el resto de los tests)
    app_setup = VeterinariaApp()
    dto_vet = VeterinarioCreateDTO(
        nombre="Dr. Gomez", matricula="VET12345", 
        especialidad="Cardiologia", telefono="555-1234"
    )
    app_setup.registrar_veterinario(dto_vet)
    app_setup.cerrar()
    
    # 3. Ejecución de tests específicos
    test_historial_completo()
    test_archivos_y_consultas()
    test_tratamientos_multiples()
    test_historial_post_transferencia()
    test_carga_masiva_historial()
    
    print("\n✨ TODAS LAS PRUEBAS DE INTEGRACIÓN FINALIZADAS ✨")