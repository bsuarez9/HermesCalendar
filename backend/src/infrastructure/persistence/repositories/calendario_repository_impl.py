"""Implementación del repositorio de calendario usando datos cargados en memoria desde Excel."""
from datetime import date
from typing import Dict, List, Optional

from ....domain.entities.dia_calendario import DiaCalendario
from ....domain.repositories.calendario_repository import ICalendarioRepository
from ....domain.value_objects.dia_habil_numero import DiaHabilNumero
from ...excel.calendario_excel_reader import CalendarioExcelReader


class CalendarioRepositoryImpl(ICalendarioRepository):
    """
    Implementación del repositorio de calendario.

    Esta implementación carga el calendario desde Excel una sola vez
    y lo mantiene en memoria para consultas rápidas.
    """

    def __init__(self, excel_path: str):
        """
        Constructor.

        Args:
            excel_path: Ruta al archivo Excel
        """
        self.excel_reader = CalendarioExcelReader(excel_path)
        self._calendario: List[DiaCalendario] = []
        self._indice_fechas: Dict[date, DiaCalendario] = {}
        self._cargar_calendario()

    def _cargar_calendario(self) -> None:
        """Carga el calendario desde Excel y construye índices."""
        self._calendario = self.excel_reader.leer_calendario()

        # Construir índice por fecha para búsquedas rápidas
        self._indice_fechas = {dia.fecha: dia for dia in self._calendario}

    def obtener_dia(self, fecha: date) -> Optional[DiaCalendario]:
        """Obtiene un día específico del calendario."""
        return self._indice_fechas.get(fecha)

    def obtener_dias_rango(self, fecha_inicio: date, fecha_fin: date) -> List[DiaCalendario]:
        """Obtiene todos los días en un rango de fechas."""
        return [
            dia
            for dia in self._calendario
            if fecha_inicio <= dia.fecha <= fecha_fin
        ]

    def obtener_dias_habiles_mes(self, anio: int, mes: int) -> List[DiaCalendario]:
        """Obtiene todos los días hábiles de un mes específico."""
        return [
            dia
            for dia in self._calendario
            if dia.fecha.year == anio and dia.fecha.month == mes and dia.es_habil
        ]

    def obtener_dia_por_numero_habil(
        self, anio: int, mes: int, dia_habil: DiaHabilNumero
    ) -> Optional[DiaCalendario]:
        """Obtiene el día calendario que corresponde a un número de día hábil específico del mes."""
        for dia in self._calendario:
            if (
                dia.fecha.year == anio
                and dia.fecha.month == mes
                and dia.dia_habil_numero == dia_habil
            ):
                return dia
        return None

    def obtener_feriados_proximos(
        self, fecha_desde: date, cantidad: int = 5
    ) -> List[DiaCalendario]:
        """Obtiene los próximos feriados a partir de una fecha."""
        feriados = [
            dia
            for dia in self._calendario
            if dia.fecha >= fecha_desde and dia.es_feriado
        ]
        return feriados[:cantidad]

    def obtener_proximo_dia_habil(self, fecha: date) -> Optional[DiaCalendario]:
        """Obtiene el próximo día hábil a partir de una fecha (no incluyéndola)."""
        for dia in self._calendario:
            if dia.fecha > fecha and dia.es_habil:
                return dia
        return None

    def contar_dias_habiles_hasta(self, fecha_inicio: date, fecha_fin: date) -> int:
        """Cuenta cuántos días hábiles hay entre dos fechas."""
        return len([
            dia
            for dia in self._calendario
            if fecha_inicio <= dia.fecha <= fecha_fin and dia.es_habil
        ])
