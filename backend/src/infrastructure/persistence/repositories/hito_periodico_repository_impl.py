"""Implementación del repositorio de hitos periódicos usando SQLAlchemy."""
from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from ....domain.entities.hito_periodico import HitoPeriodico
from ....domain.repositories.hito_periodico_repository import IHitoPeriodicoRepository
from ....domain.value_objects.dia_habil_numero import DiaHabilNumero
from ..models.hito_periodico_model import HitoPeriodicoModel


class HitoPeriodicoRepositoryImpl(IHitoPeriodicoRepository):
    """Implementación del repositorio de hitos periódicos con SQLAlchemy."""

    def __init__(self, session: Session):
        """
        Constructor.

        Args:
            session: Sesión de SQLAlchemy
        """
        self.session = session

    def obtener_por_id(self, hito_id: UUID) -> Optional[HitoPeriodico]:
        """Obtiene un hito periódico por su ID."""
        model = self.session.query(HitoPeriodicoModel).filter_by(id=hito_id).first()
        return self._to_entity(model) if model else None

    def obtener_todos(self, solo_activos: bool = True) -> List[HitoPeriodico]:
        """Obtiene todos los hitos periódicos."""
        query = self.session.query(HitoPeriodicoModel)

        if solo_activos:
            query = query.filter_by(activo=True)

        models = query.order_by(HitoPeriodicoModel.dia_habil).all()
        return [self._to_entity(m) for m in models]

    def obtener_por_dia_habil(self, dia_habil: DiaHabilNumero) -> List[HitoPeriodico]:
        """Obtiene todos los hitos de un día hábil específico."""
        models = (
            self.session.query(HitoPeriodicoModel)
            .filter_by(dia_habil=dia_habil.valor, activo=True)
            .all()
        )
        return [self._to_entity(m) for m in models]

    def guardar(self, hito: HitoPeriodico) -> HitoPeriodico:
        """Guarda un nuevo hito periódico o actualiza uno existente."""
        # Buscar si ya existe
        model = self.session.query(HitoPeriodicoModel).filter_by(id=hito.id).first()

        if model:
            # Actualizar existente
            model.dia_habil = hito.dia_habil.valor
            model.accion = hito.accion
            model.descripcion = hito.descripcion
            model.activo = hito.activo
        else:
            # Crear nuevo
            model = HitoPeriodicoModel(
                id=hito.id,
                dia_habil=hito.dia_habil.valor,
                accion=hito.accion,
                descripcion=hito.descripcion,
                activo=hito.activo,
            )
            self.session.add(model)

        self.session.commit()
        self.session.refresh(model)

        return self._to_entity(model)

    def eliminar(self, hito_id: UUID) -> bool:
        """Elimina un hito periódico."""
        model = self.session.query(HitoPeriodicoModel).filter_by(id=hito_id).first()

        if not model:
            return False

        self.session.delete(model)
        self.session.commit()
        return True

    def existe_hito(self, dia_habil: DiaHabilNumero, accion: str) -> bool:
        """Verifica si ya existe un hito con la misma acción en el mismo día hábil."""
        count = (
            self.session.query(HitoPeriodicoModel)
            .filter_by(dia_habil=dia_habil.valor, accion=accion)
            .count()
        )
        return count > 0

    @staticmethod
    def _to_entity(model: HitoPeriodicoModel) -> HitoPeriodico:
        """Convierte un modelo de DB a entidad de dominio."""
        return HitoPeriodico(
            id=model.id,
            dia_habil=DiaHabilNumero(model.dia_habil),
            accion=model.accion,
            descripcion=model.descripcion,
            activo=model.activo,
        )
