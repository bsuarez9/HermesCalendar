# 🏗️ Arquitectura del Sistema - Calendario YPF

## 📐 Arquitectura General

Este proyecto implementa **Clean Architecture** (Arquitectura Limpia) también conocida como **Arquitectura Hexagonal** o **Ports & Adapters**, siguiendo principios SOLID y Domain-Driven Design (DDD).

## 🎯 Principios Fundamentales

1. **Independencia de Frameworks**: La lógica de negocio no depende de librerías externas
2. **Testeable**: La lógica de negocio puede probarse sin UI, BD, servidor web
3. **Independencia de la UI**: La UI puede cambiar sin afectar el resto del sistema
4. **Independencia de la Base de Datos**: Puedes cambiar PostgreSQL por MongoDB sin afectar las reglas de negocio
5. **Independencia de Agentes Externos**: Las reglas de negocio no saben nada del mundo exterior

## 📦 Estructura de Capas

```
┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                        │
│                  (API REST - FastAPI)                        │
│           Controllers, Routes, Request/Response              │
└─────────────────────┬───────────────────────────────────────┘
                      │ ↓ Dependency
┌─────────────────────┴───────────────────────────────────────┐
│                   APPLICATION LAYER                          │
│              Use Cases / Application Services                │
│        DTOs, Interfaces, Orchestration Logic                 │
└─────────────────────┬───────────────────────────────────────┘
                      │ ↓ Dependency
┌─────────────────────┴───────────────────────────────────────┐
│                     DOMAIN LAYER                             │
│              Entities, Value Objects, Domain Logic           │
│         Business Rules, Domain Services, Interfaces          │
└─────────────────────┬───────────────────────────────────────┘
                      │ ↑ Implementation
┌─────────────────────┴───────────────────────────────────────┐
│                  INFRASTRUCTURE LAYER                        │
│    Database, Excel Reader, External Services, Config         │
│         Repository Implementations, Adapters                 │
└─────────────────────────────────────────────────────────────┘
```

### ⚠️ Regla de Dependencias

**Las dependencias solo apuntan hacia adentro**. Las capas externas pueden depender de las internas, pero nunca al revés.

- ✅ Presentation → Application → Domain
- ✅ Infrastructure → Domain (implementa interfaces del dominio)
- ❌ Domain → Infrastructure (NUNCA)
- ❌ Domain → Application (NUNCA)

---

## 🔷 Backend - Arquitectura en Capas

### 1️⃣ Domain Layer (Capa de Dominio)

**Responsabilidad**: Contiene la lógica de negocio pura, reglas del dominio.

**Contenido**:
- `entities/`: Objetos de negocio con identidad (Dia, Hito, HitoPeriodico)
- `value_objects/`: Objetos sin identidad (Fecha, TipoHito, DiaHabil)
- `repositories/`: Interfaces (contratos) de repositorios
- `services/`: Servicios de dominio (lógica compleja entre entidades)

**Principios**:
- Sin dependencias externas (solo Python estándar)
- Inmutabilidad donde sea posible
- Validaciones de reglas de negocio

**Ejemplo**:
```python
# domain/entities/hito_periodico.py
class HitoPeriodico:
    def __init__(self, dia_habil: int, accion: str):
        self._validar_dia_habil(dia_habil)
        self.dia_habil = dia_habil
        self.accion = accion
    
    def _validar_dia_habil(self, dia: int):
        if not 1 <= dia <= 31:
            raise ValueError("Día hábil debe estar entre 1 y 31")
```

### 2️⃣ Application Layer (Capa de Aplicación)

**Responsabilidad**: Orquesta el flujo de datos entre capas, coordina use cases.

**Contenido**:
- `use_cases/`: Casos de uso de la aplicación (uno por acción)
- `dtos/`: Data Transfer Objects (objetos para transferir datos)
- `interfaces/`: Interfaces de servicios de aplicación

**Principios**:
- Sin lógica de negocio (eso va en Domain)
- Sin detalles de infraestructura (DB, Excel, etc.)
- Orquestación pura

**Ejemplo**:
```python
# application/use_cases/obtener_hitos_proximos.py
class ObtenerHitosProximosUseCase:
    def __init__(self, hito_repo: IHitoRepository, calendario_service: ICalendarioService):
        self.hito_repo = hito_repo
        self.calendario_service = calendario_service
    
    def execute(self, dias: int) -> List[HitoDTO]:
        fecha_actual = self.calendario_service.obtener_fecha_actual()
        hitos = self.hito_repo.obtener_proximos(fecha_actual, dias)
        return [HitoDTO.from_entity(h) for h in hitos]
```

### 3️⃣ Infrastructure Layer (Capa de Infraestructura)

**Responsabilidad**: Implementaciones concretas, adaptadores a sistemas externos.

**Contenido**:
- `persistence/models/`: Modelos de SQLAlchemy (ORM)
- `persistence/repositories/`: Implementaciones de interfaces de repositorios
- `excel/`: Lector de archivos Excel
- `config/`: Configuración (DB, variables de entorno)

**Principios**:
- Implementa interfaces definidas en Domain
- Contiene detalles técnicos (queries SQL, lectura de archivos)
- Puede cambiar sin afectar Domain/Application

