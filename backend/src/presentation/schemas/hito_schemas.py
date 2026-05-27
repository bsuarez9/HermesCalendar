"""Pydantic schemas para hitos."""
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class HitoPeriodicoResponse(BaseModel):
    """Schema de respuesta para hito periódico."""

    id: str
    dia_habil: int = Field(..., ge=1, le=31, description="Número de día hábil (D+X)")
    accion: str = Field(..., min_length=1, description="Descripción de la acción")
    descripcion: Optional[str] = Field(None, description="Descripción adicional")
    activo: bool = Field(True, description="Indica si el hito está activo")

    class Config:
        from_attributes = True


class HitoPeriodicoCreate(BaseModel):
    """Schema para crear un nuevo hito periódico."""

    dia_habil: int = Field(..., ge=1, le=31, description="Número de día hábil (D+X)")
    accion: str = Field(..., min_length=1, description="Descripción de la acción")
    descripcion: Optional[str] = Field(None, description="Descripción adicional")


class HitoPeriodicoUpdate(BaseModel):
    """Schema para actualizar un hito periódico."""

    accion: Optional[str] = Field(None, min_length=1)
    descripcion: Optional[str] = None
    activo: Optional[bool] = None


class HitoImportanteResponse(BaseModel):
    """Schema de respuesta para hito importante."""

    id: str
    fecha: str = Field(..., description="Fecha en formato ISO (YYYY-MM-DD)")
    titulo: str = Field(..., min_length=1)
    descripcion: Optional[str] = None
    categoria: Optional[str] = None
    activo: bool = True
    dias_hasta_hito: Optional[int] = None

    class Config:
        from_attributes = True


class HitoImportanteCreate(BaseModel):
    """Schema para crear un nuevo hito importante."""

    fecha: str = Field(..., description="Fecha en formato ISO (YYYY-MM-DD)")
    titulo: str = Field(..., min_length=1)
    descripcion: Optional[str] = None
    categoria: Optional[str] = None

    @field_validator("fecha")
    @classmethod
    def validate_fecha_format(cls, v: str) -> str:
        """Valida que la fecha esté en formato ISO."""
        from datetime import date

        try:
            date.fromisoformat(v)
        except ValueError:
            raise ValueError("Formato de fecha inválido. Use YYYY-MM-DD")
        return v


class HitoImportanteUpdate(BaseModel):
    """Schema para actualizar un hito importante."""

    titulo: Optional[str] = Field(None, min_length=1)
    descripcion: Optional[str] = None
    categoria: Optional[str] = None
    activo: Optional[bool] = None
    fecha: Optional[str] = Field(None, description="Fecha en formato ISO (YYYY-MM-DD)")

    @field_validator("fecha")
    @classmethod
    def validate_fecha_format(cls, v: Optional[str]) -> Optional[str]:
        """Valida que la fecha esté en formato ISO."""
        if v is None:
            return v

        from datetime import date

        try:
            date.fromisoformat(v)
        except ValueError:
            raise ValueError("Formato de fecha inválido. Use YYYY-MM-DD")
        return v
