"""Use cases para gestionar hitos importantes."""
from typing import List, Optional
from uuid import UUID

from ...domain.entities.hito_importante import HitoImportante
from ...domain.repositories.hito_importante_repository import IHitoImportanteRepository
from ..dtos.hito_importante_dto import (
    ActualizarHitoImportanteDTO,
    CrearHitoImportanteDTO,
    HitoImportanteDTO,
)


class CrearHitoImportanteUseCase:
    """Use case para crear un nuevo hito importante."""

    def __init__(self, hito_repo: IHitoImportanteRepository):
        """
        Constructor.

        Args:
            hito_repo: Repositorio de hitos importantes
        """
        self.hito_repo = hito_repo

    def execute(self, dto: CrearHitoImportanteDTO) -> HitoImportanteDTO:
        """
        Ejecuta el use case para crear un hito importante.

        Args:
            dto: DTO con los datos del nuevo hito

        Returns:
            DTO del hito creado
        """
        # Validar DTO
        dto.validar()

        # Crear entidad
        hito = HitoImportante(
            fecha=dto.to_date(),
            titulo=dto.titulo,
            descripcion=dto.descripcion,
            categoria=dto.categoria,
        )

        # Guardar
        hito_guardado = self.hito_repo.guardar(hito)

        # Retornar DTO
        return HitoImportanteDTO.from_entity(hito_guardado, calcular_dias=True)


class ActualizarHitoImportanteUseCase:
    """Use case para actualizar un hito importante existente."""

    def __init__(self, hito_repo: IHitoImportanteRepository):
        """
        Constructor.

        Args:
            hito_repo: Repositorio de hitos importantes
        """
        self.hito_repo = hito_repo

    def execute(self, hito_id: UUID, dto: ActualizarHitoImportanteDTO) -> HitoImportanteDTO:
        """
        Ejecuta el use case para actualizar un hito.

        Args:
            hito_id: ID del hito a actualizar
            dto: DTO con los datos a actualizar

        Returns:
            DTO del hito actualizado

        Raises:
            ValueError: Si el hito no existe
        """
        # Validar DTO
        dto.validar()

        # Obtener hito existente
        hito = self.hito_repo.obtener_por_id(hito_id)
        if not hito:
            raise ValueError(f"No se encontró el hito con ID {hito_id}")

        # Aplicar cambios
        if dto.titulo is not None:
            hito.actualizar_titulo(dto.titulo)

        if dto.descripcion is not None:
            hito.actualizar_descripcion(dto.descripcion)

        if dto.categoria is not None:
            hito.actualizar_categoria(dto.categoria)

        if dto.activo is not None:
            if dto.activo:
                hito.activar()
            else:
                hito.desactivar()

        if dto.fecha is not None:
            hito.fecha = dto.to_date()  # type: ignore

        # Guardar cambios
        hito_actualizado = self.hito_repo.guardar(hito)

        return HitoImportanteDTO.from_entity(hito_actualizado, calcular_dias=True)


class EliminarHitoImportanteUseCase:
    """Use case para eliminar un hito importante."""

    def __init__(self, hito_repo: IHitoImportanteRepository):
        """
        Constructor.

        Args:
            hito_repo: Repositorio de hitos importantes
        """
        self.hito_repo = hito_repo

    def execute(self, hito_id: UUID) -> bool:
        """
        Ejecuta el use case para eliminar un hito.

        Args:
            hito_id: ID del hito a eliminar

        Returns:
            True si se eliminó, False si no existía
        """
        return self.hito_repo.eliminar(hito_id)


class ListarHitosImportantesUseCase:
    """Use case para listar hitos importantes."""

    def __init__(self, hito_repo: IHitoImportanteRepository):
        """
        Constructor.

        Args:
            hito_repo: Repositorio de hitos importantes
        """
        self.hito_repo = hito_repo

    def execute(
        self, categoria: Optional[str] = None, solo_activos: bool = True
    ) -> List[HitoImportanteDTO]:
        """
        Ejecuta el use case para listar hitos.

        Args:
            categoria: Filtrar por categoría (opcional)
            solo_activos: Si es True, solo retorna hitos activos

        Returns:
            Lista de DTOs de hitos importantes
        """
        if categoria:
            hitos = self.hito_repo.obtener_por_categoria(
                categoria=categoria, solo_activos=solo_activos
            )
        else:
            hitos = self.hito_repo.obtener_todos(solo_activos=solo_activos)

        return [HitoImportanteDTO.from_entity(h, calcular_dias=True) for h in hitos]
