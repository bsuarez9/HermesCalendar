"""Configuración de la base de datos."""
import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

# Obtener DATABASE_URL desde variables de entorno
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./calendario_ypf.db")

# Crear engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
    echo=False,  # Cambiar a True para ver SQL queries en desarrollo
)

# Crear session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para modelos
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency para obtener una sesión de base de datos.

    Yields:
        Sesión de SQLAlchemy
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """
    Inicializa la base de datos creando todas las tablas.

    Se debe llamar al iniciar la aplicación.
    """
    Base.metadata.create_all(bind=engine)
