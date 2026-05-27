/**
 * Widget que muestra la posición actual en el mes (D+X)
 */
import { PosicionActual } from '@domain/entities/Dashboard';
import { format } from 'date-fns';
import { es } from 'date-fns/locale';

interface Props {
  posicion: PosicionActual;
}

export const PosicionActualWidget = ({ posicion }: Props) => {
  const fechaActual = new Date(posicion.fechaActual);

  return (
    <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-ypf-blue">
      <h2 className="text-xl font-semibold text-gray-800 mb-4">
        📍 ¿Dónde estamos hoy?
      </h2>

      <div className="space-y-4">
        {/* Fecha Actual */}
        <div>
          <p className="text-sm text-gray-600">Hoy es</p>
          <p className="text-2xl font-bold text-gray-900">
            {format(fechaActual, "EEEE, d 'de' MMMM", { locale: es })}
          </p>
        </div>

        {/* Día Hábil Actual */}
        <div className="flex items-center space-x-4">
          <div className="flex-1">
            <p className="text-sm text-gray-600">Estamos en</p>
            <p className="text-4xl font-bold text-ypf-blue">
              D+{posicion.diaHabilActual}
            </p>
          </div>

          <div className="text-gray-400 text-3xl">→</div>

          <div className="flex-1">
            <p className="text-sm text-gray-600">Próximo día hábil</p>
            <p className="text-4xl font-bold text-green-600">
              D+{posicion.proximoDiaHabil}
            </p>
          </div>
        </div>

        {/* Fecha Próximo Día Hábil */}
        <div className="bg-green-50 rounded p-3">
          <p className="text-sm text-green-800">
            <strong>Próximo día hábil:</strong>{' '}
            {format(new Date(posicion.fechaProximoDiaHabil), 'EEEE, d/MM/yyyy', {
              locale: es,
            })}
          </p>
        </div>
      </div>
    </div>
  );
};
