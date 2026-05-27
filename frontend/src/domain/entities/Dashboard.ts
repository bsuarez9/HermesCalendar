/**
 * Entidades de dominio para el Dashboard
 */

export interface DiaCalendario {
  fecha: string;
  nombreDia: string;
  tipo: 'Habil' | 'No habil';
  diaHabilNumero: number | null;
  observaciones: string | null;
  esHabil: boolean;
  esFeriado: boolean;
}

export interface HitoPeriodico {
  id: string;
  diaHabil: number;
  accion: string;
  descripcion?: string;
  activo: boolean;
}

export interface HitoImportante {
  id: string;
  fecha: string;
  titulo: string;
  descripcion?: string;
  categoria?: string;
  activo: boolean;
  diasHastaHito?: number;
}

export interface PosicionActual {
  diaHabilActual: number;
  proximoDiaHabil: number;
  fechaActual: string;
  fechaProximoDiaHabil: string;
}

export interface HitosProximoDia {
  diaHabil: number;
  fecha: string;
  hitosPeriodicos: HitoPeriodico[];
}

export interface Dashboard {
  posicionActual: PosicionActual;
  hitosProximoDia: HitosProximoDia;
  feriadosProximos: DiaCalendario[];
  hitosImportantesProximos: HitoImportante[];
  diasHabilesRestantesMes: number;
}
