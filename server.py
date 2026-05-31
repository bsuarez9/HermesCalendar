"""
Servidor Gunicorn para Cloudera Applications
Ejecuta Gunicorn desde Python para compatibilidad con Jupyter
"""
import os
import sys
import subprocess
import time
import signal

# Cambiar al directorio del proyecto
project_dir = '/home/cdsw/HermesCalendar'
if os.path.exists(project_dir):
    os.chdir(project_dir)
    sys.path.insert(0, project_dir)

print("🚀 Iniciando Gunicorn para Calendario YPF...")

# Obtener puerto de Cloudera
PORT = int(os.environ.get("CDSW_APP_PORT", os.environ.get("PORT", 8080)))

# CRÍTICO: Matar procesos zombies en el puerto
print(f"🔍 Limpiando puerto {PORT}...")
try:
    # Buscar y matar procesos en el puerto
    result = subprocess.run(
        f"lsof -ti:{PORT}",
        shell=True,
        capture_output=True,
        text=True
    )
    if result.stdout.strip():
        pids = result.stdout.strip().split('\n')
        print(f"⚠️ Encontrados PIDs en puerto {PORT}: {pids}")
        for pid in pids:
            try:
                os.kill(int(pid), signal.SIGKILL)
                print(f"✅ Proceso {pid} terminado")
            except Exception as e:
                print(f"⚠️ No se pudo terminar {pid}: {e}")
        time.sleep(3)  # Esperar a que el SO libere el puerto
    else:
        print(f"✅ Puerto {PORT} libre")
except Exception as e:
    print(f"⚠️ Error limpiando puerto: {e}")

time.sleep(1)  # Sleep adicional para race conditions

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
