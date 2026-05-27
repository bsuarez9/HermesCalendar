"""Router para gestión de hitos periódicos."""
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ...dependencies.container import (
    get_actualizar_hito_periodico_use_case,
    get_crear_hito_periodico_use_case,
    get_db,
    get_eliminar_hito_periodico_use_case,
    get_listar_hitos_periodicos_use_case,
)
from ...schemas.hito_schemas import (
    HitoPeriodicoCreate,
    HitoPeriodicoResponse,
    HitoPeriodicoUpdate,
)
from ....application.dtos.hito_periodico_dto import (
    ActualizarHitoPeriodicoDTO,
    CrearHitoPeriodicoDTO,
)
from ....application.use_cases.gestionar_hito_periodico import (
    ActualizarHitoPeriodicoUseCase,
    CrearHitoPeriodicoUseCase,
    EliminarHitoPeriodicoUseCase,
    ListarHitosPeriodicosUseCase,
)

router = APIRouter(prefix="/hitos-periodicos", tags=["Hitos Periódicos"])


@router.get("", response_model=List[HitoPeriodicoResponse], summary="Listar hitos periódicos")
async def listar_hitos(
    solo_activos: bool = True,
    use_case: ListarHitosPeriodicosUseCase = Depends(get_listar_hitos_periodicos_use_case),
) -> List[HitoPeriodicoResponse]:
    """
    Lista todos los hitos periódicos.

    Args:
        solo_activos: Si es True, solo retorna hitos activos
    """
    hitos_dtos = use_case.execute(solo_activos=solo_activos)
    return [HitoPeriodicoResponse(**dto.__dict__) for dto in hitos_dtos]


@router.post(
    "",
    response_model=HitoPeriodicoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear hito periódico",
)
async def crear_hito(
    hito: HitoPeriodicoCreate,
    use_case: CrearHitoPeriodicoUseCase = Depends(get_crear_hito_periodico_use_case),
) -> HitoPeriodicoResponse:
    """
    Crea un nuevo hito periódico.

    El hito se repetirá automáticamente cada mes en el día hábil especificado.
    """
    try:
        dto = CrearHitoPeriodicoDTO(**hito.model_dump())
        hito_dto = use_case.execute(dto)
        return HitoPeriodicoResponse(**hito_dto.__dict__)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put(
    "/{hito_id}", response_model=HitoPeriodicoResponse, summary="Actualizar hito periódico"
)
async def actualizar_hito(
    hito_id: str,
    hito: HitoPeriodicoUpdate,
    use_case: ActualizarHitoPeriodicoUseCase = Depends(get_actualizar_hito_periodico_use_case),
) -> HitoPeriodicoResponse:
    """
    Actualiza un hito periódico existente.

    Solo los campos provistos serán actualizados.
    """
    try:
        hito_uuid = UUID(hito_id)
        dto = ActualizarHitoPeriodicoDTO(**hito.model_dump(exclude_none=True))
        hito_dto = use_case.execute(hito_uuid, dto)
        return HitoPeriodicoResponse(**hito_dto.__dict__)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete(
    "/{hito_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar hito periódico",
)
async def eliminar_hito(
    hito_id: str,
    use_case: EliminarHitoPeriodicoUseCase = Depends(get_eliminar_hito_periodico_use_case),
) -> None:
    """
    Elimina un hito periódico.

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
