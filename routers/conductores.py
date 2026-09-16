from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Conductor
from schemas import ConductorCreate, ConductorResponse


router = APIRouter(
    prefix="/conductores",
    tags=["Conductores"]
)


# =========================
# OBTENER TODOS
# =========================

@router.get("/", response_model=list[ConductorResponse])
def obtener_conductores(db: Session = Depends(get_db)):
    return db.query(Conductor).all()


# =========================
# OBTENER UNO
# =========================

@router.get("/{conductor_id}", response_model=ConductorResponse)
def obtener_conductor(
    conductor_id: int,
    db: Session = Depends(get_db)
):
    conductor = db.query(Conductor).filter(
        Conductor.id == conductor_id
    ).first()

    if not conductor:
        raise HTTPException(
            status_code=404,
            detail="Conductor no encontrado"
        )

    return conductor


# =========================
# CREAR
# =========================

@router.post("/", response_model=ConductorResponse)
def crear_conductor(
    conductor: ConductorCreate,
    db: Session = Depends(get_db)
):
    nuevo_conductor = Conductor(
        nombre=conductor.nombre,
        apellido=conductor.apellido,
        documento=conductor.documento,
        licencia=conductor.licencia,
        telefono=conductor.telefono,
        activo=conductor.activo
    )

    db.add(nuevo_conductor)
    db.commit()
    db.refresh(nuevo_conductor)

    return nuevo_conductor


# =========================
# ACTUALIZAR
# =========================

@router.put("/{conductor_id}", response_model=ConductorResponse)
def actualizar_conductor(
    conductor_id: int,
    conductor: ConductorCreate,
    db: Session = Depends(get_db)
):
    conductor_db = db.query(Conductor).filter(
        Conductor.id == conductor_id
    ).first()

    if not conductor_db:
        raise HTTPException(
            status_code=404,
            detail="Conductor no encontrado"
        )

    conductor_db.nombre = conductor.nombre
    conductor_db.apellido = conductor.apellido
    conductor_db.documento = conductor.documento
    conductor_db.licencia = conductor.licencia
    conductor_db.telefono = conductor.telefono
    conductor_db.activo = conductor.activo

    db.commit()
    db.refresh(conductor_db)

    return conductor_db


# =========================
# ELIMINAR
# =========================

@router.delete("/{conductor_id}")
def eliminar_conductor(
    conductor_id: int,
    db: Session = Depends(get_db)
):
    conductor = db.query(Conductor).filter(
        Conductor.id == conductor_id
    ).first()

    if not conductor:
        raise HTTPException(
            status_code=404,
            detail="Conductor no encontrado"
        )

    db.delete(conductor)
    db.commit()

    return {
        "mensaje": "Conductor eliminado correctamente"
    }