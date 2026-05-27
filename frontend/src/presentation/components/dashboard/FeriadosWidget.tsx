/**
 * Widget que muestra los próximos feriados
 */
import { DiaCalendario } from '@domain/entities/Dashboard';
import { format } from 'date-fns';
import { es } from 'date-fns/locale';

interface Props {
  feriados: DiaCalendario[];
}

export const FeriadosWidget = ({ feriados }: Props) => {
  return (
    <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-red-500">
      <h2 className="text-xl font-semibold text-gray-800 mb-4">
        🎉 Próximos Feriados
      </h2>

      {feriados.length > 0 ? (
        <ul className="space-y-3">
          {feriados.map((feriado, index) => {
            const fecha = new Date(feriado.fecha);
            const hoy = new Date();
            const diasHasta = Math.ceil(
              (fecha.getTime() - hoy.getTime()) / (1000 * 60 * 60 * 24)
            );

            return (
              <li
                key={index}
                className="flex items-center justify-between p-3 bg-red-50 rounded hover:bg-red-100 transition"
              >
                <div className="flex-1">
                  <p className="font-medium text-gray-900">
                    {format(fecha, 'EEEE, d/MM/yyyy', { locale: es })}
                  </p>
                  {feriado.observaciones && (
                    <p className="text-sm text-gray-600 mt-1">
                      {feriado.observaciones}
                    </p>
                  )}
                </div>
                <span className="text-xs bg-red-200 text-red-800 px-2 py-1 rounded">
                  {diasHasta === 0
                    ? 'Hoy'
                    : diasHasta === 1
                    ? 'Mañana'
                    : `En ${diasHasta} días`}
                </span>
              </li>
            );
          })}
        </ul>
      ) : (
        <p className="text-center py-8 text-gray-500">
          No hay feriados próximos
        </p>
      )}
    </div>
  );
};
