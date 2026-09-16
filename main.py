from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from database import engine


# Routers
from routers.roles import router as roles_router
from routers.usuarios import router as usuarios_router
from routers.acudientes import router as acudientes_router
from routers.estudiantes import router as estudiantes_router
from routers.conductores import router as conductores_router
from routers.vehiculos import router as vehiculos_router
from routers.rutas import router as rutas_router
from routers.paraderos import router as paraderos_router
from routers.estudiante_ruta import router as estudiante_ruta_router
from routers.registros_abordaje import router as registros_abordaje_router


app = FastAPI(
    title="Gestión de Rutas y Transporte Escolar",
    description="API para la gestión del transporte escolar",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://monumental-faun-1cec9c.netlify.app",
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(IntegrityError)
async def manejar_error_integridad(request: Request, exc: IntegrityError):
    """Devuelve un conflicto legible al violar claves únicas o foráneas."""
    return JSONResponse(
        status_code=409,
        content={"detail": "No se pudo guardar el registro: ya existe o referencia datos inexistentes."},
    )


# =========================
# REGISTRO DE ROUTERS
# =========================

app.include_router(roles_router)
app.include_router(usuarios_router)
app.include_router(acudientes_router)
app.include_router(estudiantes_router)
app.include_router(conductores_router)
app.include_router(vehiculos_router)
app.include_router(rutas_router)
app.include_router(paraderos_router)
app.include_router(estudiante_ruta_router)
app.include_router(registros_abordaje_router)


# =========================
# RUTA PRINCIPAL
# =========================

@app.get("/")
def inicio():
    return {
        "mensaje": "API funcionando"
    }


# =========================
# PRUEBA DE BASE DE DATOS
# =========================

@app.get("/prueba-db")
def prueba_db():
    with engine.connect() as connection:
        resultado = connection.execute(text("SELECT 1"))

        return {
            "mensaje": "Conexion con Supabase exitosa",
            "resultado": resultado.scalar()
        }
