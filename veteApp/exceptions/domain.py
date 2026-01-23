# exceptions/domain.py

class DomainError(Exception):
    """Error base de dominio para toda la aplicación."""
    def __init__(self, message="Error de dominio"):
        self.message = message
        super().__init__(self.message)


# ---------------------------------------------------------
# DUEÑOS
# ---------------------------------------------------------
class DuenoNotFoundError(DomainError):
    def __init__(self, message="El dueño solicitado no existe o está inactivo"):
        super().__init__(message)

class DuenoAlreadyExistsError(DomainError):
    def __init__(self, message="Ya existe un dueño registrado con ese DNI"):
        super().__init__(message)

class DuenoConditionError(DomainError):
    """Regla de negocio: ej. No se puede desactivar un dueño con mascotas activas."""
    def __init__(self, message="No se puede realizar la operación por condiciones del dueño"):
        super().__init__(message)

class DuenoWithNoPacientesError(DomainError):
    def __init__(self, message="El dueño no tiene pacientes asociados"):
        super().__init__(message)


# ---------------------------------------------------------
# PACIENTES (MASCOTAS)
# ---------------------------------------------------------
class PacienteNotFoundError(DomainError):
    def __init__(self, message="El paciente solicitado no fue encontrado"):
        super().__init__(message)

class PacienteInactiveError(DomainError):
    def __init__(self, message="La mascota se encuentra inactiva en el sistema"):
        super().__init__(message)

class PacienteDoesNotBelongToDuenoError(DomainError):
    def __init__(self, message="El paciente no pertenece al dueño indicado"):
        super().__init__(message)


# ---------------------------------------------------------
# VETERINARIOS
# ---------------------------------------------------------
class VeterinarioNotFoundError(DomainError):
    def __init__(self, message="El profesional no fue encontrado"):
        super().__init__(message)

class VeterinarioInactiveError(DomainError):
    def __init__(self, message="El veterinario se encuentra inactivo"):
        super().__init__(message)

class VeterinarioAlreadyExistsError(DomainError):
    def __init__(self, message="La matrícula profesional ya se encuentra registrada"):
        super().__init__(message)


# ---------------------------------------------------------
# CONSULTAS (ACTOS MÉDICOS)
# ---------------------------------------------------------
class ConsultaNotFoundError(DomainError):
    def __init__(self, message="La consulta médica no existe o fue anulada"):
        super().__init__(message)

class ConsultaDoesNotBelongToPacienteError(DomainError):
    def __init__(self, message="La consulta no corresponde al historial de este paciente"):
        super().__init__(message)

class ConsultaClosedError(DomainError):
    def __init__(self, message="La consulta ya está finalizada y no admite más cambios"):
        super().__init__(message)


# ---------------------------------------------------------
# TRATAMIENTOS
# ---------------------------------------------------------
class TratamientoNotFoundError(DomainError):
    def __init__(self, message="El tratamiento médico no fue encontrado"):
        super().__init__(message)

class InvalidTratamientoError(DomainError):
    def __init__(self, message="Los datos del tratamiento son inválidos o están incompletos"):
        super().__init__(message)

class ConsultaWithNoTratamientosError(DomainError):
    def __init__(self, message="Esta consulta no registra tratamientos aplicados"):
        super().__init__(message)


# ---------------------------------------------------------
# ARCHIVOS CLÍNICOS
# ---------------------------------------------------------
class ArchivoClinicoNotFoundError(DomainError):
    def __init__(self, message="El archivo (imagen/estudio) no fue encontrado"):
        super().__init__(message)

class ArchivoClinicoDoesNotBelongToConsultaError(DomainError):
    def __init__(self, message="El archivo no corresponde a la consulta indicada"):
        super().__init__(message)

class NonExistentArchivoClinicoError(DomainError):
    def __init__(self, message="El archivo solicitado no existe físicamente en el almacenamiento"):
        super().__init__(message)


# ---------------------------------------------------------
# GENERALES / ESTADO
# ---------------------------------------------------------
class OperationNotAllowedError(DomainError):
    def __init__(self, message="Operación no permitida por las reglas del sistema"):
        super().__init__(message)

class InvalidStateError(DomainError):
    def __init__(self, message="El registro se encuentra en un estado que no permite esta acción"):
        super().__init__(message)