/**
 * Página principal del Dashboard
 */
import { useQuery } from '@tanstack/react-query';
import { dashboardApi } from '@infrastructure/api/dashboardApi';
import { PosicionActualWidget } from '@presentation/components/dashboard/PosicionActualWidget';
import { HitosProximoDiaWidget } from '@presentation/components/dashboard/HitosProximoDiaWidget';
import { FeriadosWidget } from '@presentation/components/dashboard/FeriadosWidget';
import { HitosImportantesWidget } from '@presentation/components/dashboard/HitosImportantesWidget';

export const DashboardPage = () => {
  const { data: dashboard, isLoading, error } = useQuery({
    queryKey: ['dashboard'],
    queryFn: dashboardApi.getDashboard,
    refetchInterval: 60000, // Refrescar cada minuto
  });

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-xl">Cargando dashboard...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-xl text-red-600">
          Error al cargar el dashboard. Por favor, intente nuevamente.
        </div>
      </div>
    );
  }

  if (!dashboard) return null;

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <header className="mb-8">
          <h1 className="text-4xl font-bold text-ypf-blue">Calendario YPF</h1>
          <p className="text-gray-600 mt-2">
            Sistema de gestión de hitos y días hábiles
          </p>
        </header>

        {/* Grid de Widgets */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Posición Actual */}
          <PosicionActualWidget posicion={dashboard.posicionActual} />

          {/* Hitos Próximo Día */}
          <HitosProximoDiaWidget hitosProximoDia={dashboard.hitosProximoDia} />

          {/* Feriados Próximos */}
          <FeriadosWidget feriados={dashboard.feriadosProximos} />

          {/* Hitos Importantes */}
          <HitosImportantesWidget
            hitos={dashboard.hitosImportantesProximos}
            diasHabilesRestantes={dashboard.diasHabilesRestantesMes}
          />
        </div>
      </div>
    </div>
  );
};
