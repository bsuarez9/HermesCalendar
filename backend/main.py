"""Punto de entrada principal de la aplicación FastAPI."""
import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.infrastructure.config.database import init_db
from src.presentation.api.v1 import (
    dashboard_router,
    hitos_importantes_router,
    hitos_periodicos_router,
)

# Cargar variables de entorno
load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Contexto de ciclo de vida de la aplicación.

    Se ejecuta al iniciar y al cerrar la aplicación.
    """
    # Startup: Inicializar base de datos
    print("🚀 Inicializando base de datos...")
    init_db()
    print("✅ Base de datos inicializada")

    yield

    # Shutdown
    print("👋 Cerrando aplicación...")


# Crear aplicación FastAPI
app = FastAPI(
    title="Calendario YPF API",
    description="""
    API REST para la gestión del calendario de hitos de YPF.

    Funcionalidades:
    - Dashboard con posición actual en el mes (D+X)
    - Gestión de hitos periódicos (mensuales)
    - Gestión de hitos importantes (fechas específicas)
    - Consulta de días hábiles y feriados

    Arquitectura: Clean Architecture / Hexagonal
    """,
    version="1.0.0",
    lifespan=lifespan,
)

# Configurar CORS
origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers
app.include_router(dashboard_router.router, prefix="/api/v1")
app.include_router(hitos_periodicos_router.router, prefix="/api/v1")
app.include_router(hitos_importantes_router.router, prefix="/api/v1")


@app.get("/", tags=["Health"])
async def root():
    """Health check endpoint."""
    return {
        "status": "ok",
        "message": "Calendario YPF API is running",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/health", tags=["Health"])
async def health():
    """Health check detallado."""
    return {
        "status": "healthy",
        "database": "connected",
        "excel": os.path.exists(
            os.getenv("EXCEL_FILE_PATH", "./Calendario_Argentina_2026_Completo.xlsx")
        ),
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Hot reload en desarrollo
    )
