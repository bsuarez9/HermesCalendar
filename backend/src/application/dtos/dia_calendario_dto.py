"""DTOs para Día del Calendario."""
from dataclasses import dataclass
from datetime import date
from typing import Optional

from ...domain.entities.dia_calendario import DiaCalendario


@dataclass
class DiaCalendarioDTO:
    """DTO para transferir datos de un día del calendario."""

    fecha: str  # Formato ISO: YYYY-MM-DD
    nombre_dia: str
    tipo: str  # "Habil" o "No habil"
    dia_habil_numero: Optional[int]
    observaciones: Optional[str]
    es_habil: bool
    es_feriado: bool

    @classmethod
    def from_entity(cls, entity: DiaCalendario) -> "DiaCalendarioDTO":
        """
        Convierte una entidad DiaCalendario a DTO.

        Args:
            entity: Entidad de dominio

        Returns:
            DTO con los datos de la entidad
        """
        return cls(
            fecha=entity.fecha.isoformat(),
            nombre_dia=entity.nombre_dia,
            tipo=entity.tipo.value,
            dia_habil_numero=entity.dia_habil_numero.valor if entity.dia_habil_numero else None,
            observaciones=entity.observaciones,
            es_habil=entity.es_habil,
            es_feriado=entity.es_feriado,
        )
