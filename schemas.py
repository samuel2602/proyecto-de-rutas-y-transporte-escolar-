from pydantic import BaseModel
from typing import Optional
from datetime import time, datetime


# =========================
# ROLES
# =========================

class RolBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None


class RolCreate(RolBase):
    pass


class RolResponse(RolBase):
    id: int

    class Config:
        from_attributes = True


# =========================
# USUARIOS
# =========================

class UsuarioBase(BaseModel):
    nombre: str
    apellido: str
    correo: str
    telefono: Optional[str] = None
    rol_id: int


class UsuarioCreate(UsuarioBase):
    pass


class UsuarioResponse(UsuarioBase):
    id: int

    class Config:
        from_attributes = True


# =========================
# ACUDIENTES
# =========================

class AcudienteBase(BaseModel):
    nombre: str
    apellido: str
    documento: str
    telefono: str
    correo: Optional[str] = None
    usuario_id: int


class AcudienteCreate(AcudienteBase):
    pass


class AcudienteResponse(AcudienteBase):
    id: int

    class Config:
        from_attributes = True


# =========================
# ESTUDIANTES
# =========================

class EstudianteBase(BaseModel):
    nombre: str
    apellido: str
    documento: str
    grado: Optional[str] = None
    direccion: Optional[str] = None
    acudiente_id: int


class EstudianteCreate(EstudianteBase):
    pass


class EstudianteResponse(EstudianteBase):
    id: int

    class Config:
        from_attributes = True


# =========================
# CONDUCTORES
# =========================

class ConductorBase(BaseModel):
    nombre: str
    apellido: str
    documento: str
    licencia: str
    telefono: Optional[str] = None
    activo: Optional[bool] = True


class ConductorCreate(ConductorBase):
    pass


class ConductorResponse(ConductorBase):
    id: int

    class Config:
        from_attributes = True


# =========================
# VEHICULOS
# =========================

class VehiculoBase(BaseModel):
    placa: str
    marca: Optional[str] = None
    modelo: Optional[str] = None
    capacidad: int
    estado: Optional[str] = "Disponible"


class VehiculoCreate(VehiculoBase):
    pass


class VehiculoResponse(VehiculoBase):
    id: int

    class Config:
        from_attributes = True


# =========================
# RUTAS
# =========================

class RutaBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    hora_salida: time
    hora_llegada: Optional[time] = None
    conductor_id: int
    vehiculo_id: int
    estado: Optional[str] = "Activa"


class RutaCreate(RutaBase):
    pass


class RutaResponse(RutaBase):
    id: int

    class Config:
        from_attributes = True


# =========================
# PARADEROS
# =========================

class ParaderoBase(BaseModel):
    nombre: str
    direccion: str
    referencia: Optional[str] = None
    latitud: Optional[float] = None
    longitud: Optional[float] = None


class ParaderoCreate(ParaderoBase):
    pass


class ParaderoResponse(ParaderoBase):
    id: int

    class Config:
        from_attributes = True


# =========================
# ESTUDIANTE - RUTA
# =========================

class EstudianteRutaBase(BaseModel):
    estudiante_id: int
    ruta_id: int
    paradero_id: int


class EstudianteRutaCreate(EstudianteRutaBase):
    pass


class EstudianteRutaResponse(EstudianteRutaBase):
    id: int

    class Config:
        from_attributes = True


# =========================
# REGISTROS DE ABORDAJE
# =========================

class RegistroAbordajeBase(BaseModel):
    estudiante_id: int
    ruta_id: int
    tipo: str


class RegistroAbordajeCreate(RegistroAbordajeBase):
    pass


class RegistroAbordajeResponse(RegistroAbordajeBase):
    id: int
    fecha_hora: Optional[datetime] = None

    class Config:
        from_attributes = True