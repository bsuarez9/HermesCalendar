"""Value Object para el número de día hábil del mes."""
from dataclasses import dataclass


@dataclass(frozen=True)
class DiaHabilNumero:
    """Representa el número de día hábil dentro del mes (D+1, D+2, ..., D+31)."""

    valor: int

    def __post_init__(self) -> None:
        """Valida que el número de día hábil sea válido."""
        if not isinstance(self.valor, int):
            raise TypeError("El número de día hábil debe ser un entero")

        if not 1 <= self.valor <= 31:
            raise ValueError(f"El día hábil debe estar entre 1 y 31, recibido: {self.valor}")

    def __str__(self) -> str:
        return f"D+{self.valor}"

    def __repr__(self) -> str:
        return f"DiaHabilNumero(valor={self.valor})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DiaHabilNumero):
            return NotImplemented
        return self.valor == other.valor

    def __hash__(self) -> int:
        return hash(self.valor)
