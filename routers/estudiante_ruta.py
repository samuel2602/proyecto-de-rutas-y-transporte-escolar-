from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import EstudianteRuta
from schemas import EstudianteRutaCreate, EstudianteRutaResponse


router = APIRouter(
    prefix="/estudiante-ruta",
    tags=["Estudiante - Ruta"]
)


@router.get("/", response_model=list[EstudianteRutaResponse])
def obtener_asignaciones(db: Session = Depends(get_db)):
    return db.query(EstudianteRuta).all()


@router.get("/{asignacion_id}", response_model=EstudianteRutaResponse)
def obtener_asignacion(
    asignacion_id: int,
    db: Session = Depends(get_db)
):
    asignacion = db.query(EstudianteRuta).filter(
        EstudianteRuta.id == asignacion_id
    ).first()

    if not asignacion:
        raise HTTPException(
            status_code=404,
            detail="Asignación no encontrada"
        )

    return asignacion


@router.post("/", response_model=EstudianteRutaResponse)
def crear_asignacion(
    asignacion: EstudianteRutaCreate,
    db: Session = Depends(get_db)
):
    nueva_asignacion = EstudianteRuta(
        estudiante_id=asignacion.estudiante_id,
        ruta_id=asignacion.ruta_id,
        paradero_id=asignacion.paradero_id
    )

    db.add(nueva_asignacion)
    db.commit()
    db.refresh(nueva_asignacion)

    return nueva_asignacion


@router.put("/{asignacion_id}", response_model=EstudianteRutaResponse)
def actualizar_asignacion(
    asignacion_id: int,
    asignacion: EstudianteRutaCreate,
    db: Session = Depends(get_db)
):
    asignacion_db = db.query(EstudianteRuta).filter(
        EstudianteRuta.id == asignacion_id
    ).first()

    if not asignacion_db:
        raise HTTPException(
            status_code=404,
            detail="Asignación no encontrada"
        )

    asignacion_db.estudiante_id = asignacion.estudiante_id
    asignacion_db.ruta_id = asignacion.ruta_id
    asignacion_db.paradero_id = asignacion.paradero_id

    db.commit()
    db.refresh(asignacion_db)

    return asignacion_db


@router.delete("/{asignacion_id}")
def eliminar_asignacion(
    asignacion_id: int,
    db: Session = Depends(get_db)
):
    asignacion = db.query(EstudianteRuta).filter(
        EstudianteRuta.id == asignacion_id
    ).first()

    if not asignacion:
        raise HTTPException(
            status_code=404,
            detail="Asignación no encontrada"
        )

    db.delete(asignacion)
    db.commit()

    return {
        "mensaje": "Asignación eliminada correctamente"
    }