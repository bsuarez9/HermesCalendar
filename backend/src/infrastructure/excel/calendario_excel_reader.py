"""Lector de Excel para el calendario."""
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from openpyxl import load_workbook
from openpyxl.worksheet.worksheet import Worksheet

from ...domain.entities.dia_calendario import DiaCalendario
from ...domain.entities.hito_importante import HitoImportante
from ...domain.entities.hito_periodico import HitoPeriodico
from ...domain.value_objects.dia_habil_numero import DiaHabilNumero
from ...domain.value_objects.dia_tipo import DiaTipo


class CalendarioExcelReader:
    """
    Lector especializado para el archivo Excel de Calendario YPF.

    Lee las 3 hojas del Excel y convierte los datos en entidades de dominio.
    """

    def __init__(self, excel_path: str):
        """
        Constructor.

        Args:
            excel_path: Ruta al archivo Excel
        """
        self.excel_path = Path(excel_path)
        if not self.excel_path.exists():
            raise FileNotFoundError(f"No se encontró el archivo Excel: {excel_path}")

    def leer_calendario(self) -> List[DiaCalendario]:
        """
        Lee la hoja de calendario y retorna una lista de días.

        Returns:
            Lista de DiaCalendario ordenados por fecha
        """
        wb = load_workbook(self.excel_path, read_only=True, data_only=True)
        ws = wb["Calendario_Argentina_2026_Compl"]

        dias: List[DiaCalendario] = []

        # Saltar header (fila 1)
        for row in ws.iter_rows(min_row=2, values_only=True):
            if not row[0]:  # Si no hay fecha, terminar
                break

            fecha = row[0] if isinstance(row[0], datetime) else None
            if not fecha:
                continue

            nombre_dia = row[1] or ""
            tipo_str = row[2] or "No habil"
            dia_habil_num = row[3]
            observaciones = row[4]

            # Crear value objects
            tipo = DiaTipo.HABIL if tipo_str == "Habil" else DiaTipo.NO_HABIL
            dia_habil_numero = DiaHabilNumero(dia_habil_num) if dia_habil_num else None

            # Crear entidad
            dia = DiaCalendario(
                fecha=fecha.date(),
                nombre_dia=nombre_dia,
                tipo=tipo,
                dia_habil_numero=dia_habil_numero,
                observaciones=observaciones,
            )

            dias.append(dia)

        wb.close()
        return dias

    def leer_hitos_periodicos(self) -> List[HitoPeriodico]:
        """
        Lee la hoja de hitos periódicos y retorna una lista de hitos.

        Returns:
            Lista de HitoPeriodico ordenados por día hábil
        """
        wb = load_workbook(self.excel_path, read_only=True, data_only=True)
        ws = wb["Hitos_Periodicos"]

        hitos: List[HitoPeriodico] = []

        # Saltar header (fila 1)
        for row in ws.iter_rows(min_row=2, values_only=True):
            if not row[0]:  # Si no hay día hábil, terminar
                break

            dia_habil_num = row[0]
            accion = row[1]

            if not accion:
                continue

            # Crear entidad
            dia_habil = DiaHabilNumero(dia_habil_num)
            hito = HitoPeriodico(dia_habil=dia_habil, accion=accion)

            hitos.append(hito)

        wb.close()
        return sorted(hitos, key=lambda h: h.dia_habil.valor)

    def leer_hitos_importantes(self) -> List[HitoImportante]:
        """
        Lee la hoja de hitos importantes y retorna una lista de hitos.

        Returns:
            Lista de HitoImportante ordenados por fecha
        """
        wb = load_workbook(self.excel_path, read_only=True, data_only=True)
        ws = wb["Hitos_Importantes_YPF"]

        hitos: List[HitoImportante] = []

        # Saltar header (fila 1)
        for row in ws.iter_rows(min_row=2, values_only=True):
            if not row[0]:  # Si no hay fecha, terminar
                break

            fecha = row[0] if isinstance(row[0], datetime) else None
            titulo = row[1]

            if not fecha or not titulo:
                continue

            # Crear entidad
            hito = HitoImportante(fecha=fecha.date(), titulo=titulo)

            hitos.append(hito)

        wb.close()
        return sorted(hitos, key=lambda h: h.fecha)

    def leer_todo(self) -> Dict[str, List]:
        """
        Lee todas las hojas del Excel y retorna un diccionario con los datos.

        Returns:
            Diccionario con claves 'calendario', 'hitos_periodicos', 'hitos_importantes'
        """
        return {
            "calendario": self.leer_calendario(),
            "hitos_periodicos": self.leer_hitos_periodicos(),
            "hitos_importantes": self.leer_hitos_importantes(),
        }
