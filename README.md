# 📅 Calendario YPF - Proyecto Hermes

Sistema de gestión de hitos y días hábiles para YPF, desarrollado con **Clean Architecture**.

## 🚀 Inicio Rápido

### Prerequisitos
- **Python 3.8+** (IMPORTANTE para Cloudera)
- Navegador web moderno

### Instalación y Ejecución

1. **Clonar el repositorio**
```bash
git clone https://github.com/TU-USUARIO/calendario-ypf.git
cd calendario-ypf
```

2. **Instalar dependencias del backend**
```bash
cd backend
pip install -r requirements.txt
cd ..
```

3. **Iniciar la aplicación**

**Windows** (recomendado):
```bash
# Doble click en:
INICIAR_APP.bat
```

**Manual** (cualquier sistema operativo):
```bash
# Terminal 1 - Backend (Python Flask - Puerto 8000)
cd backend
python app_flask.py

# Terminal 2 - Frontend (Puerto 5173)
cd frontend
python server.py
```

4. **Abrir en el navegador**
```
http://localhost:5173
```

5. **Detener la aplicación**
```bash
# Windows: Doble click en:
DETENER_APP.bat

# O cerrar las 2 ventanas de consola que se abrieron
```

---

## ✨ Funcionalidades

### 🏠 Dashboard
- **Posición actual en días hábiles (D+X)**
- Hitos del próximo día hábil
- Próximos feriados
- Hitos importantes con conteo de días
- Días hábiles restantes en el mes

### 📅 Calendario
- **Vista Mensual**: Calendario completo con todos los hitos
- **Vista Semanal**: Detalle día por día (Lun-Vie)
- Agrupación inteligente de hitos (ej: "EERR (5)")
- Código de colores:
  - 🟢 Verde: Día hábil
  - 🔴 Rojo: Día no hábil/Feriado
  - 🔵 Azul: Día actual
  - 🟡 Amarillo: Hitos importantes
  - 🔵 Celeste: Hitos periódicos

### 📊 Gestión de Hitos
- Próximamente: CRUD desde la web
- Por ahora: Editar Excel directamente

---

## 📝 Cómo Agregar/Modificar Hitos

1. Abrir: `Calendario_Argentina_2026_Completo.xlsx`
2. Editar las hojas:
   - **Hitos_Periodicos**: Hitos mensuales (D+7, D+10, etc.)
   - **Hitos_Importantes_YPF**: Fechas específicas
3. Guardar el archivo
4. En la web: Click "🔄 Recargar Datos"

---

## 🛠️ Stack Tecnológico

### Backend (Python - Compatible con Cloudera ✅)
- **Python 3.8+**
- **Flask** - Framework web ligero
- **Flask-CORS** - Manejo de CORS
- **openpyxl** - Lectura de archivos Excel
- **python-dotenv** - Variables de entorno

### Frontend
- **HTML5/CSS3**
- **JavaScript vanilla** (sin frameworks)
- **Fetch API** para consumir backend

### Arquitectura
- **Clean Architecture** (Hexagonal)
- **Domain-Driven Design (DDD)**
- **Repository Pattern**
- **SOLID Principles**

---

## 📂 Estructura del Proyecto

```
CalendarioApp/
├── backend/                              # Backend Python Flask
│   ├── src/
│   │   ├── domain/                      # Entidades y lógica de negocio
│   │   ├── application/                 # Casos de uso
│   │   └── infrastructure/              # Lectura de Excel, APIs
│   ├── app_flask.py                     # Servidor Flask principal
│   ├── requirements.txt                 # Dependencias Python
│   └── .env                             # Configuración
│
├── frontend/                            # Frontend HTML/CSS/JavaScript
│   ├── app.html                        # Aplicación principal
│   ├── app.js                          # Lógica del frontend
│   └── server.py                       # Servidor HTTP simple (Python)
│
├── imagenes/                           # Logos YPF y Hermes
│   ├── ypf_azul.png
│   └── Proyecto Hermes_Isotipo_COL.png
│
├── Calendario_Argentina_2026_Completo.xlsx  # Datos fuente
├── INICIAR_APP.bat                     # Script de inicio (Windows)
├── DETENER_APP.bat                     # Script para detener servidores
├── LEEME.txt                           # Guía de uso rápida
├── ARCHITECTURE.md                     # Documentación de arquitectura
└── README.md                           # Este archivo
```

---

## 🌐 APIs Disponibles

```
GET  /api/v1/dashboard           # Dashboard principal
GET  /api/v1/calendario          # Todos los días del año con D+X
GET  /api/v1/hitos-periodicos    # Hitos periódicos (D+X)
GET  /api/v1/hitos-importantes   # Hitos en fechas específicas
POST /api/v1/reload              # Recargar datos del Excel
```

---

## 🔧 Configuración

Editar `backend/.env` para cambiar configuraciones:

```env
DATABASE_URL=sqlite:///./calendario_ypf.db
EXCEL_FILE_PATH=../Calendario_Argentina_2026_Completo.xlsx
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
```

---

## 🐛 Solución de Problemas

### Puerto ocupado
```bash
# Windows
DETENER_APP.bat
```

### No se ven los datos
- Click en "🔄 Recargar Datos" en la web
- Verificar que el Excel esté en la carpeta raíz

### Error al conectar con backend
- Verificar que ambas ventanas estén abiertas (Backend YPF y Frontend YPF)
- Backend debe estar en: http://localhost:8000
- Frontend debe estar en: http://localhost:5173

---

## ☁️ Despliegue en Cloudera

### Prerequisitos
- Cuenta de Cloudera
- Repositorio GitHub con este código

### Pasos para Deploy

1. **Subir a GitHub** (ver sección siguiente)

2. **Crear proyecto en Cloudera**
   - New Project → From Git Repository
   - Pegar URL del repo: `https://github.com/TU-USUARIO/calendario-ypf`

3. **Configurar Runtime**
   - Runtime: **Python 3.8+**
   - Entry Point: `backend/app_flask.py`
   - Port: `8000`

4. **Variables de Entorno en Cloudera**
   ```
   EXCEL_FILE_PATH=./Calendario_Argentina_2026_Completo.xlsx
   ALLOWED_ORIGINS=*
   ```

5. **Deploy**
   - Cloudera ejecutará automáticamente `python app_flask.py`
   - La app estará disponible en la URL que te asigne Cloudera

### Nota Importante
El frontend server.py NO es necesario en Cloudera. Solo necesitas desplegar el backend, y los usuarios accederán directamente a la API o podrás servir el frontend desde Cloudera también.

---

## 📄 Licencia

Uso interno YPF - Proyecto Hermes

---

## 👥 Autor

Desarrollado para YPF - Proyecto Hermes 2026
