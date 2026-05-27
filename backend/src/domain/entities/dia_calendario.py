"""Entidad Día del Calendario."""
from dataclasses import dataclass
from datetime import date
from typing import Optional

from ..value_objects.dia_tipo import DiaTipo
from ..value_objects.dia_habil_numero import DiaHabilNumero


@dataclass
class DiaCalendario:
    """
    Entidad que representa un día en el calendario.

    Representa un día específico del calendario argentino con información
    sobre si es hábil, qué número de día hábil es dentro del mes, y observaciones.
    """

    fecha: date
    nombre_dia: str
    tipo: DiaTipo
    dia_habil_numero: Optional[DiaHabilNumero]
    observaciones: Optional[str] = None

    def __post_init__(self) -> None:
        """Validaciones de la entidad."""
        if not isinstance(self.fecha, date):
            raise TypeError("fecha debe ser de tipo datetime.date")

        if not isinstance(self.tipo, DiaTipo):
            raise TypeError("tipo debe ser una instancia de DiaTipo")

        # Validación de coherencia: si es hábil, debe tener número
        if self.tipo == DiaTipo.HABIL and self.dia_habil_numero is None:
            raise ValueError("Un día hábil debe tener un número de día hábil asignado")

        # Si es no hábil, no debe tener número
        if self.tipo == DiaTipo.NO_HABIL and self.dia_habil_numero is not None:
            raise ValueError("Un día no hábil no puede tener número de día hábil")

    @property
    def es_habil(self) -> bool:
        """Retorna True si el día es hábil."""
        return self.tipo.es_habil()

    @property
    def es_feriado(self) -> bool:
        """Retorna True si el día es un feriado (tiene observaciones indicando feriado)."""
        if not self.observaciones:
            return False
        return "feriado" in self.observaciones.lower()

    def __str__(self) -> str:
        tipo_str = "Hábil" if self.es_habil else "No hábil"
        dia_num = f" ({self.dia_habil_numero})" if self.dia_habil_numero else ""
        return f"{self.fecha.strftime('%d/%m/%Y')} - {self.nombre_dia} - {tipo_str}{dia_num}"

    def __repr__(self) -> str:
        return (
            f"DiaCalendario(fecha={self.fecha}, nombre_dia='{self.nombre_dia}', "
            f"tipo={self.tipo}, dia_habil_numero={self.dia_habil_numero})"
        )
