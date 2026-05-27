"""
Servidor HTTP simple para servir el frontend desde localhost.
Esto soluciona los problemas de CORS con file://
"""
import http.server
import socketserver
import os

# Puerto para el frontend
PORT = 5173

# Cambiar al directorio raíz del proyecto (padre de frontend)
# Esto permite servir tanto frontend/ como imagenes/
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Headers CORS para permitir peticiones al backend
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_GET(self):
        # Redirigir / a app.html
        if self.path == '/':
            self.path = '/frontend/app.html'
        return super().do_GET()

print("🚀 Servidor Frontend iniciado")
print(f"📍 URL: http://localhost:{PORT}")
print(f"📂 Directorio: {os.getcwd()}")
print(f"\n✅ Abre tu navegador en: http://localhost:{PORT}")
print("⏹️  Presiona Ctrl+C para detener el servidor\n")

with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Servidor detenido")
