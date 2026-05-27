"""Entidad Hito Periódico."""
from dataclasses import dataclass
from typing import Optional
from uuid import UUID, uuid4

from ..value_objects.dia_habil_numero import DiaHabilNumero


@dataclass
class HitoPeriodico:
    """
    Entidad que representa un hito que se repite todos los meses en un día hábil específico.

    Ejemplos:
    - D+7: EERR MyD - Corpo
    - D+10: CAS
    - D+12: Arbol Refinería
    """

    dia_habil: DiaHabilNumero
    accion: str
    id: UUID
    descripcion: Optional[str] = None
    activo: bool = True

    def __init__(
        self,
        dia_habil: DiaHabilNumero,
        accion: str,
        id: Optional[UUID] = None,
        descripcion: Optional[str] = None,
        activo: bool = True,
    ):
        """
        Constructor del hito periódico.

        Args:
            dia_habil: Día hábil del mes en el que se debe cumplir el hito
            accion: Descripción de la acción a realizar
            id: Identificador único (se genera automáticamente si no se proporciona)
            descripcion: Descripción adicional opcional
            activo: Indica si el hito está activo
        """
        self.id = id or uuid4()
        self.dia_habil = dia_habil
        self.accion = self._validar_accion(accion)
        self.descripcion = descripcion
        self.activo = activo

    @staticmethod
    def _validar_accion(accion: str) -> str:
        """Valida que la acción no esté vacía."""
        if not accion or not accion.strip():
            raise ValueError("La acción no puede estar vacía")
        return accion.strip()

    def desactivar(self) -> None:
        """Desactiva el hito periódico."""
        self.activo = False

    def activar(self) -> None:
        """Activa el hito periódico."""
        self.activo = True

    def actualizar_accion(self, nueva_accion: str) -> None:
        """Actualiza la descripción de la acción."""
        self.accion = self._validar_accion(nueva_accion)

    def actualizar_descripcion(self, nueva_descripcion: Optional[str]) -> None:
        """Actualiza la descripción adicional."""
        self.descripcion = nueva_descripcion

    def __str__(self) -> str:
        estado = "✓" if self.activo else "✗"
        return f"{estado} {self.dia_habil}: {self.accion}"

    def __repr__(self) -> str:
        return (
            f"HitoPeriodico(id={self.id}, dia_habil={self.dia_habil}, "
            f"accion='{self.accion}', activo={self.activo})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, HitoPeriodico):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)
