/**
 * API para el dashboard
 */
import { Dashboard } from '@domain/entities/Dashboard';
import { apiClient } from './apiClient';

export const dashboardApi = {
  /**
   * Obtiene los datos del dashboard
   */
  getDashboard: async (): Promise<Dashboard> => {
    return apiClient.get<Dashboard>('/dashboard');
  },
};
