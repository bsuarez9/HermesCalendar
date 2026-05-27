"""
Script de entrada para Cloudera
Compatible con entornos Jupyter/Notebook
"""
import os
import sys

# Agregar el directorio actual al path
current_dir = os.getcwd()
sys.path.insert(0, current_dir)

# Configurar variables de entorno antes de importar Flask
os.environ['EXCEL_FILE_PATH'] = os.path.join(current_dir, 'Calendario_Argentina_2026_Completo.xlsx')

# Ahora importar y ejecutar la app Flask
from backend.app_flask_cloudera import app, cargar_excel, EXCEL_PATH

if __name__ == "__main__":
    print("🚀 Iniciando Calendario YPF API (Flask) - Cloudera...")
    print(f"📂 Working Directory: {current_dir}")
    print(f"📂 Excel: {EXCEL_PATH}")

    # Cargar datos
    cargar_excel()

    # Obtener puerto de variables de entorno o usar 8080 por defecto
    PORT = int(os.environ.get("CDSW_APP_PORT", os.environ.get("PORT", 8080)))

    print(f"✅ Servidor listo en http://0.0.0.0:{PORT}")

    # Ejecutar Flask
    app.run(
        host="0.0.0.0",
        port=PORT,
        debug=False  # Desactivar debug en Cloudera para evitar reloader
    )
