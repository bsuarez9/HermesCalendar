"""Interface del repositorio de hitos importantes."""
from abc import ABC, abstractmethod
from datetime import date
from typing import List, Optional
from uuid import UUID

from ..entities.hito_importante import HitoImportante


class IHitoImportanteRepository(ABC):
    """
    Interfaz para el repositorio de hitos importantes.

    Define el contrato para acceder y gestionar hitos con fecha específica.
    """

    @abstractmethod
    def obtener_por_id(self, hito_id: UUID) -> Optional[HitoImportante]:
        """
        Obtiene un hito importante por su ID.

        Args:
            hito_id: ID del hito

        Returns:
            HitoImportante si existe, None si no
        """
        pass

    @abstractmethod
    def obtener_todos(self, solo_activos: bool = True) -> List[HitoImportante]:
        """
        Obtiene todos los hitos importantes.

        Args:
            solo_activos: Si es True, solo retorna hitos activos

        Returns:
            Lista de hitos importantes ordenados por fecha
        """
        pass

    @abstractmethod
    def obtener_por_fecha(self, fecha: date) -> List[HitoImportante]:
        """
        Obtiene todos los hitos de una fecha específica.

        Args:
            fecha: Fecha a buscar

        Returns:
            Lista de hitos en esa fecha
        """
        pass

    @abstractmethod
    def obtener_rango(
        self, fecha_inicio: date, fecha_fin: date, solo_activos: bool = True
    ) -> List[HitoImportante]:
        """
        Obtiene todos los hitos en un rango de fechas.

        Args:
            fecha_inicio: Fecha de inicio (inclusive)
            fecha_fin: Fecha de fin (inclusive)
            solo_activos: Si es True, solo retorna hitos activos

        Returns:
            Lista de hitos en el rango ordenados por fecha
        """
        pass

    @abstractmethod
    def obtener_proximos(
        self, fecha_desde: date, cantidad: int = 10, solo_activos: bool = True
    ) -> List[HitoImportante]:
        """
        Obtiene los próximos N hitos a partir de una fecha.

        Args:
            fecha_desde: Fecha de inicio
            cantidad: Cantidad de hitos a retornar
            solo_activos: Si es True, solo retorna hitos activos

        Returns:
            Lista de hitos futuros ordenados por fecha
        """
        pass

    @abstractmethod
    def guardar(self, hito: HitoImportante) -> HitoImportante:
        """
        Guarda un nuevo hito importante o actualiza uno existente.

        Args:
            hito: Hito a guardar

        Returns:
            El hito guardado
        """
        pass

    @abstractmethod
    def eliminar(self, hito_id: UUID) -> bool:
        """
        Elimina un hito importante.

        Args:
            hito_id: ID del hito a eliminar

        Returns:
            True si se eliminó, False si no existía
        """
        pass

    @abstractmethod
    def obtener_por_categoria(
        self, categoria: str, solo_activos: bool = True
    ) -> List[HitoImportante]:
        """
        Obtiene hitos por categoría.

        Args:
            categoria: Categoría a filtrar
            solo_activos: Si es True, solo retorna hitos activos

        Returns:
            Lista de hitos de la categoría
        """
        pass
