"""DTOs para Hito Importante."""
from dataclasses import dataclass
from datetime import date as date_type
from typing import Optional
from uuid import UUID

from ...domain.entities.hito_importante import HitoImportante


@dataclass
class HitoImportanteDTO:
    """DTO para transferir datos de un hito importante."""

    id: str  # UUID como string
    fecha: str  # Formato ISO: YYYY-MM-DD
    titulo: str
    descripcion: Optional[str]
    categoria: Optional[str]
    activo: bool
    dias_hasta_hito: Optional[int] = None  # Calculado dinámicamente

    @classmethod
    def from_entity(
        cls, entity: HitoImportante, calcular_dias: bool = False
    ) -> "HitoImportanteDTO":
        """
        Convierte una entidad HitoImportante a DTO.

        Args:
            entity: Entidad de dominio
            calcular_dias: Si es True, calcula los días hasta el hito

        Returns:
            DTO con los datos de la entidad
        """
        dias_hasta = None
        if calcular_dias:
            dias_hasta = entity.dias_hasta_hito()

        return cls(
            id=str(entity.id),
            fecha=entity.fecha.isoformat(),
            titulo=entity.titulo,
            descripcion=entity.descripcion,
            categoria=entity.categoria,
            activo=entity.activo,
            dias_hasta_hito=dias_hasta,
        )


@dataclass
class CrearHitoImportanteDTO:
    """DTO para crear un nuevo hito importante."""

    fecha: str  # Formato ISO: YYYY-MM-DD
    titulo: str
    descripcion: Optional[str] = None
    categoria: Optional[str] = None

    def validar(self) -> None:
        """Valida los datos del DTO."""
        if not self.titulo or not self.titulo.strip():
            raise ValueError("El título no puede estar vacío")

        try:
            date_type.fromisoformat(self.fecha)
        except ValueError:
            raise ValueError(f"Formato de fecha inválido: {self.fecha}. Use YYYY-MM-DD")

    def to_date(self) -> date_type:
        """Convierte la fecha string a date."""
        return date_type.fromisoformat(self.fecha)


@dataclass
class ActualizarHitoImportanteDTO:
    """DTO para actualizar un hito importante existente."""

    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    categoria: Optional[str] = None
    activo: Optional[bool] = None
    fecha: Optional[str] = None  # Formato ISO: YYYY-MM-DD

    def validar(self) -> None:
        """Valida los datos del DTO."""
        if self.titulo is not None and not self.titulo.strip():
            raise ValueError("El título no puede estar vacío")

        if self.fecha is not None:
            try:
                date_type.fromisoformat(self.fecha)
            except ValueError:
                raise ValueError(f"Formato de fecha inválido: {self.fecha}. Use YYYY-MM-DD")

    def to_date(self) -> Optional[date_type]:
        """Convierte la fecha string a date si existe."""
        return date_type.fromisoformat(self.fecha) if self.fecha else None
