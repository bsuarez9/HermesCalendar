"""Interface del repositorio de calendario."""
from abc import ABC, abstractmethod
from datetime import date
from typing import List, Optional

from ..entities.dia_calendario import DiaCalendario
from ..value_objects.dia_habil_numero import DiaHabilNumero


class ICalendarioRepository(ABC):
    """
    Interfaz para el repositorio de calendario.

    Define el contrato para acceder a los datos del calendario.
    La implementación puede venir de Excel, base de datos, API, etc.
    """

    @abstractmethod
    def obtener_dia(self, fecha: date) -> Optional[DiaCalendario]:
        """
        Obtiene un día específico del calendario.

        Args:
            fecha: Fecha a buscar

        Returns:
            DiaCalendario si existe, None si no
        """
        pass

    @abstractmethod
    def obtener_dias_rango(self, fecha_inicio: date, fecha_fin: date) -> List[DiaCalendario]:
        """
        Obtiene todos los días en un rango de fechas.

        Args:
            fecha_inicio: Fecha de inicio (inclusive)
            fecha_fin: Fecha de fin (inclusive)

        Returns:
            Lista de días en el rango
        """
        pass

    @abstractmethod
    def obtener_dias_habiles_mes(self, anio: int, mes: int) -> List[DiaCalendario]:
        """
        Obtiene todos los días hábiles de un mes específico.

        Args:
            anio: Año
            mes: Mes (1-12)

        Returns:
            Lista de días hábiles del mes ordenados por fecha
        """
        pass

    @abstractmethod
    def obtener_dia_por_numero_habil(
        self, anio: int, mes: int, dia_habil: DiaHabilNumero
    ) -> Optional[DiaCalendario]:
        """
        Obtiene el día calendario que corresponde a un número de día hábil específico del mes.

        Ejemplo: para obtener el D+7 de Enero 2026
        obtener_dia_por_numero_habil(2026, 1, DiaHabilNumero(7))

        Args:
            anio: Año
            mes: Mes (1-12)
            dia_habil: Número de día hábil (D+1, D+2, etc.)

        Returns:
            DiaCalendario correspondiente o None si no existe
        """
        pass

    @abstractmethod
    def obtener_feriados_proximos(
        self, fecha_desde: date, cantidad: int = 5
    ) -> List[DiaCalendario]:
        """
        Obtiene los próximos feriados a partir de una fecha.

        Args:
            fecha_desde: Fecha de inicio
            cantidad: Cantidad de feriados a retornar

        Returns:
            Lista de feriados ordenados por fecha
        """
        pass

    @abstractmethod
    def obtener_proximo_dia_habil(self, fecha: date) -> Optional[DiaCalendario]:
        """
        Obtiene el próximo día hábil a partir de una fecha (no incluyéndola).

        Args:
            fecha: Fecha de referencia

        Returns:
            El próximo día hábil o None si no hay
        """
        pass

    @abstractmethod
    def contar_dias_habiles_hasta(self, fecha_inicio: date, fecha_fin: date) -> int:
        """
        Cuenta cuántos días hábiles hay entre dos fechas.

        Args:
            fecha_inicio: Fecha de inicio (inclusive)
            fecha_fin: Fecha de fin (inclusive)

        Returns:
            Número de días hábiles
        """
        pass
