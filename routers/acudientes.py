from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Acudiente
from schemas import AcudienteCreate, AcudienteResponse


router = APIRouter(
    prefix="/acudientes",
    tags=["Acudientes"]
)


@router.get("/", response_model=list[AcudienteResponse])
def obtener_acudientes(db: Session = Depends(get_db)):
    return db.query(Acudiente).all()


@router.get("/{acudiente_id}", response_model=AcudienteResponse)
def obtener_acudiente(
    acudiente_id: int,
    db: Session = Depends(get_db)
):
    acudiente = db.query(Acudiente).filter(
        Acudiente.id == acudiente_id
    ).first()

    if not acudiente:
        raise HTTPException(
            status_code=404,
            detail="Acudiente no encontrado"
        )

    return acudiente


@router.post("/", response_model=AcudienteResponse)
def crear_acudiente(
    acudiente: AcudienteCreate,
    db: Session = Depends(get_db)
):
    nuevo_acudiente = Acudiente(
        nombre=acudiente.nombre,
        apellido=acudiente.apellido,
        documento=acudiente.documento,
        telefono=acudiente.telefono,
        correo=acudiente.correo,
        usuario_id=acudiente.usuario_id
    )

    db.add(nuevo_acudiente)
    db.commit()
    db.refresh(nuevo_acudiente)

    return nuevo_acudiente


@router.put("/{acudiente_id}", response_model=AcudienteResponse)
def actualizar_acudiente(
    acudiente_id: int,
    acudiente: AcudienteCreate,
    db: Session = Depends(get_db)
):
    acudiente_db = db.query(Acudiente).filter(
        Acudiente.id == acudiente_id
    ).first()

    if not acudiente_db:
        raise HTTPException(
            status_code=404,
            detail="Acudiente no encontrado"
        )

    acudiente_db.nombre = acudiente.nombre
    acudiente_db.apellido = acudiente.apellido
    acudiente_db.documento = acudiente.documento
    acudiente_db.telefono = acudiente.telefono
    acudiente_db.correo = acudiente.correo
    acudiente_db.usuario_id = acudiente.usuario_id

    db.commit()
    db.refresh(acudiente_db)

    return acudiente_db


@router.delete("/{acudiente_id}")
def eliminar_acudiente(
    acudiente_id: int,
    db: Session = Depends(get_db)
):
    acudiente = db.query(Acudiente).filter(
        Acudiente.id == acudiente_id
    ).first()

    if not acudiente:
        raise HTTPException(
            status_code=404,
            detail="Acudiente no encontrado"
        )

    db.delete(acudiente)
    db.commit()

    return {
        "mensaje": "Acudiente eliminado correctamente"
    }