# test_app.py
from application.app.vet_app import VeterinariaApp
from application.dto.dueno_dto import DuenoCreateDTO
from application.dto.paciente_dto import PacienteCreateDTO
from application.dto.veterinario_dto import VeterinarioCreateDTO
from database.init_db import init_db
import os

def limpiar_base_de_datos():
    if os.path.exists("vete.db"):
        os.remove("vete.db")
        print("🗑️ Base de datos antigua eliminada.")

def probar_sistema():
    print("🚀 Iniciando prueba de integración...")
    
    # 1. Inicializamos la base de datos (crea tablas si no existen)
    init_db()
    
    # 2. Instanciamos nuestra App Orquestadora
    app = VeterinariaApp()
    
    try:
        # --- PRUEBA 1: Registrar un Dueño ---
        print("\n1. Registrando dueño...")
        nuevo_dueno_data = DuenoCreateDTO(
            dni="12345678",
            nombre="Juan Perez",
            telefono="11223344",
            email="juan@mail.com",
            direccion="Calle Falsa 123"
        )
        print("\n1. Registrando dueño...")
        nuevo_dueno_data2 = DuenoCreateDTO(
            dni="12245678",
            nombre="Marta Perez",
            telefono="11123344",
            email="juan@mail.com",
            direccion="Calle Falsa 123"
        )
        dueno_guardado = app.registrar_dueno(nuevo_dueno_data)
        app.registrar_dueno(nuevo_dueno_data2)
        print(f"✅ Dueño guardado: {dueno_guardado.nombre} (ID: {dueno_guardado.id})")

        # --- PRUEBA 2: Registrar una Mascota para ese dueño ---
        print("\n2. Registrando mascota...")
        nueva_mascota_data = PacienteCreateDTO(
            nombre="Firulais",
            especie="Perro",
            raza="Labrador",
            sexo="Macho",
            dueno_id=dueno_guardado.id  # Usamos el ID que nos devolvió la DB
        )
        mascota_guardada = app.registrar_paciente(nueva_mascota_data)
        print(f"✅ Mascota guardada: {mascota_guardada.nombre} de {dueno_guardado.nombre}")

        # --- PRUEBA 3: Listar para verificar persistencia ---
        print("\n3. Verificando lista de pacientes...")
        pacientes = app.listar_pacientes_por_dueno(dueno_guardado.id)
        if len(pacientes) > 0:
            print(f"✅ Éxito: Se encontró a {pacientes[0].nombre} en la base de datos.")

    except Exception as e:
        print(f"❌ ERROR EN LA PRUEBA: {e}")
    
    finally:
        app.cerrar()
        print("\n🏁 Prueba finalizada.")
        
        
def test_historial_completo():
    app = VeterinariaApp()
    try:
        # 1. Usamos el dueño ID 1 que ya existe
        # 2. Registramos una nueva mascota para él
        print("\n--- Test: Registro de Consulta ---")
        nueva_mascota = PacienteCreateDTO(
            nombre="Luna", especie="Gato", raza="Siamés", sexo="Hembra", dueno_id=1
        )
        mascota = app.registrar_paciente(nueva_mascota)
        
        # 3. Registramos una consulta para Luna
        from application.dto.consulta_dto import ConsultaCreateDTO
        dto_consulta = ConsultaCreateDTO(
            paciente_id=mascota.id,
            veterinario_id=1, # Asegúrate de tener un vet ID 1 o créalo antes
            motivo="Chequeo anual",
            diagnostico="Sana",
            peso=3.5
        )
        consulta = app.registrar_consulta(dto_consulta)
        print(f"✅ Consulta registrada ID: {consulta.id} para {mascota.nombre}")
        
    finally:
        app.cerrar()
        
