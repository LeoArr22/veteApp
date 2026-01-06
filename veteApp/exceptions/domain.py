class DomainError(Exception):
    pass


# -----------------------------
# Dueños
# -----------------------------
class DuenoNoEncontrado(DomainError):
    pass


class DuenoSinPacientes(DomainError):
    pass


# -----------------------------
# Pacientes
# -----------------------------
class PacienteNoEncontrado(DomainError):
    pass


class PacienteInactivo(DomainError):
    pass


class PacienteNoPerteneceADueno(DomainError):
    pass


# -----------------------------
# Veterinarios
# -----------------------------
class VeterinarioNoEncontrado(DomainError):
    pass


class VeterinarioInactivo(DomainError):
    pass


# -----------------------------
# Consultas
# -----------------------------
class ConsultaNoEncontrada(DomainError):
    pass


class ConsultaNoPerteneceAPaciente(DomainError):
    pass


class ConsultaCerrada(DomainError):
    pass


# -----------------------------
# Tratamientos
# -----------------------------
class TratamientoNoEncontrado(DomainError):
    pass


class TratamientoInvalido(DomainError):
    pass


class ConsultaSinTratamientos(DomainError):
    pass


# -----------------------------
# Archivos clínicos
# -----------------------------
class ArchivoClinicoNoEncontrado(DomainError):
    pass


class ArchivoClinicoNoPerteneceAConsulta(DomainError):
    pass


class ArchivoClinicoInexistente(DomainError):
    pass


# -----------------------------
# Generales
# -----------------------------
class OperacionNoPermitida(DomainError):
    pass


class EstadoInvalido(DomainError):
    pass
