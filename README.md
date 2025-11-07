# 🛩️ Sistema de Monitoreo Aéreo - GaserosFC

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/Python-3.9-blue.svg)
![Django](https://img.shields.io/badge/Django-4.2.26-green.svg)
![Svelte](https://img.shields.io/badge/Svelte-5.39.6-orange.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)

Sistema completo de monitoreo y análisis del tráfico aéreo en tiempo real, desarrollado para el **Hackathon GaserosFC**. La plataforma integra datos de la API de OpenSky Network para proporcionar visualización, análisis y almacenamiento persistente de información de vuelos.

## 📋 Tabla de Contenidos

- [Características Principales](#-características-principales)
- [Arquitectura del Sistema](#-arquitectura-del-sistema)
- [Tecnologías Utilizadas](#-tecnologías-utilizadas)
- [Requisitos Previos](#-requisitos-previos)
- [Instalación](#-instalación)
- [Configuración](#-configuración)
- [Uso](#-uso)
- [API Endpoints](#-api-endpoints)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Modelos de Datos](#-modelos-de-datos)
- [Características del Frontend](#-características-del-frontend)
- [Contribuir](#-contribuir)
- [Licencia](#-licencia)

## ✨ Características Principales

### Backend (Django REST API)
- 🔄 **Integración con OpenSky Network API** - Acceso a datos de vuelos en tiempo real
- 💾 **Persistencia de Datos** - Almacenamiento automático en MySQL de snapshots de vuelos
- 🔐 **Autenticación OAuth2** - Integración con sistema de autenticación de OpenSky
- 🚀 **API RESTful** - Endpoints organizados y documentados
- 📊 **Modelos de Datos Optimizados** - Estructura de base de datos eficiente con índices
- 🔍 **Filtrado Avanzado** - Filtros por país de origen, estado, y más
- ⚡ **Operaciones en Lote** - Inserción masiva para mejor rendimiento
- 🛡️ **Manejo de Errores** - Control de rate limiting y excepciones

### Frontend (Svelte)
- 🎨 **Diseño Glassmorphism** - Interfaz moderna con efectos de vidrio esmerilado
- 📱 **Responsive Design** - Adaptable a todos los dispositivos
- 📊 **Visualización de Datos en Tiempo Real** - Gráficos y métricas actualizadas
- 🔍 **Búsqueda y Filtros Avanzados** - Múltiples criterios de filtrado
- 📈 **Dashboard Completo** - Métricas de vuelos, aeropuertos y servicios
- 🚨 **Sistema de Alertas** - Notificaciones en tiempo real
- 🌐 **Monitoreo de Servicios** - Estado de sistemas críticos

## 🏗️ Arquitectura del Sistema

```
┌─────────────────┐      ┌──────────────────┐      ┌─────────────────┐
│   Frontend      │      │    Backend       │      │  OpenSky API    │
│   (Svelte)      │◄────►│    (Django)      │◄────►│                 │
│   Port: 5173    │      │    Port: 8000    │      │  Public API     │
└─────────────────┘      └──────────────────┘      └─────────────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │   MySQL DB       │
                         │   Port: 3306     │
                         │   (hackathon)    │
                         └──────────────────┘
```

### Flujo de Datos

1. **Obtención de Datos**: Backend consulta OpenSky API con autenticación OAuth2
2. **Procesamiento**: Django procesa y estructura los datos de vuelos
3. **Almacenamiento**: Datos guardados en MySQL con snapshots y estados de vuelos
4. **API REST**: Frontend consume endpoints del backend
5. **Visualización**: Svelte renderiza datos en tiempo real con interfaz interactiva

## 🛠️ Tecnologías Utilizadas

### Backend
- **Python 3.9** - Lenguaje de programación
- **Django 4.2.26** - Framework web
- **MySQL** - Base de datos relacional
- **django-cors-headers** - Manejo de CORS
- **python-decouple** - Gestión de variables de entorno
- **requests 2.32.5** - Cliente HTTP para APIs externas
- **mysqlclient 2.2.7** - Conector MySQL

### Frontend
- **Svelte 5.39.6** - Framework JavaScript reactivo
- **Vite 7.1.7** - Build tool y dev server
- **JavaScript ES6+** - Lenguaje de programación
- **CSS3** - Estilos con glassmorphism

### DevOps
- **Docker** - Contenedorización
- **Docker Compose** - Orquestación de contenedores
- **Git** - Control de versiones

### APIs Externas
- **OpenSky Network API** - Datos de vuelos en tiempo real
  - REST API para estados de vuelos
  - OAuth2 para autenticación

## 📦 Requisitos Previos

- **Docker** y **Docker Compose** (recomendado)
- O bien:
  - **Python 3.9+**
  - **Node.js 16+** y **npm**
  - **MySQL 8.0+**
  - **Git**

## 🚀 Instalación

### Opción 1: Docker (Recomendado)

1. **Clonar el repositorio**
```bash
git clone https://github.com/ElRayoRapido09/Hackathon_GaserosFC.git
cd Hackathon_GaserosFC
```

2. **Configurar variables de entorno**
```bash
# Crear archivo .env en la carpeta Backend/
cp Backend/.env.example Backend/.env
# Editar con tus credenciales
```

3. **Iniciar servicios con Docker**
```bash
docker-compose up -d
```

4. **Aplicar migraciones**
```bash
docker exec -it backend-hackathon python manage.py migrate
```

5. **Crear superusuario (opcional)**
```bash
docker exec -it backend-hackathon python manage.py createsuperuser
```

### Opción 2: Instalación Manual

#### Backend

1. **Navegar a la carpeta del backend**
```bash
cd Backend
```

2. **Crear entorno virtual**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar base de datos MySQL**
```sql
CREATE DATABASE hackathon CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'tu_usuario'@'localhost' IDENTIFIED BY 'tu_password';
GRANT ALL PRIVILEGES ON hackathon.* TO 'tu_usuario'@'localhost';
FLUSH PRIVILEGES;
```

5. **Configurar settings.py**
```python
# Editar Backend/zabbix/settings.py con tus credenciales
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hackathon',
        'USER': 'tu_usuario',
        'PASSWORD': 'tu_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

6. **Aplicar migraciones**
```bash
python manage.py migrate
```

7. **Iniciar servidor**
```bash
python manage.py runserver 0.0.0.0:8000
```

#### Frontend

1. **Navegar a la carpeta del frontend**
```bash
cd monitoreo-aereo
```

2. **Instalar dependencias**
```bash
npm install
```

3. **Iniciar servidor de desarrollo**
```bash
npm run dev
```

## ⚙️ Configuración

### Variables de Entorno (Backend)

Crear archivo `.env` en la carpeta `Backend/`:

```env
# Django
SECRET_KEY=tu-secret-key-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=hackathon
DB_USER=root
DB_PASSWORD=12345
DB_HOST=host.docker.internal
DB_PORT=3306

# OpenSky API (opcional - mejora rate limits)
OPENSKY_CLIENT_ID=gaserosfc-api-client
OPENSKY_CLIENT_SECRET=GPsfDsxv8i8MAj9PPN1OEUERM9HhzdCU
```

### CORS Configuration

El backend está configurado para aceptar requests desde:
- `http://localhost:5173` (Frontend en desarrollo)

Para añadir más orígenes, editar `Backend/zabbix/settings.py`:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://tu-dominio.com",
]
```

## 💻 Uso

### Acceder a la Aplicación

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000/api/
- **Admin Django**: http://localhost:8000/admin/

### Funcionalidades Principales

#### 1. Obtener Vuelos Activos
```bash
curl http://localhost:8000/api/flights/
```

#### 2. Filtrar por País
```bash
curl http://localhost:8000/api/flights/?origin_country=Spain
```

#### 3. Guardar Snapshot de Vuelos
```bash
curl http://localhost:8000/api/flights/save/
```

#### 4. Consultar Snapshots Guardados
```bash
curl http://localhost:8000/api/snapshots/
```

#### 5. Obtener Snapshot Específico
```bash
curl http://localhost:8000/api/snapshots/?snapshot_id=1
```

## 📡 API Endpoints

### Base URL: `http://localhost:8000/api/`

| Método | Endpoint | Descripción | Parámetros |
|--------|----------|-------------|------------|
| GET | `/flights/` | Obtiene vuelos activos de OpenSky | `?origin_country=<país>`<br>`?save_to_db=true/false` |
| GET | `/flights/save/` | Obtiene y guarda vuelos | `?origin_country=<país>` |
| GET | `/snapshots/` | Lista de snapshots guardados | `?limit=<número>`<br>`?snapshot_id=<id>` |

### Ejemplos de Respuestas

#### GET `/api/flights/`

```json
{
  "time": 1699377890,
  "states": [
    [
      "abc123",           // icao24
      "UAL123  ",         // callsign
      "United States",    // origin_country
      1699377888,         // time_position
      1699377889,         // last_contact
      -118.4085,          // longitude
      33.9425,            // latitude
      10668.0,            // baro_altitude (m)
      false,              // on_ground
      231.67,             // velocity (m/s)
      45.5,               // true_track (grados)
      -5.2,               // vertical_rate (m/s)
      null,               // sensors
      10700.5,            // geo_altitude (m)
      "1234",             // squawk
      false,              // spi
      0                   // position_source
    ]
  ],
  "db_snapshot": {
    "snapshot_id": 42,
    "total_saved": 8567,
    "saved_at": "2024-11-07T15:45:30.123456Z"
  }
}
```

#### GET `/api/snapshots/?snapshot_id=1`

```json
{
  "snapshot_id": 1,
  "time": 1699377890,
  "total_states": 8567,
  "created_at": "2024-11-07T15:45:30.123456Z",
  "states": [
    {
      "icao24": "abc123",
      "callsign": "UAL123",
      "origin_country": "United States",
      "longitude": -118.4085,
      "latitude": 33.9425,
      "baro_altitude": 10668.0,
      "velocity": 231.67,
      // ... más campos
    }
  ]
}
```

## 📁 Estructura del Proyecto

```
Hackathon_GaserosFC/
├── Backend/                          # Aplicación Django
│   ├── API/                          # Aplicación de API
│   │   ├── migrations/               # Migraciones de base de datos
│   │   │   └── 0001_initial.py      # Migración inicial
│   │   ├── __init__.py
│   │   ├── admin.py                  # Configuración del admin
│   │   ├── apps.py                   # Configuración de la app
│   │   ├── models.py                 # Modelos (FlightSnapshot, FlightState)
│   │   ├── tests.py                  # Tests unitarios
│   │   ├── urls.py                   # URLs de la API
│   │   └── views.py                  # Vistas y lógica de negocio
│   ├── zabbix/                       # Configuración del proyecto
│   │   ├── __init__.py
│   │   ├── asgi.py                   # Configuración ASGI
│   │   ├── settings.py               # Configuración principal
│   │   ├── urls.py                   # URLs principales
│   │   └── wsgi.py                   # Configuración WSGI
│   ├── db.sqlite3                    # Base de datos SQLite (desarrollo)
│   ├── manage.py                     # Script de gestión Django
│   └── requirements.txt              # Dependencias Python
├── monitoreo-aereo/                  # Aplicación Svelte
│   ├── public/                       # Archivos estáticos públicos
│   ├── src/                          # Código fuente
│   │   ├── assets/                   # Assets (imágenes, etc.)
│   │   ├── lib/                      # Componentes reutilizables
│   │   │   └── monitoreo/
│   │   │       └── +page.svelte      # Página de monitoreo
│   │   ├── +page.svelte              # Página principal
│   │   ├── App.svelte                # Componente principal (843 líneas)
│   │   ├── app.css                   # Estilos globales
│   │   └── main.js                   # Punto de entrada
│   ├── index.html                    # HTML principal
│   ├── jsconfig.json                 # Configuración JavaScript
│   ├── package.json                  # Dependencias Node
│   ├── README.md                     # Documentación frontend
│   ├── svelte.config.js              # Configuración Svelte
│   └── vite.config.js                # Configuración Vite
├── docker-compose.yml                # Configuración Docker Compose
└── README.md                         # Este archivo
```

## 🗄️ Modelos de Datos

### FlightSnapshot

Almacena el timestamp de cada consulta a OpenSky API.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | BigAutoField | ID único (PK) |
| `time` | BigIntegerField | Timestamp Unix de la consulta |
| `created_at` | DateTimeField | Fecha de creación del registro |
| `total_states` | IntegerField | Número de estados en el snapshot |

**Relaciones**: Un FlightSnapshot tiene muchos FlightState

### FlightState

Almacena cada estado individual de vuelo según OpenSky API.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | BigAutoField | ID único (PK) |
| `snapshot` | ForeignKey | Referencia al snapshot (FK) |
| `icao24` | CharField(6) | Código ICAO24 del transponder |
| `callsign` | CharField(8) | Indicativo de llamada |
| `origin_country` | CharField(100) | País de origen |
| `time_position` | BigIntegerField | Timestamp de última posición |
| `last_contact` | BigIntegerField | Timestamp de último contacto |
| `longitude` | FloatField | Longitud (grados decimales) |
| `latitude` | FloatField | Latitud (grados decimales) |
| `baro_altitude` | FloatField | Altitud barométrica (metros) |
| `on_ground` | BooleanField | Si está en tierra |
| `velocity` | FloatField | Velocidad (m/s) |
| `true_track` | FloatField | Rumbo verdadero (0-360°) |
| `vertical_rate` | FloatField | Velocidad vertical (m/s) |
| `sensors` | JSONField | Array de IDs de sensores |
| `geo_altitude` | FloatField | Altitud geométrica (metros) |
| `squawk` | CharField(4) | Código transponder |
| `spi` | BooleanField | Si SPI está activo |
| `position_source` | IntegerField | Fuente: 0=ADS-B, 1=ASTERIX, 2=MLAT |
| `created_at` | DateTimeField | Fecha de creación |

**Índices**: Optimizado con múltiples índices para consultas eficientes
**Unique Together**: `(snapshot, icao24, last_contact)`

## 🎨 Características del Frontend

### Secciones del Dashboard

#### 1. 🛩️ Vuelos Activos
- **Vista en tiempo real** de todos los vuelos activos
- **Búsqueda dinámica** por ID, aerolínea o ruta
- **Filtros por estado**: En vuelo, Despegando, Aproximación
- **Ordenamiento**: Por ID, estado o altitud
- **Métricas individuales**: Altitud, velocidad, ETA

#### 2. 🛫 Tráfico Aéreo
- **Estadísticas por aeropuerto**
  - Despegues y llegadas
  - Retrasos
  - Eficiencia operacional
- **Gráficos de tendencias**
- **Filtros temporales**: Diario, semanal, mensual
- **Comparativas entre aeropuertos**

#### 3. 📊 Estadísticas de Vuelo
- **Métricas globales**:
  - Total de vuelos
  - Porcentaje de puntualidad
  - Vuelos retrasados/cancelados
- **Gráficos semanales**:
  - Vuelos a tiempo
  - Vuelos retrasados
  - Vuelos cancelados
- **Análisis de rendimiento**
- **Velocidad promedio de vuelos**
- **Vuelos en ascenso/descenso**

#### 4. ⚙️ Estado del Sistema
- **Monitor de servicios críticos**:
  - Radar Principal
  - Sistema de Comunicación
  - Base de Datos
  - Torre de Control
  - Sistema Meteorológico
  - Sistemas de Backup
- **Métricas de rendimiento**:
  - Uptime
  - Tiempo de respuesta
  - Estado operacional
- **Sistema de alertas** con niveles de prioridad
- **Métricas de recursos**:
  - CPU
  - Memoria
  - Disco
  - Red

### Diseño UI/UX

#### Glassmorphism
- Efectos de vidrio esmerilado con transparencias
- Blur y gradientes dinámicos
- Sombras y bordes sutiles
- Paleta de colores moderna

#### Responsive
- **Mobile First**: Optimizado para móviles
- **Breakpoints**: Tablet y Desktop
- **Touch-friendly**: Botones y controles táctiles
- **Navegación adaptativa**

#### Accesibilidad
- Alto contraste disponible
- Navegación por teclado
- Reducción de animaciones (prefers-reduced-motion)
- Etiquetas ARIA

## 🔐 Seguridad

### Backend
- ✅ Credenciales en variables de entorno
- ✅ CORS configurado correctamente
- ✅ Django middleware de seguridad
- ⚠️ CSRF deshabilitado en endpoints API (configurar en producción)
- ⚠️ DEBUG=True (cambiar a False en producción)
- ⚠️ SECRET_KEY hardcodeada (usar variable de entorno)

### Recomendaciones para Producción
1. Cambiar `DEBUG=False`
2. Usar `SECRET_KEY` desde variable de entorno
3. Configurar HTTPS/SSL
4. Implementar autenticación JWT
5. Rate limiting en endpoints
6. Validación de entrada de datos
7. Sanitización de consultas SQL
8. Implementar CSRF tokens
9. Configurar firewall y security groups
10. Backups automáticos de base de datos

## 🧪 Testing

### Backend
```bash
cd Backend
python manage.py test
```

### Frontend
```bash
cd monitoreo-aereo
npm run test
```

## 📈 Mejoras Futuras

### Funcionalidades
- [ ] Autenticación de usuarios
- [ ] Sistema de notificaciones push
- [ ] Exportación de datos (CSV, JSON, PDF)
- [ ] Predicción de rutas con ML
- [ ] Integración con más APIs de aviación
- [ ] Mapa interactivo con posiciones en tiempo real
- [ ] WebSocket para actualizaciones en tiempo real
- [ ] Sistema de alertas personalizables
- [ ] Dashboard administrativo avanzado

### Optimizaciones
- [ ] Cache con Redis
- [ ] Compresión de respuestas
- [ ] Lazy loading de componentes
- [ ] Service Workers para PWA
- [ ] CDN para assets estáticos
- [ ] Optimización de imágenes
- [ ] Code splitting en frontend

### Infraestructura
- [ ] CI/CD con GitHub Actions
- [ ] Kubernetes para orquestación
- [ ] Monitoreo con Prometheus/Grafana
- [ ] Logs centralizados con ELK Stack
- [ ] Testing automatizado
- [ ] Deploy en la nube (AWS/Azure/GCP)

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

### Guidelines
- Seguir PEP 8 para Python
- Usar ESLint para JavaScript
- Comentar código complejo
- Incluir tests para nuevas funcionalidades
- Actualizar documentación

## 📝 Licencia

Este proyecto fue desarrollado para el **Hackathon GaserosFC**.

## 👥 Autores

- **ElRayoRapido09** - [GitHub](https://github.com/ElRayoRapido09)

## 🙏 Agradecimientos

- **OpenSky Network** - Por proporcionar la API de datos de vuelos
- **Comunidad Django** - Por el excelente framework
- **Comunidad Svelte** - Por el increíble framework reactivo
- **Hackathon GaserosFC** - Por la oportunidad

## 📞 Contacto

Para preguntas o soporte:
- GitHub Issues: [Crear Issue](https://github.com/ElRayoRapido09/Hackathon_GaserosFC/issues)
- Email: [Tu email aquí]

## 📚 Referencias

- [OpenSky Network API Documentation](https://openskynetwork.github.io/opensky-api/)
- [Django Documentation](https://docs.djangoproject.com/)
- [Svelte Documentation](https://svelte.dev/docs)
- [Docker Documentation](https://docs.docker.com/)

---

⭐ Si te gusta este proyecto, dale una estrella en GitHub!

**Desarrollado con ❤️ para el Hackathon GaserosFC**
