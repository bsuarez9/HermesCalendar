/**
 * Widget que muestra los hitos del próximo día hábil
 */
import { HitosProximoDia } from '@domain/entities/Dashboard';
import { format } from 'date-fns';
import { es } from 'date-fns/locale';

interface Props {
  hitosProximoDia: HitosProximoDia;
}

export const HitosProximoDiaWidget = ({ hitosProximoDia }: Props) => {
  const fecha = new Date(hitosProximoDia.fecha);
  const hayHitos = hitosProximoDia.hitosPeriodicos.length > 0;

  return (
    <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-green-500">
      <h2 className="text-xl font-semibold text-gray-800 mb-4">
        📅 Para el D+{hitosProximoDia.diaHabil}
      </h2>

      <p className="text-sm text-gray-600 mb-4">
        {format(fecha, "EEEE, d 'de' MMMM", { locale: es })}
      </p>

      {hayHitos ? (
        <ul className="space-y-3">
          {hitosProximoDia.hitosPeriodicos.map((hito) => (
            <li
              key={hito.id}
              className="flex items-start space-x-3 p-3 bg-gray-50 rounded hover:bg-gray-100 transition"
            >
              <span className="text-green-600 mt-1">✓</span>
              <div className="flex-1">
                <p className="font-medium text-gray-900">{hito.accion}</p>
                {hito.descripcion && (
                  <p className="text-sm text-gray-600 mt-1">{hito.descripcion}</p>
                )}
              </div>
            </li>
          ))}
        </ul>
      ) : (
        <div className="text-center py-8 text-gray-500">
          <p>No hay hitos programados para este día</p>
        </div>
      )}
    </div>
  );
};
