from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Vehiculo
from schemas import VehiculoCreate, VehiculoResponse


router = APIRouter(
    prefix="/vehiculos",
    tags=["Vehículos"]
)


# =========================
# OBTENER TODOS
# =========================

@router.get("/", response_model=list[VehiculoResponse])
def obtener_vehiculos(db: Session = Depends(get_db)):
    return db.query(Vehiculo).all()


# =========================
# OBTENER UNO
# =========================

@router.get("/{vehiculo_id}", response_model=VehiculoResponse)
def obtener_vehiculo(
    vehiculo_id: int,
    db: Session = Depends(get_db)
):
    vehiculo = db.query(Vehiculo).filter(
        Vehiculo.id == vehiculo_id
    ).first()

    if not vehiculo:
        raise HTTPException(
            status_code=404,
            detail="Vehículo no encontrado"
        )

    return vehiculo


# =========================
# CREAR
# =========================

@router.post("/", response_model=VehiculoResponse)
def crear_vehiculo(
    vehiculo: VehiculoCreate,
    db: Session = Depends(get_db)
):
    nuevo_vehiculo = Vehiculo(
        placa=vehiculo.placa,
        marca=vehiculo.marca,
        modelo=vehiculo.modelo,
        capacidad=vehiculo.capacidad,
        estado=vehiculo.estado
    )

    db.add(nuevo_vehiculo)
    db.commit()
    db.refresh(nuevo_vehiculo)

    return nuevo_vehiculo


# =========================
# ACTUALIZAR
# =========================

@router.put("/{vehiculo_id}", response_model=VehiculoResponse)
def actualizar_vehiculo(
    vehiculo_id: int,
    vehiculo: VehiculoCreate,
    db: Session = Depends(get_db)
):
    vehiculo_db = db.query(Vehiculo).filter(
        Vehiculo.id == vehiculo_id
    ).first()

    if not vehiculo_db:
        raise HTTPException(
            status_code=404,
            detail="Vehículo no encontrado"
        )

    vehiculo_db.placa = vehiculo.placa
    vehiculo_db.marca = vehiculo.marca
    vehiculo_db.modelo = vehiculo.modelo
    vehiculo_db.capacidad = vehiculo.capacidad
    vehiculo_db.estado = vehiculo.estado

    db.commit()
    db.refresh(vehiculo_db)

    return vehiculo_db


# =========================
# ELIMINAR
# =========================

@router.delete("/{vehiculo_id}")
def eliminar_vehiculo(
    vehiculo_id: int,
    db: Session = Depends(get_db)
):
    vehiculo = db.query(Vehiculo).filter(
        Vehiculo.id == vehiculo_id
    ).first()

    if not vehiculo:
        raise HTTPException(
            status_code=404,
            detail="Vehículo no encontrado"
        )

    db.delete(vehiculo)
    db.commit()

    return {
        "mensaje": "Vehículo eliminado correctamente"
    }