def test_archivos_y_consultas():
    app = VeterinariaApp()
    print("\n--- Test: Adjuntar Estudios a Consulta ---")
    try:
        # 1. Buscamos al paciente 1 (Firulais) y al vet 1
        # 2. Creamos una consulta de urgencia
        from application.dto.consulta_dto import ConsultaCreateDTO
        from application.dto.archivo_clinico_dto import ArchivoClinicoCreateDTO

        dto_con = ConsultaCreateDTO(
            paciente_id=1, veterinario_id=1,
            motivo="Ingesta de objeto extraño",
            diagnostico="Obstrucción leve", peso=12.5
        )
        consulta = app.registrar_consulta(dto_con)

        # 3. Adjuntamos una "Radiografía"
        dto_archivo = ArchivoClinicoCreateDTO(
            consulta_id=consulta.id,
            nombre_original="radiografia_x1.png",
            ruta_archivo="/uploads/radiografia_x1.png",
            tipo="Imagen"
        )
        archivo = app.adjuntar_archivo(dto_archivo)
        print(f"✅ Archivo '{archivo.nombre_original}' vinculado a Consulta #{consulta.id}")

        # 4. Verificamos que la consulta tenga sus archivos
        archivos = app.listar_archivos_consulta(consulta.id)
        assert len(archivos) > 0
        print(f"✅ Verificación exitosa: La consulta tiene {len(archivos)} archivo(s).")

    finally:
        app.cerrar()

def test_tratamientos_multiples():
    app = VeterinariaApp()
    print("\n--- Test: Tratamientos en Cascada ---")
    try:
        from application.dto.tratamiento_dto import TratamientoCreateDTO
        
        # 1. Usamos la consulta #2 que acabamos de crear
        t1 = TratamientoCreateDTO(consulta_id=2, nombre="Vacuna Antirrábica", dosis="1ml")
        t2 = TratamientoCreateDTO(consulta_id=2, nombre="Desparasitación", dosis="1 tableta")
        
        app.registrar_tratamiento(t1)
        app.registrar_tratamiento(t2)
        
        # 2. Verificamos
        tratamientos = app.listar_tratamientos_consulta(2)
        print(f"✅ Consulta #2 tiene {len(tratamientos)} tratamientos registrados.")
        for t in tratamientos:
            print(f"   - {t.nombre} ({t.dosis})")
            
    finally:
        app.cerrar()

def test_historial_post_transferencia():
    app = VeterinariaApp()
    print("\n--- Test: Persistencia de Historial tras Transferencia ---")
    try:
        # 1. Verificamos cuántas consultas tiene Firulais (ID 1) bajo el Dueño 1
        historial_antes = app.obtener_historial_clinico(1)
        cant_antes = len(historial_antes)
        
        # 2. Transferimos a Firulais al Dueño 2 (Marta)
        app.transferir_mascota(paciente_id=1, nuevo_dueno_id=2)
        
        # 3. Verificamos el historial otra vez
        historial_despues = app.obtener_historial_clinico(1)
        
        if len(historial_despues) == cant_antes:
            print(f"✅ Éxito: Firulais mantiene sus {cant_antes} consultas a pesar del cambio de dueño.")
        else:
            print("❌ ERROR: Se perdió información en la transferencia.")
    finally:
        app.cerrar()
        
def test_carga_masiva_historial():
    app = VeterinariaApp()
    print("\n--- Test de Carga Masiva: 50 Consultas ---")
    try:
        from application.dto.consulta_dto import ConsultaCreateDTO
        import time

        inicio = time.time()
        for i in range(50):
            dto = ConsultaCreateDTO(
                paciente_id=1, 
                veterinario_id=1, 
                motivo=f"Revisión de rutina #{i}", 
                diagnostico="Sano", 
                peso=10.5 + i
            )
            app.registrar_consulta(dto)
        
        fin = time.time()
        historial = app.obtener_historial_clinico(1)
        
        print(f"✅ Éxito: Se registraron 50 consultas en {fin - inicio:.2f} segundos.")
        print(f"Total en historial: {len(historial)} registros.")
        
    finally:
        app.cerrar()

if __name__ == "__main__":
    limpiar_base_de_datos()
    probar_sistema()
    app = VeterinariaApp()
    from application.dto.consulta_dto import ConsultaCreateDTO
    dto_veterinario= VeterinarioCreateDTO(
            nombre ="Dr. Gomez", matricula ="VET12345", especialidad ="Cardiologia", telefono ="555-1234"
        )
    app.registrar_veterinario(dto_veterinario)
    test_historial_completo()
    test_archivos_y_consultas()
    test_tratamientos_multiples()
    test_historial_post_transferencia()
    test_carga_masiva_historial()