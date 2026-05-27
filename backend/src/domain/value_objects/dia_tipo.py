"""Value Object para el tipo de día."""
from enum import Enum


class DiaTipo(str, Enum):
    """Tipos de día en el calendario."""

    HABIL = "Habil"
    NO_HABIL = "No habil"

    def es_habil(self) -> bool:
        """Retorna True si el día es hábil."""
        return self == DiaTipo.HABIL
