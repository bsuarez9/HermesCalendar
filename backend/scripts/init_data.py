"""Script para inicializar datos en la base de datos desde el Excel."""
import os
import sys
from pathlib import Path

# Agregar el directorio raíz al path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from dotenv import load_dotenv

from src.infrastructure.config.database import SessionLocal, init_db
from src.infrastructure.excel.calendario_excel_reader import CalendarioExcelReader
from src.infrastructure.persistence.models.hito_importante_model import HitoImportanteModel
from src.infrastructure.persistence.models.hito_periodico_model import HitoPeriodicoModel

# Cargar variables de entorno
load_dotenv()


def cargar_hitos_desde_excel():
    """
    Carga los hitos periódicos e importantes desde el Excel a la base de datos.

    Esta función debe ejecutarse una sola vez al iniciar la aplicación
    para poblar la base de datos con los datos iniciales del Excel.
    """
    print("🚀 Iniciando carga de datos desde Excel...")

    # Inicializar BD
    init_db()

    # Obtener path del Excel
    excel_path = os.getenv("EXCEL_FILE_PATH", "../Calendario_Argentina_2026_Completo.xlsx")

    if not os.path.exists(excel_path):
        print(f"❌ Error: No se encontró el archivo Excel en {excel_path}")
        return

    print(f"📂 Leyendo archivo: {excel_path}")

    # Leer Excel
    reader = CalendarioExcelReader(excel_path)
    datos = reader.leer_todo()

    # Obtener sesión
    db = SessionLocal()

    try:
        # Cargar hitos periódicos
        print(f"\n📅 Cargando {len(datos['hitos_periodicos'])} hitos periódicos...")
        for hito in datos["hitos_periodicos"]:
            # Verificar si ya existe
            existe = (
                db.query(HitoPeriodicoModel)
                .filter_by(dia_habil=hito.dia_habil.valor, accion=hito.accion)
                .first()
            )

            if not existe:
                model = HitoPeriodicoModel(
                    id=hito.id,
                    dia_habil=hito.dia_habil.valor,
                    accion=hito.accion,
                    descripcion=hito.descripcion,
                    activo=hito.activo,
                )
                db.add(model)
                print(f"  ✅ D+{hito.dia_habil.valor}: {hito.accion}")
            else:
                print(f"  ⏭️  D+{hito.dia_habil.valor}: {hito.accion} (ya existe)")

        # Cargar hitos importantes
        print(f"\n🎯 Cargando {len(datos['hitos_importantes'])} hitos importantes...")
        for hito in datos["hitos_importantes"]:
            # Verificar si ya existe
            existe = (
                db.query(HitoImportanteModel)
                .filter_by(fecha=hito.fecha, titulo=hito.titulo)
                .first()
            )

            if not existe:
                model = HitoImportanteModel(
                    id=hito.id,
                    fecha=hito.fecha,
                    titulo=hito.titulo,
                    descripcion=hito.descripcion,
                    categoria=hito.categoria,
                    activo=hito.activo,
                )
                db.add(model)
                print(f"  ✅ {hito.fecha}: {hito.titulo}")
            else:
                print(f"  ⏭️  {hito.fecha}: {hito.titulo} (ya existe)")

        # Commit
        db.commit()
        print("\n✅ ¡Datos cargados exitosamente!")

    except Exception as e:
        print(f"\n❌ Error al cargar datos: {e}")
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    cargar_hitos_desde_excel()
