from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Estudiante
from schemas import EstudianteCreate, EstudianteResponse


router = APIRouter(
    prefix="/estudiantes",
    tags=["Estudiantes"]
)


# =========================================================
# GET - Obtener todos los estudiantes
# =========================================================

@router.get("/", response_model=list[EstudianteResponse])
def obtener_estudiantes(db: Session = Depends(get_db)):
    return db.query(Estudiante).all()


# =========================================================
# GET - Obtener estudiante por ID
# =========================================================

@router.get("/{estudiante_id}", response_model=EstudianteResponse)
def obtener_estudiante(
    estudiante_id: int,
    db: Session = Depends(get_db)
):
    estudiante = db.query(Estudiante).filter(
        Estudiante.id == estudiante_id
    ).first()

    if not estudiante:
        raise HTTPException(
            status_code=404,
            detail="Estudiante no encontrado"
        )

    return estudiante


# =========================================================
# POST - Crear estudiante
# =========================================================

@router.post("/", response_model=EstudianteResponse)
def crear_estudiante(
    estudiante: EstudianteCreate,
    db: Session = Depends(get_db)
):
    # Verificar documento duplicado
    existente = db.query(Estudiante).filter(
        Estudiante.documento == estudiante.documento
    ).first()

    if existente:
        raise HTTPException(
            status_code=400,
            detail="Ya existe un estudiante con ese documento"
        )

    nuevo_estudiante = Estudiante(
        nombre=estudiante.nombre,
        apellido=estudiante.apellido,
        documento=estudiante.documento,
        grado=estudiante.grado,
        direccion=estudiante.direccion,
        acudiente_id=estudiante.acudiente_id
    )

    db.add(nuevo_estudiante)
    db.commit()
    db.refresh(nuevo_estudiante)

    return nuevo_estudiante


# =========================================================
# PUT - Actualizar estudiante
# =========================================================

@router.put("/{estudiante_id}", response_model=EstudianteResponse)
def actualizar_estudiante(
    estudiante_id: int,
    estudiante: EstudianteCreate,
    db: Session = Depends(get_db)
):
    estudiante_db = db.query(Estudiante).filter(
        Estudiante.id == estudiante_id
    ).first()

    if not estudiante_db:
        raise HTTPException(
            status_code=404,
            detail="Estudiante no encontrado"
        )

    estudiante_db.nombre = estudiante.nombre
    estudiante_db.apellido = estudiante.apellido
    estudiante_db.documento = estudiante.documento
    estudiante_db.grado = estudiante.grado
    estudiante_db.direccion = estudiante.direccion
    estudiante_db.acudiente_id = estudiante.acudiente_id

    db.commit()
    db.refresh(estudiante_db)

    return estudiante_db


# =========================================================
# DELETE - Eliminar estudiante
# =========================================================

@router.delete("/{estudiante_id}")
def eliminar_estudiante(
    estudiante_id: int,
    db: Session = Depends(get_db)
):
    estudiante = db.query(Estudiante).filter(
        Estudiante.id == estudiante_id
    ).first()

    if not estudiante:
        raise HTTPException(
            status_code=404,
            detail="Estudiante no encontrado"
        )

    db.delete(estudiante)
    db.commit()

    return {
        "mensaje": "Estudiante eliminado correctamente"
    }