from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Paradero
from schemas import ParaderoCreate, ParaderoResponse


router = APIRouter(
    prefix="/paraderos",
    tags=["Paraderos"]
)


# =========================
# OBTENER TODOS
# =========================

@router.get("/", response_model=list[ParaderoResponse])
def obtener_paraderos(db: Session = Depends(get_db)):
    return db.query(Paradero).all()


# =========================
# OBTENER UNO
# =========================

@router.get("/{paradero_id}", response_model=ParaderoResponse)
def obtener_paradero(
    paradero_id: int,
    db: Session = Depends(get_db)
):
    paradero = db.query(Paradero).filter(
        Paradero.id == paradero_id
    ).first()

    if not paradero:
        raise HTTPException(
            status_code=404,
            detail="Paradero no encontrado"
        )

    return paradero


# =========================
# CREAR
# =========================

@router.post("/", response_model=ParaderoResponse)
def crear_paradero(
    paradero: ParaderoCreate,
    db: Session = Depends(get_db)
):
    nuevo_paradero = Paradero(
        nombre=paradero.nombre,
        direccion=paradero.direccion,
        referencia=paradero.referencia,
        latitud=paradero.latitud,
        longitud=paradero.longitud
    )

    db.add(nuevo_paradero)
    db.commit()
    db.refresh(nuevo_paradero)

    return nuevo_paradero


# =========================
# ACTUALIZAR
# =========================

@router.put("/{paradero_id}", response_model=ParaderoResponse)
def actualizar_paradero(
    paradero_id: int,
    paradero: ParaderoCreate,
    db: Session = Depends(get_db)
):
    paradero_db = db.query(Paradero).filter(
        Paradero.id == paradero_id
    ).first()

    if not paradero_db:
        raise HTTPException(
            status_code=404,
            detail="Paradero no encontrado"
        )

    paradero_db.nombre = paradero.nombre
    paradero_db.direccion = paradero.direccion
    paradero_db.referencia = paradero.referencia
    paradero_db.latitud = paradero.latitud
    paradero_db.longitud = paradero.longitud

    db.commit()
    db.refresh(paradero_db)

    return paradero_db


# =========================
# ELIMINAR
# =========================

@router.delete("/{paradero_id}")
def eliminar_paradero(
    paradero_id: int,
    db: Session = Depends(get_db)
):
    paradero = db.query(Paradero).filter(
        Paradero.id == paradero_id
    ).first()

    if not paradero:
        raise HTTPException(
            status_code=404,
            detail="Paradero no encontrado"
        )

    db.delete(paradero)
    db.commit()

    return {
        "mensaje": "Paradero eliminado correctamente"
    }