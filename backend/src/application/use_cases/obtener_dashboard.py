"""Use case para obtener datos del dashboard."""
from datetime import date
from typing import List

from ...domain.repositories.calendario_repository import ICalendarioRepository
from ...domain.repositories.hito_importante_repository import IHitoImportanteRepository
from ...domain.repositories.hito_periodico_repository import IHitoPeriodicoRepository
from ...domain.services.calendario_service import CalendarioService
from ..dtos.dashboard_dto import (
    DashboardDTO,
    HitosProximoDiaDTO,
    PosicionActualDTO,
)
from ..dtos.dia_calendario_dto import DiaCalendarioDTO
from ..dtos.hito_importante_dto import HitoImportanteDTO
from ..dtos.hito_periodico_dto import HitoPeriodicoDTO


class ObtenerDashboardUseCase:
    """
    Use case para obtener todos los datos necesarios para el dashboard.

    Este use case orquesta múltiples operaciones para consolidar
    toda la información que necesita el dashboard principal.
    """

    def __init__(
        self,
        calendario_repo: ICalendarioRepository,
        hito_periodico_repo: IHitoPeriodicoRepository,
        hito_importante_repo: IHitoImportanteRepository,
        calendario_service: CalendarioService,
    ):
        """
        Constructor del use case.

        Args:
            calendario_repo: Repositorio de calendario
            hito_periodico_repo: Repositorio de hitos periódicos
            hito_importante_repo: Repositorio de hitos importantes
            calendario_service: Servicio de dominio del calendario
        """
        self.calendario_repo = calendario_repo
        self.hito_periodico_repo = hito_periodico_repo
        self.hito_importante_repo = hito_importante_repo
        self.calendario_service = calendario_service

    def execute(self) -> DashboardDTO:
        """
        Ejecuta el use case y retorna los datos del dashboard.

        Returns:
            DTO con toda la información del dashboard
        """
        # 1. Obtener posición actual en el mes
        posicion_actual = self._obtener_posicion_actual()

        # 2. Obtener hitos del próximo día hábil
        hitos_proximo_dia = self._obtener_hitos_proximo_dia()

        # 3. Obtener próximos feriados
        feriados_proximos = self._obtener_feriados_proximos()

        # 4. Obtener hitos importantes próximos
        hitos_importantes_proximos = self._obtener_hitos_importantes_proximos()

        # 5. Calcular días hábiles restantes en el mes
        dias_habiles_restantes = len(
            self.calendario_service.obtener_dias_habiles_restantes_mes()
        )

        return DashboardDTO(
            posicion_actual=posicion_actual,
            hitos_proximo_dia=hitos_proximo_dia,
            feriados_proximos=feriados_proximos,
            hitos_importantes_proximos=hitos_importantes_proximos,
            dias_habiles_restantes_mes=dias_habiles_restantes,
        )

    def _obtener_posicion_actual(self) -> PosicionActualDTO:
        """Obtiene la posición actual en el mes (D+X)."""
        dia_actual_numero, proximo_dia_numero = self.calendario_service.calcular_posicion_en_mes()

        dia_actual = self.calendario_service.obtener_dia_habil_actual()
        proximo_dia = self.calendario_repo.obtener_proximo_dia_habil(date.today())

        fecha_proximo = proximo_dia.fecha if proximo_dia else dia_actual.fecha

        return PosicionActualDTO(
            dia_habil_actual=dia_actual_numero.valor,
            proximo_dia_habil=proximo_dia_numero.valor,
            fecha_actual=dia_actual.fecha.isoformat(),
            fecha_proximo_dia_habil=fecha_proximo.isoformat(),
        )

    def _obtener_hitos_proximo_dia(self) -> HitosProximoDiaDTO:
        """Obtiene los hitos del próximo día hábil."""
        _, proximo_dia_numero = self.calendario_service.calcular_posicion_en_mes()

        # Obtener hitos periódicos para ese día
        hitos_entities = self.hito_periodico_repo.obtener_por_dia_habil(proximo_dia_numero)
        hitos_dtos = [HitoPeriodicoDTO.from_entity(h) for h in hitos_entities if h.activo]

        # Obtener la fecha del próximo día hábil
        proximo_dia = self.calendario_repo.obtener_proximo_dia_habil(date.today())
        fecha_proximo = proximo_dia.fecha if proximo_dia else date.today()

        return HitosProximoDiaDTO(
            dia_habil=proximo_dia_numero.valor,
            fecha=fecha_proximo.isoformat(),
            hitos_periodicos=hitos_dtos,
        )

    def _obtener_feriados_proximos(self) -> List[DiaCalendarioDTO]:
        """Obtiene los próximos 5 feriados."""
        feriados = self.calendario_repo.obtener_feriados_proximos(
            fecha_desde=date.today(), cantidad=5
        )
        return [DiaCalendarioDTO.from_entity(f) for f in feriados]

    def _obtener_hitos_importantes_proximos(self) -> List[HitoImportanteDTO]:
        """Obtiene los próximos 10 hitos importantes."""
        hitos = self.hito_importante_repo.obtener_proximos(
            fecha_desde=date.today(), cantidad=10, solo_activos=True
        )
        return [HitoImportanteDTO.from_entity(h, calcular_dias=True) for h in hitos]
