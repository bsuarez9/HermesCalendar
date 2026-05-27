"""Implementación del repositorio de hitos importantes usando SQLAlchemy."""
from datetime import date
from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from ....domain.entities.hito_importante import HitoImportante
from ....domain.repositories.hito_importante_repository import IHitoImportanteRepository
from ..models.hito_importante_model import HitoImportanteModel


class HitoImportanteRepositoryImpl(IHitoImportanteRepository):
    """Implementación del repositorio de hitos importantes con SQLAlchemy."""

    def __init__(self, session: Session):
        """
        Constructor.

        Args:
            session: Sesión de SQLAlchemy
        """
        self.session = session

    def obtener_por_id(self, hito_id: UUID) -> Optional[HitoImportante]:
        """Obtiene un hito importante por su ID."""
        model = self.session.query(HitoImportanteModel).filter_by(id=hito_id).first()
        return self._to_entity(model) if model else None

    def obtener_todos(self, solo_activos: bool = True) -> List[HitoImportante]:
        """Obtiene todos los hitos importantes."""
        query = self.session.query(HitoImportanteModel)

        if solo_activos:
            query = query.filter_by(activo=True)

        models = query.order_by(HitoImportanteModel.fecha).all()
        return [self._to_entity(m) for m in models]

    def obtener_por_fecha(self, fecha: date) -> List[HitoImportante]:
        """Obtiene todos los hitos de una fecha específica."""
        models = (
            self.session.query(HitoImportanteModel)
            .filter_by(fecha=fecha, activo=True)
            .all()
        )
        return [self._to_entity(m) for m in models]

    def obtener_rango(
        self, fecha_inicio: date, fecha_fin: date, solo_activos: bool = True
    ) -> List[HitoImportante]:
        """Obtiene todos los hitos en un rango de fechas."""
        query = self.session.query(HitoImportanteModel).filter(
            HitoImportanteModel.fecha >= fecha_inicio,
            HitoImportanteModel.fecha <= fecha_fin,
        )

        if solo_activos:
            query = query.filter_by(activo=True)

        models = query.order_by(HitoImportanteModel.fecha).all()
        return [self._to_entity(m) for m in models]

    def obtener_proximos(
        self, fecha_desde: date, cantidad: int = 10, solo_activos: bool = True
    ) -> List[HitoImportante]:
        """Obtiene los próximos N hitos a partir de una fecha."""
        query = self.session.query(HitoImportanteModel).filter(
            HitoImportanteModel.fecha >= fecha_desde
        )

        if solo_activos:
            query = query.filter_by(activo=True)

        models = query.order_by(HitoImportanteModel.fecha).limit(cantidad).all()
        return [self._to_entity(m) for m in models]

    def guardar(self, hito: HitoImportante) -> HitoImportante:
        """Guarda un nuevo hito importante o actualiza uno existente."""
        # Buscar si ya existe
        model = self.session.query(HitoImportanteModel).filter_by(id=hito.id).first()

        if model:
            # Actualizar existente
            model.fecha = hito.fecha
            model.titulo = hito.titulo
            model.descripcion = hito.descripcion
            model.categoria = hito.categoria
            model.activo = hito.activo
        else:
            # Crear nuevo
            model = HitoImportanteModel(
                id=hito.id,
                fecha=hito.fecha,
                titulo=hito.titulo,
                descripcion=hito.descripcion,
                categoria=hito.categoria,
                activo=hito.activo,
            )
            self.session.add(model)

        self.session.commit()
        self.session.refresh(model)

        return self._to_entity(model)

    def eliminar(self, hito_id: UUID) -> bool:
        """Elimina un hito importante."""
        model = self.session.query(HitoImportanteModel).filter_by(id=hito_id).first()

        if not model:
            return False

        self.session.delete(model)
        self.session.commit()
        return True

    def obtener_por_categoria(
        self, categoria: str, solo_activos: bool = True
    ) -> List[HitoImportante]:
        """Obtiene hitos por categoría."""
        query = self.session.query(HitoImportanteModel).filter_by(categoria=categoria)

        if solo_activos:
            query = query.filter_by(activo=True)

        models = query.order_by(HitoImportanteModel.fecha).all()
        return [self._to_entity(m) for m in models]

    @staticmethod
    def _to_entity(model: HitoImportanteModel) -> HitoImportante:
        """Convierte un modelo de DB a entidad de dominio."""
        return HitoImportante(
            id=model.id,
            fecha=model.fecha,
            titulo=model.titulo,
            descripcion=model.descripcion,
            categoria=model.categoria,
            activo=model.activo,
        )
