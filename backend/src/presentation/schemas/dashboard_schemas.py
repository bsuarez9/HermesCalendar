"""Pydantic schemas para el dashboard."""
from typing import List

from pydantic import BaseModel, Field


class DiaCalendarioResponse(BaseModel):
    """Schema para un día del calendario."""

    fecha: str
    nombre_dia: str
    tipo: str
    dia_habil_numero: int | None
    observaciones: str | None
    es_habil: bool
    es_feriado: bool


class PosicionActualResponse(BaseModel):
    """Schema para la posición actual en el mes."""

    dia_habil_actual: int = Field(..., description="Día hábil actual (D+X)")
    proximo_dia_habil: int = Field(..., description="Próximo día hábil (D+X)")
    fecha_actual: str
    fecha_proximo_dia_habil: str


class HitoPeriodicoSimpleResponse(BaseModel):
    """Schema simplificado para hitos periódicos en el dashboard."""

    id: str
    dia_habil: int
    accion: str


class HitosProximoDiaResponse(BaseModel):
    """Schema para hitos del próximo día hábil."""

    dia_habil: int
    fecha: str
    hitos_periodicos: List[HitoPeriodicoSimpleResponse] = Field(default_factory=list)


class HitoImportanteProximoResponse(BaseModel):
    """Schema para hitos importantes próximos."""

    id: str
    fecha: str
    titulo: str
    categoria: str | None
    dias_hasta_hito: int | None


class DashboardResponse(BaseModel):
    """Schema principal del dashboard."""

    posicion_actual: PosicionActualResponse
    hitos_proximo_dia: HitosProximoDiaResponse
    feriados_proximos: List[DiaCalendarioResponse] = Field(default_factory=list)
    hitos_importantes_proximos: List[HitoImportanteProximoResponse] = Field(
        default_factory=list
    )
    dias_habiles_restantes_mes: int = 0
