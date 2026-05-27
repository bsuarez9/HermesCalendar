/**
 * Widget que muestra los hitos importantes próximos
 */
import { HitoImportante } from '@domain/entities/Dashboard';
import { format } from 'date-fns';
import { es } from 'date-fns/locale';

interface Props {
  hitos: HitoImportante[];
  diasHabilesRestantes: number;
}

export const HitosImportantesWidget = ({ hitos, diasHabilesRestantes }: Props) => {
  return (
    <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-yellow-500">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-semibold text-gray-800">
          ⭐ Hitos Importantes
        </h2>
        <span className="text-sm bg-yellow-100 text-yellow-800 px-3 py-1 rounded">
          {diasHabilesRestantes} días hábiles restantes en el mes
        </span>
      </div>

      {hitos.length > 0 ? (
        <ul className="space-y-3">
          {hitos.map((hito) => {
            const fecha = new Date(hito.fecha);
            const diasHasta = hito.diasHastaHito || 0;

            return (
              <li
                key={hito.id}
                className="flex items-start space-x-3 p-3 bg-yellow-50 rounded hover:bg-yellow-100 transition"
              >
                <div className="flex-1">
                  <div className="flex items-center space-x-2">
                    <p className="font-medium text-gray-900">{hito.titulo}</p>
                    {hito.categoria && (
                      <span className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded">
                        {hito.categoria}
                      </span>
                    )}
                  </div>
                  <p className="text-sm text-gray-600 mt-1">
                    {format(fecha, "d 'de' MMMM, yyyy", { locale: es })}
                  </p>
                  {hito.descripcion && (
                    <p className="text-sm text-gray-500 mt-1">{hito.descripcion}</p>
                  )}
                </div>
                <span className="text-xs bg-yellow-200 text-yellow-800 px-2 py-1 rounded whitespace-nowrap">
                  {diasHasta === 0
                    ? 'Hoy'
                    : diasHasta === 1
                    ? 'Mañana'
                    : diasHasta < 0
                    ? 'Pasado'
                    : `En ${diasHasta} días`}
                </span>
              </li>
            );
          })}
        </ul>
      ) : (
        <p className="text-center py-8 text-gray-500">
          No hay hitos importantes próximos
        </p>
      )}
    </div>
  );
};
