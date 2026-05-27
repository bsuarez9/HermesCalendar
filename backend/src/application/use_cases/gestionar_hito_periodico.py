"""Use cases para gestionar hitos periódicos."""
from typing import List
from uuid import UUID

from ...domain.entities.hito_periodico import HitoPeriodico
from ...domain.repositories.hito_periodico_repository import IHitoPeriodicoRepository
from ...domain.value_objects.dia_habil_numero import DiaHabilNumero
from ..dtos.hito_periodico_dto import (
    ActualizarHitoPeriodicoDTO,
    CrearHitoPeriodicoDTO,
    HitoPeriodicoDTO,
)


class CrearHitoPeriodicoUseCase:
    """Use case para crear un nuevo hito periódico."""

    def __init__(self, hito_repo: IHitoPeriodicoRepository):
        """
        Constructor.

        Args:
            hito_repo: Repositorio de hitos periódicos
        """
        self.hito_repo = hito_repo

    def execute(self, dto: CrearHitoPeriodicoDTO) -> HitoPeriodicoDTO:
        """
        Ejecuta el use case para crear un hito periódico.

        Args:
            dto: DTO con los datos del nuevo hito

        Returns:
            DTO del hito creado

        Raises:
            ValueError: Si ya existe un hito con la misma acción en ese día
        """
        # Validar DTO
        dto.validar()

        # Crear value object
        dia_habil = DiaHabilNumero(dto.dia_habil)

        # Verificar que no exista un hito duplicado
        if self.hito_repo.existe_hito(dia_habil, dto.accion):
            raise ValueError(
                f"Ya existe un hito con la acción '{dto.accion}' en el día {dia_habil}"
            )

        # Crear entidad
        hito = HitoPeriodico(
            dia_habil=dia_habil, accion=dto.accion, descripcion=dto.descripcion
        )

        # Guardar
        hito_guardado = self.hito_repo.guardar(hito)

        # Retornar DTO
        return HitoPeriodicoDTO.from_entity(hito_guardado)


class ActualizarHitoPeriodicoUseCase:
    """Use case para actualizar un hito periódico existente."""

    def __init__(self, hito_repo: IHitoPeriodicoRepository):
        """
        Constructor.

        Args:
            hito_repo: Repositorio de hitos periódicos
        """
        self.hito_repo = hito_repo

    def execute(self, hito_id: UUID, dto: ActualizarHitoPeriodicoDTO) -> HitoPeriodicoDTO:
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
        if dto.accion is not None:
            hito.actualizar_accion(dto.accion)

        if dto.descripcion is not None:
            hito.actualizar_descripcion(dto.descripcion)

        if dto.activo is not None:
            if dto.activo:
                hito.activar()
            else:
                hito.desactivar()

        # Guardar cambios
        hito_actualizado = self.hito_repo.guardar(hito)

        return HitoPeriodicoDTO.from_entity(hito_actualizado)


class EliminarHitoPeriodicoUseCase:
    """Use case para eliminar un hito periódico."""

    def __init__(self, hito_repo: IHitoPeriodicoRepository):
        """
        Constructor.

        Args:
            hito_repo: Repositorio de hitos periódicos
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


class ListarHitosPeriodicosUseCase:
    """Use case para listar todos los hitos periódicos."""

    def __init__(self, hito_repo: IHitoPeriodicoRepository):
        """
        Constructor.

        Args:
            hito_repo: Repositorio de hitos periódicos
        """
        self.hito_repo = hito_repo

    def execute(self, solo_activos: bool = True) -> List[HitoPeriodicoDTO]:
        """
        Ejecuta el use case para listar hitos.

        Args:
            solo_activos: Si es True, solo retorna hitos activos

        Returns:
            Lista de DTOs de hitos periódicos
        """
        hitos = self.hito_repo.obtener_todos(solo_activos=solo_activos)
        return [HitoPeriodicoDTO.from_entity(h) for h in hitos]
