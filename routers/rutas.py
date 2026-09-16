from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Ruta
from schemas import RutaCreate, RutaResponse


router = APIRouter(
    prefix="/rutas",
    tags=["Rutas"]
)


# =========================
# OBTENER TODAS LAS RUTAS
# =========================

@router.get("/", response_model=list[RutaResponse])
def obtener_rutas(db: Session = Depends(get_db)):
    return db.query(Ruta).all()


# =========================
# OBTENER UNA RUTA
# =========================

@router.get("/{ruta_id}", response_model=RutaResponse)
def obtener_ruta(
    ruta_id: int,
    db: Session = Depends(get_db)
):
    ruta = db.query(Ruta).filter(
        Ruta.id == ruta_id
    ).first()

    if not ruta:
        raise HTTPException(
            status_code=404,
            detail="Ruta no encontrada"
        )

    return ruta


# =========================
# CREAR RUTA
# =========================

@router.post("/", response_model=RutaResponse)
def crear_ruta(
    ruta: RutaCreate,
    db: Session = Depends(get_db)
):
    nueva_ruta = Ruta(
        nombre=ruta.nombre,
        descripcion=ruta.descripcion,
        hora_salida=ruta.hora_salida,
        hora_llegada=ruta.hora_llegada,
        conductor_id=ruta.conductor_id,
        vehiculo_id=ruta.vehiculo_id,
        estado=ruta.estado
    )

    db.add(nueva_ruta)
    db.commit()
    db.refresh(nueva_ruta)

    return nueva_ruta


# =========================
# ACTUALIZAR RUTA
# =========================

@router.put("/{ruta_id}", response_model=RutaResponse)
def actualizar_ruta(
    ruta_id: int,
    ruta: RutaCreate,
    db: Session = Depends(get_db)
):
    ruta_db = db.query(Ruta).filter(
        Ruta.id == ruta_id
    ).first()

    if not ruta_db:
        raise HTTPException(
            status_code=404,
            detail="Ruta no encontrada"
        )

    ruta_db.nombre = ruta.nombre
    ruta_db.descripcion = ruta.descripcion
    ruta_db.hora_salida = ruta.hora_salida
    ruta_db.hora_llegada = ruta.hora_llegada
    ruta_db.conductor_id = ruta.conductor_id
    ruta_db.vehiculo_id = ruta.vehiculo_id
    ruta_db.estado = ruta.estado

    db.commit()
    db.refresh(ruta_db)

    return ruta_db


# =========================
# ELIMINAR RUTA
# =========================

@router.delete("/{ruta_id}")
def eliminar_ruta(
    ruta_id: int,
    db: Session = Depends(get_db)
):
    ruta = db.query(Ruta).filter(
        Ruta.id == ruta_id
    ).first()

    if not ruta:
        raise HTTPException(
            status_code=404,
            detail="Ruta no encontrada"
        )

    db.delete(ruta)
    db.commit()

    return {
        "mensaje": "Ruta eliminada correctamente"
    }