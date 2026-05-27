"""Entidad Hito Importante."""
from dataclasses import dataclass
from datetime import date
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class HitoImportante:
    """
    Entidad que representa un hito importante con fecha específica (no recurrente).

    Ejemplos:
    - 02/06/2026: WEBAPP Hermes
    - 02/06/2026: Reunión con Max (VP)
    - 01/09/2026: Migración de CILP & CIE a SIBE
    """

    fecha: date
    titulo: str
    id: UUID
    descripcion: Optional[str] = None
    categoria: Optional[str] = None
    activo: bool = True

    def __init__(
        self,
        fecha: date,
        titulo: str,
        id: Optional[UUID] = None,
        descripcion: Optional[str] = None,
        categoria: Optional[str] = None,
        activo: bool = True,
    ):
        """
        Constructor del hito importante.

        Args:
            fecha: Fecha específica del hito
            titulo: Título del hito
            id: Identificador único (se genera automáticamente si no se proporciona)
            descripcion: Descripción adicional opcional
            categoria: Categoría del hito (ej: "Reunión", "Proyecto", "Migración")
            activo: Indica si el hito está activo
        """
        if not isinstance(fecha, date):
            raise TypeError("fecha debe ser de tipo datetime.date")

        self.id = id or uuid4()
        self.fecha = fecha
        self.titulo = self._validar_titulo(titulo)
        self.descripcion = descripcion
        self.categoria = categoria
        self.activo = activo

    @staticmethod
    def _validar_titulo(titulo: str) -> str:
        """Valida que el título no esté vacío."""
        if not titulo or not titulo.strip():
            raise ValueError("El título no puede estar vacío")
        return titulo.strip()

    def es_futuro(self, fecha_referencia: Optional[date] = None) -> bool:
        """
        Determina si el hito es futuro respecto a una fecha de referencia.

        Args:
            fecha_referencia: Fecha de referencia (por defecto hoy)

        Returns:
            True si el hito es futuro
        """
        from datetime import date as date_module

        ref = fecha_referencia or date_module.today()
        return self.fecha > ref

    def dias_hasta_hito(self, fecha_referencia: Optional[date] = None) -> int:
        """
        Calcula cuántos días faltan para el hito.

        Args:
            fecha_referencia: Fecha de referencia (por defecto hoy)

        Returns:
            Número de días (negativo si ya pasó)
        """
        from datetime import date as date_module

        ref = fecha_referencia or date_module.today()
        return (self.fecha - ref).days

    def desactivar(self) -> None:
        """Desactiva el hito."""
        self.activo = False

    def activar(self) -> None:
        """Activa el hito."""
        self.activo = True

    def actualizar_titulo(self, nuevo_titulo: str) -> None:
        """Actualiza el título del hito."""
        self.titulo = self._validar_titulo(nuevo_titulo)

    def actualizar_descripcion(self, nueva_descripcion: Optional[str]) -> None:
        """Actualiza la descripción."""
        self.descripcion = nueva_descripcion

    def actualizar_categoria(self, nueva_categoria: Optional[str]) -> None:
        """Actualiza la categoría."""
        self.categoria = nueva_categoria

    def __str__(self) -> str:
        estado = "✓" if self.activo else "✗"
        categoria_str = f" [{self.categoria}]" if self.categoria else ""
        return f"{estado} {self.fecha.strftime('%d/%m/%Y')}{categoria_str}: {self.titulo}"

    def __repr__(self) -> str:
        return (
            f"HitoImportante(id={self.id}, fecha={self.fecha}, "
            f"titulo='{self.titulo}', categoria='{self.categoria}', activo={self.activo})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, HitoImportante):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)
