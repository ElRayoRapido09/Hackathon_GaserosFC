# Sistema de Monitoreo Aéreo

Una aplicación web moderna y elegante para el monitoreo y control del tráfico aéreo, construida con Svelte y diseñada con una interfaz glassmorphism.

## 🚀 Características

### 🛩️ **Vuelos Activos**
- Visualización en tiempo real de vuelos activos
- Información detallada de cada vuelo (ID, aerolínea, ruta, estado)
- Métricas de vuelo (altitud, velocidad, ETA)
- Filtros avanzados por búsqueda, estado y criterios de ordenación
- Indicadores de estado en tiempo real

### 🛫 **Tráfico Aéreo**
- Estadísticas generales del tráfico aéreo
- Monitoreo por aeropuertos con métricas de eficiencia
- Visualización de salidas, llegadas y retrasos
- Filtros por periodo de tiempo y aeropuerto específico
- Métricas de rendimiento por ubicación

### 📊 **Estadísticas de Vuelo**
- Análisis detallado de rendimiento de vuelos
- Gráficos de tendencias semanales
- Métricas de puntualidad y eficiencia
- Estadísticas por aerolínea
- Comparativas por periodos (diario, semanal, mensual)

### ⚙️ **Estado del Sistema**
- Monitor en tiempo real del estado de todos los servicios
- Alertas y notificaciones del sistema
- Métricas de rendimiento (CPU, memoria, disco, red)
- Estado de servicios críticos (radar, comunicación, base de datos)
- Panel de alertas con niveles de prioridad

## 🎨 **Diseño y UX**

### **Glassmorphism UI**
- Interfaz moderna con efectos de vidrio esmerilado
- Transparencias y desenfoques para un aspecto elegante
- Gradientes dinámicos y efectos de luz

### **Responsive Design**
- Adaptable a dispositivos móviles, tablets y desktop
- Navegación optimizada para pantallas táctiles
- Componentes que se reorganizan según el tamaño de pantalla

### **Accesibilidad**
- Soporte para modo de alto contraste
- Animaciones reducidas para usuarios sensibles al movimiento
- Navegación por teclado optimizada

## 🛠️ **Tecnologías Utilizadas**

- **Frontend**: Svelte + Vite
- **Estilos**: CSS3 con variables personalizadas
- **Fuentes**: Inter (interfaz) + JetBrains Mono (datos)
- **Iconos**: Emojis nativos para máxima compatibilidad
- **Animaciones**: CSS Animations y Transitions

## 🚀 **Instalación y Uso**

### **Prerrequisitos**
- Node.js (versión 16 o superior)
- npm o yarn

### **Instalación**
```bash
# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm run dev
```

### **Scripts Disponibles**
```bash
# Desarrollo
npm run dev

# Construcción para producción
npm run build

# Vista previa de la construcción
npm run preview

# Verificación de tipos
npm run check
```

## 📱 **Estructura de Componentes**

```
src/
├── lib/
│   └── components/
│       ├── Header.svelte          # Cabecera principal
│       ├── Sidebar.svelte         # Navegación lateral
│       ├── ActiveFlights.svelte   # Panel de vuelos activos
│       ├── AirTraffic.svelte      # Panel de tráfico aéreo
│       ├── FlightStats.svelte     # Panel de estadísticas
│       └── SystemStatus.svelte    # Panel de estado del sistema
├── +page.svelte                   # Página principal
├── app.css                        # Estilos globales
└── main.js                        # Punto de entrada
```

## 🎯 **Funcionalidades de Filtrado**

### **Vuelos Activos**
- **Búsqueda**: Por ID de vuelo, aerolínea o ruta
- **Estado**: Filtrar por estado (En vuelo, Despegando, Aproximación)
- **Ordenación**: Por ID, estado o altitud

### **Tráfico Aéreo**
- **Periodo**: Última hora, 6 horas, 24 horas, semana
- **Aeropuerto**: Todos o aeropuerto específico
- **Tipo**: Todos los vuelos, alto tráfico, con retrasos

### **Estadísticas**
- **Periodo**: Diario, semanal, mensual
- **Métrica**: Vuelos totales, a tiempo, retrasados
- **Aerolínea**: Todas o aerolínea específica

### **Estado del Sistema**
- **Servicios**: Todos, solo operacionales, con problemas
- **Alertas**: Todas, por nivel de prioridad (alta, media, baja)

## 🎨 **Paleta de Colores**

- **Primario**: Azul (#3b82f6, #60a5fa)
- **Éxito**: Verde (#22c55e)
- **Advertencia**: Naranja (#f59e0b)
- **Peligro**: Rojo (#ef4444)
- **Mantenimiento**: Púrpura (#8b5cf6)
- **Fondo**: Gradiente azul (#1e3c72 → #2a5298)

## 📊 **Métricas en Tiempo Real**

La aplicación simula datos en tiempo real para:
- Contadores de vuelos activos
- Estados de servicios del sistema
- Alertas y notificaciones
- Métricas de rendimiento
- Indicadores de tiempo

---

**Desarrollado con ❤️ usando Svelte y tecnologías web modernas**
