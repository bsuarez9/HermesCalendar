"""Interface del repositorio de hitos periódicos."""
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from ..entities.hito_periodico import HitoPeriodico
from ..value_objects.dia_habil_numero import DiaHabilNumero


class IHitoPeriodicoRepository(ABC):
    """
    Interfaz para el repositorio de hitos periódicos.

    Define el contrato para acceder y gestionar hitos que se repiten cada mes.
    """

    @abstractmethod
    def obtener_por_id(self, hito_id: UUID) -> Optional[HitoPeriodico]:
        """
        Obtiene un hito periódico por su ID.

        Args:
            hito_id: ID del hito

        Returns:
            HitoPeriodico si existe, None si no
        """
        pass

    @abstractmethod
    def obtener_todos(self, solo_activos: bool = True) -> List[HitoPeriodico]:
        """
        Obtiene todos los hitos periódicos.

        Args:
            solo_activos: Si es True, solo retorna hitos activos

        Returns:
            Lista de hitos periódicos ordenados por día hábil
        """
        pass

    @abstractmethod
    def obtener_por_dia_habil(self, dia_habil: DiaHabilNumero) -> List[HitoPeriodico]:
        """
        Obtiene todos los hitos de un día hábil específico.

        Args:
            dia_habil: Número de día hábil (D+1, D+2, etc.)

        Returns:
            Lista de hitos para ese día hábil
        """
        pass

    @abstractmethod
    def guardar(self, hito: HitoPeriodico) -> HitoPeriodico:
        """
        Guarda un nuevo hito periódico o actualiza uno existente.

        Args:
            hito: Hito a guardar

        Returns:
            El hito guardado
        """
        pass

    @abstractmethod
    def eliminar(self, hito_id: UUID) -> bool:
        """
        Elimina un hito periódico.

        Args:
            hito_id: ID del hito a eliminar

        Returns:
            True si se eliminó, False si no existía
        """
        pass

    @abstractmethod
    def existe_hito(self, dia_habil: DiaHabilNumero, accion: str) -> bool:
        """
        Verifica si ya existe un hito con la misma acción en el mismo día hábil.

        Args:
            dia_habil: Día hábil
            accion: Acción del hito

        Returns:
            True si existe un hito duplicado
        """
        pass
