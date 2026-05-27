"""Servicio de dominio para lógica relacionada con el calendario."""
from datetime import date, timedelta
from typing import List, Optional, Tuple

from ..entities.dia_calendario import DiaCalendario
from ..repositories.calendario_repository import ICalendarioRepository
from ..value_objects.dia_habil_numero import DiaHabilNumero


class CalendarioService:
    """
    Servicio de dominio para operaciones complejas del calendario.

    Contiene lógica de negocio que involucra múltiples entidades
    o que no pertenece naturalmente a una sola entidad.
    """

    def __init__(self, calendario_repo: ICalendarioRepository):
        """
        Constructor del servicio.

        Args:
            calendario_repo: Repositorio de calendario
        """
        self.calendario_repo = calendario_repo

    def obtener_dia_habil_actual(self, fecha_referencia: Optional[date] = None) -> DiaCalendario:
        """
        Obtiene el día hábil actual o el último día hábil si hoy no es hábil.

        Si la fecha de referencia cae en fin de semana o feriado,
        retorna el último día hábil anterior.

        Args:
            fecha_referencia: Fecha de referencia (por defecto hoy)

        Returns:
            El día hábil actual o el último día hábil

        Raises:
            ValueError: Si no se encuentra ningún día hábil
        """
        fecha = fecha_referencia or date.today()
        dia = self.calendario_repo.obtener_dia(fecha)

        if dia and dia.es_habil:
            return dia

        # Si no es hábil, buscar hacia atrás el último día hábil
        fecha_busqueda = fecha - timedelta(days=1)
        max_intentos = 7  # Buscar hasta una semana atrás

        for _ in range(max_intentos):
            dia = self.calendario_repo.obtener_dia(fecha_busqueda)
            if dia and dia.es_habil:
                return dia
            fecha_busqueda -= timedelta(days=1)

        raise ValueError(f"No se encontró ningún día hábil cerca de {fecha}")

    def calcular_posicion_en_mes(
        self, fecha_referencia: Optional[date] = None
    ) -> Tuple[DiaHabilNumero, DiaHabilNumero]:
        """
        Calcula en qué día hábil estamos actualmente y cuál es el siguiente.

        Returns:
            Tupla (dia_habil_actual, proximo_dia_habil)

        Example:
            Si hoy es D+6, retorna (DiaHabilNumero(6), DiaHabilNumero(7))
        """
        dia_actual = self.obtener_dia_habil_actual(fecha_referencia)

        if not dia_actual.dia_habil_numero:
            raise ValueError("El día hábil actual no tiene número asignado")

        proximo_numero = dia_actual.dia_habil_numero.valor + 1
        proximo_dia_habil = DiaHabilNumero(min(proximo_numero, 31))

        return (dia_actual.dia_habil_numero, proximo_dia_habil)

    def obtener_dias_habiles_restantes_mes(
        self, fecha_referencia: Optional[date] = None
    ) -> List[DiaCalendario]:
        """
        Obtiene todos los días hábiles que quedan en el mes actual.

        Args:
            fecha_referencia: Fecha de referencia (por defecto hoy)

        Returns:
            Lista de días hábiles futuros en el mes actual
        """
        fecha = fecha_referencia or date.today()
        ultimo_dia_mes = self._obtener_ultimo_dia_mes(fecha.year, fecha.month)

        dias_rango = self.calendario_repo.obtener_dias_rango(fecha, ultimo_dia_mes)

        # Filtrar solo días hábiles futuros
        return [dia for dia in dias_rango if dia.es_habil and dia.fecha >= fecha]

    def es_proximo_dia_habil(self, fecha_evaluar: date) -> bool:
        """
        Verifica si una fecha es el próximo día hábil desde hoy.

        Args:
            fecha_evaluar: Fecha a evaluar

        Returns:
            True si es el próximo día hábil
        """
        proximo = self.calendario_repo.obtener_proximo_dia_habil(date.today())
        return proximo is not None and proximo.fecha == fecha_evaluar

    def dias_habiles_entre_fechas(self, fecha_inicio: date, fecha_fin: date) -> int:
        """
        Calcula cuántos días hábiles hay entre dos fechas.

        Args:
            fecha_inicio: Fecha de inicio (inclusive)
            fecha_fin: Fecha de fin (inclusive)

        Returns:
            Número de días hábiles
        """
        return self.calendario_repo.contar_dias_habiles_hasta(fecha_inicio, fecha_fin)

    def obtener_fecha_dia_habil(
        self, dia_habil: DiaHabilNumero, mes: Optional[int] = None, anio: Optional[int] = None
    ) -> Optional[date]:
        """
        Obtiene la fecha calendario de un día hábil específico.

        Args:
            dia_habil: Número de día hábil (D+1, D+2, etc.)
            mes: Mes (por defecto el mes actual)
            anio: Año (por defecto el año actual)

        Returns:
            La fecha del día hábil o None si no existe
        """
        hoy = date.today()
        mes_busqueda = mes or hoy.month
        anio_busqueda = anio or hoy.year

        dia_calendario = self.calendario_repo.obtener_dia_por_numero_habil(
            anio_busqueda, mes_busqueda, dia_habil
        )

        return dia_calendario.fecha if dia_calendario else None

    @staticmethod
    def _obtener_ultimo_dia_mes(anio: int, mes: int) -> date:
        """
        Calcula el último día de un mes.

        Args:
            anio: Año
            mes: Mes

        Returns:
            Fecha del último día del mes
        """
        if mes == 12:
            return date(anio, 12, 31)
        else:
            return date(anio, mes + 1, 1) - timedelta(days=1)
