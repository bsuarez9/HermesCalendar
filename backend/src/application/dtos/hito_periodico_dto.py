"""DTOs para Hito Periódico."""
from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from ...domain.entities.hito_periodico import HitoPeriodico
from ...domain.value_objects.dia_habil_numero import DiaHabilNumero


@dataclass
class HitoPeriodicoDTO:
    """DTO para transferir datos de un hito periódico."""

    id: str  # UUID como string
    dia_habil: int
    accion: str
    descripcion: Optional[str]
    activo: bool

    @classmethod
    def from_entity(cls, entity: HitoPeriodico) -> "HitoPeriodicoDTO":
        """
        Convierte una entidad HitoPeriodico a DTO.

        Args:
            entity: Entidad de dominio

        Returns:
            DTO con los datos de la entidad
        """
        return cls(
            id=str(entity.id),
            dia_habil=entity.dia_habil.valor,
            accion=entity.accion,
            descripcion=entity.descripcion,
            activo=entity.activo,
        )


@dataclass
class CrearHitoPeriodicoDTO:
    """DTO para crear un nuevo hito periódico."""

    dia_habil: int
    accion: str
    descripcion: Optional[str] = None

    def validar(self) -> None:
        """Valida los datos del DTO."""
        if not 1 <= self.dia_habil <= 31:
            raise ValueError("El día hábil debe estar entre 1 y 31")

        if not self.accion or not self.accion.strip():
            raise ValueError("La acción no puede estar vacía")


@dataclass
class ActualizarHitoPeriodicoDTO:
    """DTO para actualizar un hito periódico existente."""

    accion: Optional[str] = None
    descripcion: Optional[str] = None
    activo: Optional[bool] = None

    def validar(self) -> None:
        """Valida los datos del DTO."""
        if self.accion is not None and not self.accion.strip():
            raise ValueError("La acción no puede estar vacía")
