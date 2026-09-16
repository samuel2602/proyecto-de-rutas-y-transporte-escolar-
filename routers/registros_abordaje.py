from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import RegistroAbordaje
from schemas import RegistroAbordajeCreate, RegistroAbordajeResponse


router = APIRouter(
    prefix="/registros-abordaje",
    tags=["Registros de Abordaje"]
)


@router.get("/", response_model=list[RegistroAbordajeResponse])
def obtener_registros(db: Session = Depends(get_db)):
    return db.query(RegistroAbordaje).all()


@router.get("/{registro_id}", response_model=RegistroAbordajeResponse)
def obtener_registro(
    registro_id: int,
    db: Session = Depends(get_db)
):
    registro = db.query(RegistroAbordaje).filter(
        RegistroAbordaje.id == registro_id
    ).first()

    if not registro:
        raise HTTPException(
            status_code=404,
            detail="Registro no encontrado"
        )

    return registro


@router.post("/", response_model=RegistroAbordajeResponse)
def crear_registro(
    registro: RegistroAbordajeCreate,
    db: Session = Depends(get_db)
):
    nuevo_registro = RegistroAbordaje(
        estudiante_id=registro.estudiante_id,
        ruta_id=registro.ruta_id,
        tipo=registro.tipo
    )

    db.add(nuevo_registro)
    db.commit()
    db.refresh(nuevo_registro)

    return nuevo_registro


@router.put("/{registro_id}", response_model=RegistroAbordajeResponse)
def actualizar_registro(
    registro_id: int,
    registro: RegistroAbordajeCreate,
    db: Session = Depends(get_db)
):
    registro_db = db.query(RegistroAbordaje).filter(
        RegistroAbordaje.id == registro_id
    ).first()

    if not registro_db:
        raise HTTPException(
            status_code=404,
            detail="Registro no encontrado"
        )

    registro_db.estudiante_id = registro.estudiante_id
    registro_db.ruta_id = registro.ruta_id
    registro_db.tipo = registro.tipo

    db.commit()
    db.refresh(registro_db)

    return registro_db


@router.delete("/{registro_id}")
def eliminar_registro(
    registro_id: int,
    db: Session = Depends(get_db)
):
    registro = db.query(RegistroAbordaje).filter(
        RegistroAbordaje.id == registro_id
    ).first()

    if not registro:
        raise HTTPException(
            status_code=404,
            detail="Registro no encontrado"
        )

    db.delete(registro)
    db.commit()

    return {
        "mensaje": "Registro eliminado correctamente"
    }