"""Modelo de base de datos para HitoPeriodico."""
from sqlalchemy import Boolean, Column, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.types import TypeDecorator
import uuid

from ...config.database import Base


class GUID(TypeDecorator):
    """Type decorator para UUID que funciona en SQLite y PostgreSQL."""

    impl = String
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(PG_UUID())
        else:
            return dialect.type_descriptor(String(36))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == "postgresql":
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return str(value)
            else:
                return str(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        if not isinstance(value, uuid.UUID):
            value = uuid.UUID(value)
        return value


class HitoPeriodicoModel(Base):
    """Modelo de base de datos para hitos periódicos."""

    __tablename__ = "hitos_periodicos"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    dia_habil = Column(Integer, nullable=False, index=True)
    accion = Column(String(255), nullable=False)
    descripcion = Column(Text, nullable=True)
    activo = Column(Boolean, default=True, nullable=False)

    def __repr__(self) -> str:
        return f"<HitoPeriodicoModel(id={self.id}, dia_habil={self.dia_habil}, accion='{self.accion}')>"
