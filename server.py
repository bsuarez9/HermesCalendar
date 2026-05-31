"""
Servidor Gunicorn para Cloudera Applications
Ejecuta Gunicorn desde Python para compatibilidad con Jupyter
"""
import os
import sys

# Cambiar al directorio del proyecto
project_dir = '/home/cdsw/HermesCalendar'
if os.path.exists(project_dir):
    os.chdir(project_dir)
    sys.path.insert(0, project_dir)

print("🚀 Iniciando Gunicorn para Calendario YPF...")

# Obtener puerto de Cloudera
PORT = int(os.environ.get("CDSW_APP_PORT", os.environ.get("PORT", 8080)))

# Importar la app antes de ejecutar Gunicorn
from run import application

print(f"📂 Directorio: {os.getcwd()}")
print(f"🌐 Puerto: {PORT}")

# Ejecutar Gunicorn programáticamente
from gunicorn.app.base import BaseApplication

class ClouderaGunicornApp(BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        for key, value in self.options.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application

# Configuración de Gunicorn
options = {
    'bind': f'0.0.0.0:{PORT}',
    'workers': 2,
    'threads': 4,
    'timeout': 120,
    'accesslog': '-',
    'errorlog': '-',
    'loglevel': 'info',
}

print("✅ Iniciando servidor WSGI...")
ClouderaGunicornApp(application, options).run()
