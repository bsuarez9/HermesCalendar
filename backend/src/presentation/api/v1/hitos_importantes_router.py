"""Router para gestión de hitos importantes."""
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from ...dependencies.container import (
    get_actualizar_hito_importante_use_case,
    get_crear_hito_importante_use_case,
    get_db,
    get_eliminar_hito_importante_use_case,
    get_listar_hitos_importantes_use_case,
)
from ...schemas.hito_schemas import (
    HitoImportanteCreate,
    HitoImportanteResponse,
    HitoImportanteUpdate,
)
from ....application.dtos.hito_importante_dto import (
    ActualizarHitoImportanteDTO,
    CrearHitoImportanteDTO,
)
from ....application.use_cases.gestionar_hito_importante import (
    ActualizarHitoImportanteUseCase,
    CrearHitoImportanteUseCase,
    EliminarHitoImportanteUseCase,
    ListarHitosImportantesUseCase,
)

router = APIRouter(prefix="/hitos-importantes", tags=["Hitos Importantes"])


@router.get(
    "", response_model=List[HitoImportanteResponse], summary="Listar hitos importantes"
)
async def listar_hitos(
    solo_activos: bool = True,
    categoria: Optional[str] = Query(None, description="Filtrar por categoría"),
    use_case: ListarHitosImportantesUseCase = Depends(get_listar_hitos_importantes_use_case),
) -> List[HitoImportanteResponse]:
    """
    Lista todos los hitos importantes.

    Args:
        solo_activos: Si es True, solo retorna hitos activos
        categoria: Filtrar por categoría (opcional)
    """
    hitos_dtos = use_case.execute(categoria=categoria, solo_activos=solo_activos)
    return [HitoImportanteResponse(**dto.__dict__) for dto in hitos_dtos]


@router.post(
    "",
    response_model=HitoImportanteResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear hito importante",
)
async def crear_hito(
    hito: HitoImportanteCreate,
    use_case: CrearHitoImportanteUseCase = Depends(get_crear_hito_importante_use_case),
) -> HitoImportanteResponse:
    """
    Crea un nuevo hito importante con fecha específica.

    Ejemplos: reuniones, proyectos, migraciones, eventos importantes.
    """
    try:
        dto = CrearHitoImportanteDTO(**hito.model_dump())
        hito_dto = use_case.execute(dto)
        return HitoImportanteResponse(**hito_dto.__dict__)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put(
    "/{hito_id}", response_model=HitoImportanteResponse, summary="Actualizar hito importante"
)
async def actualizar_hito(
    hito_id: str,
    hito: HitoImportanteUpdate,
    use_case: ActualizarHitoImportanteUseCase = Depends(get_actualizar_hito_importante_use_case),
) -> HitoImportanteResponse:
    """
    Actualiza un hito importante existente.

    Solo los campos provistos serán actualizados.
    """
    try:
        hito_uuid = UUID(hito_id)
        dto = ActualizarHitoImportanteDTO(**hito.model_dump(exclude_none=True))
        hito_dto = use_case.execute(hito_uuid, dto)
        return HitoImportanteResponse(**hito_dto.__dict__)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete(
    "/{hito_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar hito importante",
)
async def eliminar_hito(
    hito_id: str,
    use_case: EliminarHitoImportanteUseCase = Depends(get_eliminar_hito_importante_use_case),
) -> None:
    """
    Elimina un hito importante.

    Esta acción es permanente y no se puede deshacer.
    """
    try:
        hito_uuid = UUID(hito_id)
        eliminado = use_case.execute(hito_uuid)
        if not eliminado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Hito no encontrado"
            )
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID inválido")
