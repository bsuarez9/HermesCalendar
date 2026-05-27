"""Contenedor de dependencias (Dependency Injection)."""
import os
from typing import Generator

from sqlalchemy.orm import Session

from ...application.use_cases.gestionar_hito_importante import (
    ActualizarHitoImportanteUseCase,
    CrearHitoImportanteUseCase,
    EliminarHitoImportanteUseCase,
    ListarHitosImportantesUseCase,
)
from ...application.use_cases.gestionar_hito_periodico import (
    ActualizarHitoPeriodicoUseCase,
    CrearHitoPeriodicoUseCase,
    EliminarHitoPeriodicoUseCase,
    ListarHitosPeriodicosUseCase,
)
from ...application.use_cases.obtener_dashboard import ObtenerDashboardUseCase
from ...domain.services.calendario_service import CalendarioService
from ...infrastructure.config.database import SessionLocal
from ...infrastructure.persistence.repositories.calendario_repository_impl import (
    CalendarioRepositoryImpl,
)
from ...infrastructure.persistence.repositories.hito_importante_repository_impl import (
    HitoImportanteRepositoryImpl,
)
from ...infrastructure.persistence.repositories.hito_periodico_repository_impl import (
    HitoPeriodicoRepositoryImpl,
)


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


# Singletons para repositorios que no usan DB
_calendario_repository: CalendarioRepositoryImpl | None = None


def get_calendario_repository() -> CalendarioRepositoryImpl:
    """
    Dependency para obtener el repositorio de calendario.

    Returns:
        Implementación del repositorio de calendario
    """
    global _calendario_repository
    if _calendario_repository is None:
        excel_path = os.getenv(
            "EXCEL_FILE_PATH", "./Calendario_Argentina_2026_Completo.xlsx"
        )
        _calendario_repository = CalendarioRepositoryImpl(excel_path)
    return _calendario_repository


def get_hito_periodico_repository(db: Session) -> HitoPeriodicoRepositoryImpl:
    """
    Dependency para obtener el repositorio de hitos periódicos.

    Args:
        db: Sesión de base de datos

    Returns:
        Implementación del repositorio de hitos periódicos
    """
    return HitoPeriodicoRepositoryImpl(db)


def get_hito_importante_repository(db: Session) -> HitoImportanteRepositoryImpl:
    """
    Dependency para obtener el repositorio de hitos importantes.

    Args:
        db: Sesión de base de datos

    Returns:
        Implementación del repositorio de hitos importantes
    """
    return HitoImportanteRepositoryImpl(db)


def get_calendario_service(
    calendario_repo: CalendarioRepositoryImpl,
) -> CalendarioService:
    """
    Dependency para obtener el servicio de calendario.

    Args:
        calendario_repo: Repositorio de calendario

    Returns:
        Servicio de calendario
    """
    return CalendarioService(calendario_repo)


# Use Cases
def get_obtener_dashboard_use_case(
    db: Session,
    calendario_repo: CalendarioRepositoryImpl,
) -> ObtenerDashboardUseCase:
    """Dependency para obtener el use case del dashboard."""
    hito_periodico_repo = get_hito_periodico_repository(db)
    hito_importante_repo = get_hito_importante_repository(db)
    calendario_service = get_calendario_service(calendario_repo)

    return ObtenerDashboardUseCase(
        calendario_repo=calendario_repo,
        hito_periodico_repo=hito_periodico_repo,
        hito_importante_repo=hito_importante_repo,
        calendario_service=calendario_service,
    )


def get_crear_hito_periodico_use_case(db: Session) -> CrearHitoPeriodicoUseCase:
    """Dependency para crear hito periódico."""
    hito_repo = get_hito_periodico_repository(db)
    return CrearHitoPeriodicoUseCase(hito_repo)


def get_actualizar_hito_periodico_use_case(db: Session) -> ActualizarHitoPeriodicoUseCase:
    """Dependency para actualizar hito periódico."""
    hito_repo = get_hito_periodico_repository(db)
    return ActualizarHitoPeriodicoUseCase(hito_repo)


def get_eliminar_hito_periodico_use_case(db: Session) -> EliminarHitoPeriodicoUseCase:
    """Dependency para eliminar hito periódico."""
    hito_repo = get_hito_periodico_repository(db)
    return EliminarHitoPeriodicoUseCase(hito_repo)


def get_listar_hitos_periodicos_use_case(db: Session) -> ListarHitosPeriodicosUseCase:
    """Dependency para listar hitos periódicos."""
    hito_repo = get_hito_periodico_repository(db)
    return ListarHitosPeriodicosUseCase(hito_repo)


def get_crear_hito_importante_use_case(db: Session) -> CrearHitoImportanteUseCase:
    """Dependency para crear hito importante."""
    hito_repo = get_hito_importante_repository(db)
    return CrearHitoImportanteUseCase(hito_repo)


def get_actualizar_hito_importante_use_case(db: Session) -> ActualizarHitoImportanteUseCase:
    """Dependency para actualizar hito importante."""
    hito_repo = get_hito_importante_repository(db)
    return ActualizarHitoImportanteUseCase(hito_repo)


def get_eliminar_hito_importante_use_case(db: Session) -> EliminarHitoImportanteUseCase:
    """Dependency para eliminar hito importante."""
    hito_repo = get_hito_importante_repository(db)
    return EliminarHitoImportanteUseCase(hito_repo)


def get_listar_hitos_importantes_use_case(db: Session) -> ListarHitosImportantesUseCase:
    """Dependency para listar hitos importantes."""
    hito_repo = get_hito_importante_repository(db)
    return ListarHitosImportantesUseCase(hito_repo)
