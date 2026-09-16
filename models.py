from sqlalchemy import Column, Integer, String, Boolean, Time, DECIMAL, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base


class Rol(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False, unique=True)
    descripcion = Column(String(150))

    usuarios = relationship("Usuario", back_populates="rol")


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    correo = Column(String(100), nullable=False, unique=True)
    telefono = Column(String(20))
    rol_id = Column(Integer, ForeignKey("roles.id"), nullable=False)

    rol = relationship("Rol", back_populates="usuarios")
    acudientes = relationship("Acudiente", back_populates="usuario")


class Acudiente(Base):
    __tablename__ = "acudientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    documento = Column(String(30), nullable=False, unique=True)
    telefono = Column(String(20), nullable=False)
    correo = Column(String(100))
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    estudiantes = relationship("Estudiante", back_populates="acudiente")
    usuario = relationship("Usuario", back_populates="acudientes")


class Estudiante(Base):
    __tablename__ = "estudiantes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    documento = Column(String(30), nullable=False, unique=True)
    grado = Column(String(30))
    direccion = Column(String(150))
    acudiente_id = Column(Integer, ForeignKey("acudientes.id"), nullable=False)

    acudiente = relationship("Acudiente", back_populates="estudiantes")


class Conductor(Base):
    __tablename__ = "conductores"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    documento = Column(String(30), nullable=False, unique=True)
    licencia = Column(String(50), nullable=False, unique=True)
    telefono = Column(String(20))
    activo = Column(Boolean, default=True)


class Vehiculo(Base):
    __tablename__ = "vehiculos"

    id = Column(Integer, primary_key=True, index=True)
    placa = Column(String(10), nullable=False, unique=True)
    marca = Column(String(50))
    modelo = Column(String(50))
    capacidad = Column(Integer, nullable=False)
    estado = Column(String(30), default="Disponible")


class Ruta(Base):
    __tablename__ = "rutas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False, unique=True)
    descripcion = Column(String(200))
    hora_salida = Column(Time, nullable=False)
    hora_llegada = Column(Time)
    conductor_id = Column(Integer, ForeignKey("conductores.id"), nullable=False)
    vehiculo_id = Column(Integer, ForeignKey("vehiculos.id"), nullable=False)
    estado = Column(String(30), default="Activa")

    conductor = relationship("Conductor")
    vehiculo = relationship("Vehiculo")


class Paradero(Base):
    __tablename__ = "paraderos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    direccion = Column(String(150), nullable=False)
    referencia = Column(String(200))
    latitud = Column(DECIMAL(10, 7))
    longitud = Column(DECIMAL(10, 7))


class EstudianteRuta(Base):
    __tablename__ = "estudiante_ruta"
    __table_args__ = (
        UniqueConstraint(
            "estudiante_id",
            "ruta_id",
            "paradero_id",
            name="uq_estudiante_ruta_asignacion"
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    estudiante_id = Column(Integer, ForeignKey("estudiantes.id"), nullable=False)
    ruta_id = Column(Integer, ForeignKey("rutas.id"), nullable=False)
    paradero_id = Column(Integer, ForeignKey("paraderos.id"), nullable=False)


class RegistroAbordaje(Base):
    __tablename__ = "registros_abordaje"

    id = Column(Integer, primary_key=True, index=True)
    estudiante_id = Column(Integer, ForeignKey("estudiantes.id"), nullable=False)
    ruta_id = Column(Integer, ForeignKey("rutas.id"), nullable=False)
    fecha_hora = Column(DateTime, server_default="CURRENT_TIMESTAMP")
    tipo = Column(String(20), nullable=False)