/**
 * API para gestión de hitos
 */
import { HitoPeriodico, HitoImportante } from '@domain/entities/Dashboard';
import { apiClient } from './apiClient';

export interface CrearHitoPeriodicoRequest {
  diaHabil: number;
  accion: string;
  descripcion?: string;
}

export interface ActualizarHitoPeriodicoRequest {
  accion?: string;
  descripcion?: string;
  activo?: boolean;
}

export interface CrearHitoImportanteRequest {
  fecha: string; // YYYY-MM-DD
  titulo: string;
  descripcion?: string;
  categoria?: string;
}

export interface ActualizarHitoImportanteRequest {
  titulo?: string;
  descripcion?: string;
  categoria?: string;
  activo?: boolean;
  fecha?: string;
}

export const hitosPeriodicosApi = {
  listar: async (soloActivos: boolean = true): Promise<HitoPeriodico[]> => {
    return apiClient.get<HitoPeriodico[]>(`/hitos-periodicos?solo_activos=${soloActivos}`);
  },

  crear: async (data: CrearHitoPeriodicoRequest): Promise<HitoPeriodico> => {
    return apiClient.post<HitoPeriodico>('/hitos-periodicos', data);
  },

  actualizar: async (
    id: string,
    data: ActualizarHitoPeriodicoRequest
  ): Promise<HitoPeriodico> => {
    return apiClient.put<HitoPeriodico>(`/hitos-periodicos/${id}`, data);
  },

  eliminar: async (id: string): Promise<void> => {
    return apiClient.delete(`/hitos-periodicos/${id}`);
  },
};

export const hitosImportantesApi = {
  listar: async (
    soloActivos: boolean = true,
    categoria?: string
  ): Promise<HitoImportante[]> => {
    let url = `/hitos-importantes?solo_activos=${soloActivos}`;
    if (categoria) url += `&categoria=${encodeURIComponent(categoria)}`;
    return apiClient.get<HitoImportante[]>(url);
  },

  crear: async (data: CrearHitoImportanteRequest): Promise<HitoImportante> => {
    return apiClient.post<HitoImportante>('/hitos-importantes', data);
  },

  actualizar: async (
    id: string,
    data: ActualizarHitoImportanteRequest
  ): Promise<HitoImportante> => {
    return apiClient.put<HitoImportante>(`/hitos-importantes/${id}`, data);
  },

  eliminar: async (id: string): Promise<void> => {
    return apiClient.delete(`/hitos-importantes/${id}`);
  },
};
