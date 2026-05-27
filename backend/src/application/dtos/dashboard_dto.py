"""DTOs para el Dashboard."""
from dataclasses import dataclass, field
from typing import List

from .dia_calendario_dto import DiaCalendarioDTO
from .hito_importante_dto import HitoImportanteDTO
from .hito_periodico_dto import HitoPeriodicoDTO


@dataclass
class PosicionActualDTO:
    """DTO para mostrar la posición actual en el mes."""

    dia_habil_actual: int
    proximo_dia_habil: int
    fecha_actual: str  # ISO format
    fecha_proximo_dia_habil: str  # ISO format


@dataclass
class HitosProximoDiaDTO:
    """DTO para mostrar los hitos del próximo día hábil."""

    dia_habil: int
    fecha: str
    hitos_periodicos: List[HitoPeriodicoDTO] = field(default_factory=list)


@dataclass
class DashboardDTO:
    """DTO principal del dashboard con toda la información necesaria."""

    posicion_actual: PosicionActualDTO
    hitos_proximo_dia: HitosProximoDiaDTO
    feriados_proximos: List[DiaCalendarioDTO] = field(default_factory=list)
    hitos_importantes_proximos: List[HitoImportanteDTO] = field(default_factory=list)
    dias_habiles_restantes_mes: int = 0