**Ejemplo**:
```python
# infrastructure/persistence/repositories/hito_repository.py
class SQLAlchemyHitoRepository(IHitoRepository):
    def __init__(self, session: Session):
        self.session = session
    
    def obtener_proximos(self, fecha: date, dias: int) -> List[Hito]:
        # Implementación concreta con SQLAlchemy
        ...
```

### 4️⃣ Presentation Layer (Capa de Presentación)

**Responsabilidad**: Exponer la aplicación al mundo exterior (API REST).

**Contenido**:
- `api/v1/`: Routers de FastAPI
- `schemas/`: Pydantic schemas (request/response)
- `dependencies/`: Inyección de dependencias

**Principios**:
- Convierte requests HTTP en llamadas a Use Cases
- Serializa/deserializa datos
- Manejo de errores HTTP

**Ejemplo**:
```python
# presentation/api/v1/hitos.py
@router.get("/proximos", response_model=List[HitoResponse])
async def obtener_hitos_proximos(
    dias: int = 30,
    use_case: ObtenerHitosProximosUseCase = Depends(get_obtener_hitos_use_case)
):
    hitos = use_case.execute(dias)
    return hitos
```

---

## 🎨 Frontend - Arquitectura Limpia Adaptada

### 1️⃣ Domain Layer
- `entities/`: Modelos de dominio (TypeScript interfaces/classes)
- `interfaces/`: Interfaces de repositorios y servicios

### 2️⃣ Application Layer
- `services/`: Lógica de aplicación
- `use_cases/`: Casos de uso del frontend

### 3️⃣ Infrastructure Layer
- `api/`: Cliente HTTP (Axios/Fetch)
- `storage/`: LocalStorage, SessionStorage

### 4️⃣ Presentation Layer
- `components/`: Componentes React
- `pages/`: Páginas/rutas
- `hooks/`: Custom hooks

---

## 🔄 Flujo de Datos (Ejemplo: Crear Hito)

```
1. Usuario → Click en "Agregar Hito"
   ↓
2. React Component (Presentation)
   ↓
3. Service/Hook (Application)
   ↓
4. API Client (Infrastructure) → HTTP POST
   ↓
5. FastAPI Controller (Presentation)
   ↓
6. Use Case (Application)
   ↓
7. Domain Service/Entity (Domain)
   ↓
8. Repository Interface (Domain)
   ↓
9. Repository Implementation (Infrastructure) → DB
   ↓
10. Response ← ← ← ← ← (camino inverso)
```

---

## 🛠️ Stack Tecnológico

### Backend
- **Framework**: FastAPI 0.110+
- **ORM**: SQLAlchemy 2.0
- **Database**: PostgreSQL 15+ / SQLite (dev)
- **Migrations**: Alembic
- **Validación**: Pydantic 2.0
- **Testing**: pytest

### Frontend
- **Framework**: React 18
- **Language**: TypeScript 5.0
- **Build**: Vite
- **State**: TanStack Query (React Query)
- **HTTP**: Axios
- **UI**: Tailwind CSS + shadcn/ui
- **Testing**: Vitest + React Testing Library

### DevOps
- **Containerization**: Docker + Docker Compose
- **CI/CD**: GitHub Actions (opcional)

---

## 📊 Patrones de Diseño Utilizados

1. **Repository Pattern**: Abstracción del acceso a datos
2. **Dependency Injection**: Inversión de control
3. **DTO Pattern**: Transferencia de datos entre capas
4. **Factory Pattern**: Creación de objetos complejos
5. **Strategy Pattern**: Diferentes implementaciones (Excel vs DB)
6. **Observer Pattern**: Sincronización en tiempo real

---

## 🧪 Testing Strategy

- **Unit Tests**: Domain y Application (lógica pura)
- **Integration Tests**: Infrastructure (DB, Excel reader)
- **E2E Tests**: Presentation (API endpoints)
- **Coverage Target**: >80%

---

## 📝 Convenciones de Código

### Backend (Python)
- **Style Guide**: PEP 8
- **Type Hints**: Obligatorio
- **Docstrings**: Google Style
- **Naming**:
  - Classes: `PascalCase`
  - Functions/Methods: `snake_case`
  - Constants: `UPPER_SNAKE_CASE`

### Frontend (TypeScript)
- **Style Guide**: Airbnb + Prettier
- **Naming**:
  - Components: `PascalCase`
  - Functions: `camelCase`
  - Files: `kebab-case.tsx`

---

## 🚀 Ventajas de esta Arquitectura

✅ **Mantenibilidad**: Cambios aislados por capa
✅ **Testeable**: Lógica de negocio independiente
✅ **Escalable**: Fácil agregar nuevas funcionalidades
✅ **Flexible**: Cambiar DB o UI sin afectar el core
✅ **Colaborativo**: Equipos pueden trabajar en paralelo por capas
✅ **Documentación Implícita**: La estructura cuenta la historia

---

## 📚 Referencias

- Clean Architecture - Robert C. Martin
- Domain-Driven Design - Eric Evans
- Hexagonal Architecture - Alistair Cockburn
- SOLID Principles
