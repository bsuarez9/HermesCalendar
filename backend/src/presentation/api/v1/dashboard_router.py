"""Router para el dashboard."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...dependencies.container import (
    get_calendario_repository,
    get_db,
    get_obtener_dashboard_use_case,
)
from ...schemas.dashboard_schemas import DashboardResponse
from ....application.use_cases.obtener_dashboard import ObtenerDashboardUseCase
from ....infrastructure.persistence.repositories.calendario_repository_impl import (
    CalendarioRepositoryImpl,
)

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("", response_model=DashboardResponse, summary="Obtener datos del dashboard")
async def obtener_dashboard(
    db: Session = Depends(get_db),
    calendario_repo: CalendarioRepositoryImpl = Depends(get_calendario_repository),
) -> DashboardResponse:
    """
    Obtiene todos los datos necesarios para renderizar el dashboard principal.

    Retorna:
    - Posición actual en el mes (D+X)
    - Hitos del próximo día hábil
    - Próximos feriados
    - Hitos importantes próximos
    - Días hábiles restantes en el mes
    """
    use_case = get_obtener_dashboard_use_case(db, calendario_repo)
    dashboard_dto = use_case.execute()

    return DashboardResponse(**dashboard_dto.__dict__)
