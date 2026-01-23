# test_app.py
from application.app.vet_app import VeterinariaApp
from application.dto.dueno_dto import DuenoCreateDTO
from application.dto.paciente_dto import PacienteCreateDTO
from database.init_db import init_db

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
        dueno_guardado = app.registrar_dueno(nuevo_dueno_data)
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

if __name__ == "__main__":
    probar_sistema()