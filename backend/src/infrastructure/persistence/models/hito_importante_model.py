"""Modelo de base de datos para HitoImportante."""
from datetime import date

from sqlalchemy import Boolean, Column, Date, String, Text
import uuid

from ...config.database import Base
from .hito_periodico_model import GUID


class HitoImportanteModel(Base):
    """Modelo de base de datos para hitos importantes."""

    __tablename__ = "hitos_importantes"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    fecha = Column(Date, nullable=False, index=True)
    titulo = Column(String(255), nullable=False)
    descripcion = Column(Text, nullable=True)
    categoria = Column(String(100), nullable=True, index=True)
    activo = Column(Boolean, default=True, nullable=False)

    def __repr__(self) -> str:
        return f"<HitoImportanteModel(id={self.id}, fecha={self.fecha}, titulo='{self.titulo}')>"
