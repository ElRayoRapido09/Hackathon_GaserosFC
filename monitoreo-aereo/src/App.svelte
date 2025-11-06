<script>
  import { onMount } from 'svelte';
  
  // Datos de ejemplo
  let flightsData = [
    { id: 'AA123', airline: 'American Airlines', route: 'NYC → LAX', status: 'En vuelo', altitude: '35,000 ft', speed: '520 mph', eta: '14:30' },
    { id: 'UA456', airline: 'United Airlines', route: 'LAX → CHI', status: 'Despegando', altitude: '5,000 ft', speed: '180 mph', eta: '16:45' },
    { id: 'DL789', airline: 'Delta Airlines', route: 'MIA → ATL', status: 'Aproximación', altitude: '8,000 ft', speed: '250 mph', eta: '13:15' },
    { id: 'SW101', airline: 'Southwest Airlines', route: 'DAL → HOU', status: 'En vuelo', altitude: '28,000 ft', speed: '480 mph', eta: '15:20' },
    { id: 'BA202', airline: 'British Airways', route: 'LHR → JFK', status: 'En vuelo', altitude: '41,000 ft', speed: '580 mph', eta: '18:00' },
    { id: 'AF303', airline: 'Air France', route: 'CDG → LAX', status: 'En vuelo', altitude: '39,000 ft', speed: '560 mph', eta: '19:30' },
    { id: 'LH404', airline: 'Lufthansa', route: 'FRA → JFK', status: 'Despegando', altitude: '12,000 ft', speed: '320 mph', eta: '17:45' },
    { id: 'KL505', airline: 'KLM', route: 'AMS → SFO', status: 'En vuelo', altitude: '37,000 ft', speed: '540 mph', eta: '20:15' }
  ];

  let airportsData = [
    { airport: 'JFK', departures: 45, arrivals: 52, delays: 8, efficiency: 89 },
    { airport: 'LAX', departures: 38, arrivals: 41, delays: 3, efficiency: 95 },
    { airport: 'CHI', departures: 29, arrivals: 33, delays: 7, efficiency: 82 },
    { airport: 'MIA', departures: 22, arrivals: 19, delays: 2, efficiency: 93 },
    { airport: 'ATL', departures: 35, arrivals: 28, delays: 5, efficiency: 87 },
    { airport: 'SFO', departures: 31, arrivals: 34, delays: 4, efficiency: 90 }
  ];

  let servicesData = [
    { name: 'Radar Principal', status: 'operational', uptime: 99.9, responseTime: 45 },
    { name: 'Sistema de Comunicación', status: 'operational', uptime: 99.8, responseTime: 32 },
    { name: 'Base de Datos', status: 'warning', uptime: 98.5, responseTime: 120 },
    { name: 'Torre de Control', status: 'operational', uptime: 100, responseTime: 12 },
    { name: 'Sistema Meteorológico', status: 'operational', uptime: 99.6, responseTime: 67 },
    { name: 'Backup Systems', status: 'maintenance', uptime: 95.2, responseTime: 0 }
  ];

  let alertsData = [
    { id: 1, type: 'warning', message: 'Base de datos experimentando latencia elevada', time: '10:30', severity: 'medium' },
    { id: 2, type: 'info', message: 'Mantenimiento programado para sistemas de backup', time: '09:15', severity: 'low' },
    { id: 3, type: 'success', message: 'Radar principal funcionando correctamente', time: '08:45', severity: 'info' },
    { id: 4, type: 'error', message: 'Fallo temporal en comunicaciones sector 3', time: '11:20', severity: 'high' }
  ];

  let chartData = [
    { day: 'Lun', flights: 187, onTime: 165, delayed: 18, cancelled: 4 },
    { day: 'Mar', flights: 203, onTime: 178, delayed: 21, cancelled: 4 },
    { day: 'Mié', flights: 195, onTime: 172, delayed: 19, cancelled: 4 },
    { day: 'Jue', flights: 218, onTime: 191, delayed: 23, cancelled: 4 },
    { day: 'Vie', flights: 234, onTime: 205, delayed: 25, cancelled: 4 },
    { day: 'Sáb', flights: 156, onTime: 138, delayed: 15, cancelled: 3 },
    { day: 'Dom', flights: 142, onTime: 126, delayed: 13, cancelled: 3 }
  ];

  // Variables reactivas
  let activeSection = 'flights';
  let period = 'daily';
  let searchTerm = '';
  let statusFilter = 'all';
  let sortBy = 'id';
  let currentTime = new Date();

  // Variables para seguimiento de vuelos en tiempo real
  let realFlights = [];
  let totalFlights = 0;
  let onTimeCount = 0;
  let delayedCount = 0;
  let cancelledCount = 0;

  async function fetchCurrentStats() {
    try {
      const response = await fetch('http://localhost:8000/api/get_active_flights');  // Ajusta URL/puerto según sea necesario
      const data = await response.json();
      realFlights = data.states || [];
      totalFlights = realFlights.length;
      // Estimar a tiempo/retrasado/cancelado (OpenSky no lo proporciona; usando suposiciones)
      onTimeCount = Math.floor(totalFlights * 0.88);
      delayedCount = Math.floor(totalFlights * 0.10);
      cancelledCount = totalFlights - onTimeCount - delayedCount;
    } catch (error) {
      console.error('Error obteniendo estadísticas actuales:', error);
    }
  }

  // Obtener datos históricos para el gráfico semanal
  async function fetchChartData() {
    const newChartData = [];
    const days = ['Dom', 'Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb'];
    const now = new Date();
    for (let i = 6; i >= 0; i--) {
      const date = new Date(now);
      date.setDate(now.getDate() - i);
      const begin = Math.floor(date.setHours(0, 0, 0, 0) / 1000);
      const end = begin + 24 * 60 * 60;
      try {
        const response = await fetch(`http://localhost:8000/api/get_active_flights?begin=${begin}&end=${end}`);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const flights = await response.json() || [];
        const total = flights.length;
        const onTime = Math.floor(total * 0.88);
        const delayed = Math.floor(total * 0.10);
        const cancelled = total - onTime - delayed;
        newChartData.push({
          day: days[date.getDay()],
          flights: total,
          onTime,
          delayed,
          cancelled
        });
      } catch (error) {
        console.error('Error obteniendo datos del gráfico para día', i, ':', error);
        // Mantener datos anteriores si hay error, o usar 0
        const existingDay = chartData.find(d => d.day === days[date.getDay()]);
        newChartData.push(existingDay || { day: days[date.getDay()], flights: 0, onTime: 0, delayed: 0, cancelled: 0 });
      }
    }
    return newChartData;
  }

  // Vuelos filtrados
  $: filteredFlights = flightsData.filter(flight => {
    const matchesSearch = flight.id.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         flight.airline.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         flight.route.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = statusFilter === 'all' || flight.status === statusFilter;
    return matchesSearch && matchesStatus;
  }).sort((a, b) => {
    if (sortBy === 'id') return a.id.localeCompare(b.id);
    if (sortBy === 'status') return a.status.localeCompare(b.status);
    if (sortBy === 'altitude') return parseInt(a.altitude) - parseInt(b.altitude);
    return 0;
  });

  // Variables para estadísticas calculadas de chartData
  $: totalWeeklyFlights = chartData.reduce((sum, day) => sum + day.flights, 0);
  $: totalOnTime = chartData.reduce((sum, day) => sum + day.onTime, 0);
  $: totalDelayed = chartData.reduce((sum, day) => sum + day.delayed, 0);
  $: totalCancelled = chartData.reduce((sum, day) => sum + day.cancelled, 0);
  $: onTimePercentage = totalWeeklyFlights > 0 ? ((totalOnTime / totalWeeklyFlights) * 100).toFixed(1) : 0;
  $: delayedPercentage = totalWeeklyFlights > 0 ? ((totalDelayed / totalWeeklyFlights) * 100).toFixed(1) : 0;
  $: cancelledPercentage = totalWeeklyFlights > 0 ? ((totalCancelled / totalWeeklyFlights) * 100).toFixed(1) : 0;

  // Funciones de utilidad
  function getStatusColor(status) {
    switch(status) {
      case 'En vuelo': return '#22c55e';
      case 'Despegando': return '#f59e0b';
      case 'Aproximación': return '#ef4444';
      case 'operational': return '#22c55e';
      case 'warning': return '#f59e0b';
      case 'error': return '#ef4444';
      case 'maintenance': return '#8b5cf6';
      default: return '#6b7280';
    }
  }

  function getStatusIcon(status) {
    switch(status) {
      case 'operational': return '✅';
      case 'warning': return '⚠️';
      case 'error': return '❌';
      case 'maintenance': return '🔧';
      default: return '❓';
    }
  }

  function getAlertIcon(type) {
    switch(type) {
      case 'success': return '✅';
      case 'warning': return '⚠️';
      case 'error': return '❌';
      case 'info': return 'ℹ️';
      default: return '📝';
    }
  }

  function getEfficiencyColor(efficiency) {
    if (efficiency >= 90) return '#22c55e';
    if (efficiency >= 80) return '#f59e0b';
    return '#ef4444';
  }

  function showSection(sectionId) {
    activeSection = sectionId;
  }

  function setPeriod(newPeriod) {
    period = newPeriod;
  }

  // Actualizar tiempo cada segundo
  onMount(() => {
    (async () => {
      await fetchCurrentStats();
      chartData = await fetchChartData();
    })();

    const updateInterval = setInterval(async () => {
      try {
        await fetchCurrentStats();
        chartData = await fetchChartData();
      } catch (error) {
        console.error('Error actualizando datos:', error);
      }
    }, 30 * 60 * 1000); // 30 minutos

    const timeInterval = setInterval(() => {
      currentTime = new Date();
    }, 1000);

    return () => {
      clearInterval(updateInterval);
      clearInterval(timeInterval);
    };
  });

  // Simulación de actualizaciones en tiempo real
  onMount(() => {
    const updateInterval = setInterval(() => {
      if (Math.random() > 0.7) {
        const randomFlight = flightsData[Math.floor(Math.random() * flightsData.length)];
        const altitudes = ['25,000 ft', '30,000 ft', '35,000 ft', '40,000 ft'];
        randomFlight.altitude = altitudes[Math.floor(Math.random() * altitudes.length)];
        flightsData = [...flightsData]; // Trigger reactivity
      }
    }, 5000);

    return () => clearInterval(updateInterval);
  });
</script>

<div class="app">
  <!-- Header -->
  <header class="header">
    <div class="header-content">
      <div class="logo-section">
        <div class="logo">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none">
            <path d="M12 2L22 9L20 11L12 18L4 11L2 9L12 2Z" fill="currentColor"/>
            <path d="M12 10L18 6L12 2L6 6L12 10Z" fill="currentColor" opacity="0.7"/>
          </svg>
        </div>
        <div class="title">
          <h1>Control Aéreo</h1>
          <span class="subtitle">Sistema de Monitoreo</span>
        </div>
      </div>
      <div class="status-section">
        <div class="time">{currentTime.toLocaleTimeString('es-ES')}</div>
        <div class="status-indicator">
          <div class="status-dot active"></div>
          <span>Sistema Activo</span>
        </div>
      </div>
    </div>
  </header>

  <div class="main-container">
    <!-- Sidebar -->
    <aside class="sidebar">
      <nav class="nav-menu">
        
        <button class="nav-item" class:active={activeSection === 'flights'} on:click={() => showSection('flights')}>
          <span class="nav-icon">✈️</span>
          <span class="nav-label">Vuelos Activos</span>
        </button>
        <button class="nav-item" class:active={activeSection === 'traffic'} on:click={() => showSection('traffic')}>
          <span class="nav-icon">🛫</span>
          <span class="nav-label">Tráfico Aéreo</span>
        </button>
        <button class="nav-item" class:active={activeSection === 'stats'} on:click={() => showSection('stats')}>
          <span class="nav-icon">📊</span>
          <span class="nav-label">Estadísticas</span>
        </button>
        <button class="nav-item" class:active={activeSection === 'system'} on:click={() => showSection('system')}>
          <span class="nav-icon">⚙️</span>
          <span class="nav-label">Estado Sistema</span>
        </button>
        <button class="nav-item" class:active={activeSection === 'map'} on:click={() => showSection('map')}>
          <span class="nav-icon">🗺️</span>
          <span class="nav-label">Mapa Global</span>
        </button>
      </nav>
      <div class="sidebar-footer">
        <div class="quick-stats">
          <div class="stat-item">
            <span class="stat-value">{flightsData.length}</span>
            <span class="stat-label">Vuelos</span>
          </div>
          <div class="stat-item">
            <span class="stat-value">{alertsData.filter(a => a.type === 'warning' || a.type === 'error').length}</span>
            <span class="stat-label">Alertas</span>
          </div>
        </div>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="content">

      {#if activeSection === 'map'}
        <div class="map-container" style="width:100%;height:80vh;position:relative;">
                            
                            <iframe src="https://openflights.org/?lang=es_ES" width="100%" height="100%" style="border:none;"></iframe>
                        </div>
      {/if}

  <!-- Vuelos Activos Section -->
      {#if activeSection === 'flights'}
        <div class="section active">
          <div class="section-header">
            <h2 class="section-title">Vuelos Activos</h2>
            <div class="live-indicator">
              <div class="pulse-dot"></div>
              <span>EN VIVO</span>
            </div>
          </div>
          
          <div class="filters-section">
            <div class="search-box">
              <svg class="search-icon" width="20" height="20" viewBox="0 0 24 24" fill="none">
                <circle cx="11" cy="11" r="8" stroke="currentColor" stroke-width="2"/>
                <path d="21 21l-4.35-4.35" stroke="currentColor" stroke-width="2"/>
              </svg>
              <input type="text" placeholder="Buscar vuelos..." class="search-input" bind:value={searchTerm}>
            </div>
            <select class="filter-select" bind:value={statusFilter}>
              <option value="all">Todos los estados</option>
              <option value="En vuelo">En vuelo</option>
              <option value="Despegando">Despegando</option>
              <option value="Aproximación">Aproximación</option>
            </select>
            <select class="filter-select" bind:value={sortBy}>
              <option value="id">Ordenar por ID</option>
              <option value="status">Ordenar por Estado</option>
              <option value="altitude">Ordenar por Altitud</option>
            </select>
          </div>
          
          <div class="flights-grid">
            {#each filteredFlights as flight}
              <div class="flight-card">
                <div class="flight-header">
                  <h3 class="flight-id">{flight.id}</h3>
                  <div class="status-badge" style="background-color: {getStatusColor(flight.status)}">
                    {flight.status}
                  </div>
                </div>
                <div class="flight-info">
                  <div class="airline">{flight.airline}</div>
                  <div class="route">{flight.route}</div>
                </div>
                <div class="flight-metrics">
                  <div class="metric">
                    <span class="metric-label">Altitud</span>
                    <span class="metric-value">{flight.altitude}</span>
                  </div>
                  <div class="metric">
                    <span class="metric-label">Velocidad</span>
                    <span class="metric-value">{flight.speed}</span>
                  </div>
                  <div class="metric">
                    <span class="metric-label">ETA</span>
                    <span class="metric-value">{flight.eta}</span>
                  </div>
                </div>
              </div>
            {/each}
          </div>
        </div>
      {/if}

      <!-- Tráfico Aéreo Section -->
      {#if activeSection === 'traffic'}
        <div class="section active">
          <div class="section-header">
            <h2 class="section-title">Tráfico Aéreo</h2>
            <div class="last-update">
              Última actualización: {currentTime.toLocaleTimeString('es-ES')}
            </div>
          </div>
          
          <div class="overview-cards">
            <div class="stat-card primary">
              <div class="stat-icon">🛩️</div>
              <div class="stat-content">
                <div class="stat-value">284</div>
                <div class="stat-label">Vuelos Totales</div>
              </div>
            </div>
            <div class="stat-card">
              <div class="stat-icon">🛫</div>
              <div class="stat-content">
                <div class="stat-value">142</div>
                <div class="stat-label">Salidas</div>
              </div>
            </div>
            <div class="stat-card">
              <div class="stat-icon">🛬</div>
              <div class="stat-content">
                <div class="stat-value">142</div>
                <div class="stat-label">Llegadas</div>
              </div>
            </div>
            <div class="stat-card warning">
              <div class="stat-icon">⚠️</div>
              <div class="stat-content">
                <div class="stat-value">23</div>
                <div class="stat-label">Retrasos</div>
              </div>
            </div>
          </div>
          
          <div class="airports-grid">
            {#each airportsData as airport}
              <div class="airport-card">
                <div class="airport-header">
                  <h4 class="airport-code">{airport.airport}</h4>
                  <div class="efficiency-badge" style="background-color: {getEfficiencyColor(airport.efficiency)}">
                    {airport.efficiency}%
                  </div>
                </div>
                <div class="traffic-metrics">
                  <div class="metric">
                    <span class="metric-label">Salidas</span>
                    <span class="metric-value">{airport.departures}</span>
                  </div>
                  <div class="metric">
                    <span class="metric-label">Llegadas</span>
                    <span class="metric-value">{airport.arrivals}</span>
                  </div>
                  <div class="metric">
                    <span class="metric-label">Retrasos</span>
                    <span class="metric-value">{airport.delays}</span>
                  </div>
                </div>
                <div class="progress-bar">
                  <div class="progress-fill" style="width: {airport.efficiency}%; background-color: {getEfficiencyColor(airport.efficiency)}"></div>
                </div>
              </div>
            {/each}
          </div>
        </div>
      {/if}

      <!-- Estadísticas Section -->
      {#if activeSection === 'stats'}
        <div class="section active">
          <div class="section-header">
            <h2 class="section-title">Estadísticas de Vuelo</h2>
            <div class="period-tabs">
              <button class="tab" class:active={period === 'daily'} on:click={() => setPeriod('daily')}>Diario</button>
              <button class="tab" class:active={period === 'weekly'} on:click={() => setPeriod('weekly')}>Semanal</button>
              <button class="tab" class:active={period === 'monthly'} on:click={() => setPeriod('monthly')}>Mensual</button>
            </div>
          </div>
          
          <div class="overview-stats">
            <div class="stat-card primary">
              <div class="stat-header">
                <span class="stat-icon">✈️</span>
                <span class="stat-title">Total de Vuelos</span>
              </div>
              <div class="stat-value">{totalWeeklyFlights}</div>
              <div class="stat-change positive">+5.2% vs período anterior</div>
            </div>
            <div class="stat-card success">
              <div class="stat-header">
                <span class="stat-icon">✅</span>
                <span class="stat-title">A Tiempo</span>
              </div>
              <div class="stat-value">{totalOnTime}</div>
              <div class="stat-percentage">{onTimePercentage}%</div>
            </div>
            <div class="stat-card warning">
              <div class="stat-header">
                <span class="stat-icon">⏰</span>
                <span class="stat-title">Retrasados</span>
              </div>
              <div class="stat-value">{totalDelayed}</div>
              <div class="stat-percentage">{delayedPercentage}%</div>
            </div>
            <div class="stat-card danger">
              <div class="stat-header">
                <span class="stat-icon">❌</span>
                <span class="stat-title">Cancelados</span>
              </div>
              <div class="stat-value">{totalCancelled}</div>
              <div class="stat-percentage">{cancelledPercentage}%</div>
            </div>
          </div>
          
          <div class="charts-section">
            <div class="chart-container">
              <h3 class="chart-title">Tendencia Semanal</h3>
              <div class="bar-chart">
                {#each chartData as day}
                  <div class="bar-group">
                    <div class="bars">
                      <div class="bar total" style="height: {(day.flights / 250) * 100}%" title="Total: {day.flights}"></div>
                      <div class="bar on-time" style="height: {(day.onTime / 250) * 100}%" title="A tiempo: {day.onTime}"></div>
                      <div class="bar delayed" style="height: {(day.delayed / 250) * 100}%" title="Retrasados: {day.delayed}"></div>
                    </div>
                    <div class="bar-label">{day.day}</div>
                  </div>
                {/each}
              </div>
            </div>
            <div class="performance-metrics">
              <h3 class="chart-title">Métricas de Rendimiento</h3>
              <div class="metric-card">
                <div class="metric-header">
                  <span class="metric-label">Eficiencia General</span>
                  <span class="metric-value">88.1%</span>
                </div>
                <div class="progress-bar">
                  <div class="progress-fill" style="width: 88.1%; background-color: #f59e0b"></div>
                </div>
              </div>
              <div class="metric-card">
                <div class="metric-header">
                  <span class="metric-label">Retraso Promedio</span>
                  <span class="metric-value">15 min</span>
                </div>
                <div class="delay-indicator good">Excelente</div>
              </div>
            </div>
          </div>
        </div>
      {/if}

      <!-- Sistema Section -->
      {#if activeSection === 'system'}
        <div class="section active">
          <div class="section-header">
            <h2 class="section-title">Estado del Sistema</h2>
            <div class="system-overview">
              <div class="status-indicator operational">
                <span class="status-dot"></span>
                <span class="status-text">Operacional</span>
              </div>
              <div class="uptime">Disponibilidad: 99.7%</div>
            </div>
          </div>
          
          <div class="overview-cards">
            <div class="overview-card">
              <div class="card-icon">⏱️</div>
              <div class="card-content">
                <div class="card-value">99.7%</div>
                <div class="card-label">Tiempo de actividad</div>
              </div>
            </div>
            <div class="overview-card">
              <div class="card-icon">🕐</div>
              <div class="card-content">
                <div class="card-value">2 días</div>
                <div class="card-label">Último incidente</div>
              </div>
            </div>
            <div class="overview-card">
              <div class="card-icon">🔧</div>
              <div class="card-content">
                <div class="card-value">5/6</div>
                <div class="card-label">Servicios activos</div>
              </div>
            </div>
            <div class="overview-card">
              <div class="card-icon">🚨</div>
              <div class="card-content">
                <div class="card-value">{alertsData.filter(a => a.type === 'warning' || a.type === 'error').length}</div>
                <div class="card-label">Alertas activas</div>
              </div>
            </div>
          </div>
          
          <div class="performance-section">
            <h3 class="subsection-title">Rendimiento del Sistema</h3>
            <div class="performance-grid">
              <div class="performance-card">
                <div class="performance-header">
                  <span class="performance-label">CPU</span>
                  <span class="performance-value">67%</span>
                </div>
                <div class="progress-bar">
                  <div class="progress-fill" style="width: 67%; background-color: #f59e0b"></div>
                </div>
              </div>
              <div class="performance-card">
                <div class="performance-header">
                  <span class="performance-label">Memoria</span>
                  <span class="performance-value">72%</span>
                </div>
                <div class="progress-bar">
                  <div class="progress-fill" style="width: 72%; background-color: #f59e0b"></div>
                </div>
              </div>
              <div class="performance-card">
                <div class="performance-header">
                  <span class="performance-label">Disco</span>
                  <span class="performance-value">45%</span>
                </div>
                <div class="progress-bar">
                  <div class="progress-fill" style="width: 45%; background-color: #22c55e"></div>
                </div>
              </div>
              <div class="performance-card">
                <div class="performance-header">
                  <span class="performance-label">Red</span>
                  <span class="performance-value">89%</span>
                </div>
                <div class="progress-bar">
                  <div class="progress-fill" style="width: 89%; background-color: #ef4444"></div>
                </div>
              </div>
            </div>
          </div>
          
          <div class="main-content-system">
            <div class="services-section">
              <h3 class="subsection-title">Estado de Servicios</h3>
              <div class="services-list">
                {#each servicesData as service}
                  <div class="service-card">
                    <div class="service-header">
                      <div class="service-name">
                        <span class="service-icon">{getStatusIcon(service.status)}</span>
                        <span class="service-title">{service.name}</span>
                      </div>
                      <div class="service-status" style="color: {getStatusColor(service.status)}">
                        {service.status === 'operational' ? 'Operacional' : 
                         service.status === 'warning' ? 'Advertencia' :
                         service.status === 'maintenance' ? 'Mantenimiento' : 'Error'}
                      </div>
                    </div>
                    <div class="service-metrics">
                      <div class="metric">
                        <span class="metric-label">Disponibilidad</span>
                        <span class="metric-value">{service.uptime}%</span>
                      </div>
                      <div class="metric">
                        <span class="metric-label">Tiempo de respuesta</span>
                        <span class="metric-value">{service.responseTime}ms</span>
                      </div>
                    </div>
                    <div class="uptime-bar">
                      <div class="uptime-fill" style="width: {service.uptime}%; background-color: {getStatusColor(service.status)}"></div>
                    </div>
                  </div>
                {/each}
              </div>
            </div>
            
            <div class="alerts-section">
              <h3 class="subsection-title">Alertas del Sistema</h3>
              <div class="alerts-list">
                {#each alertsData as alert}
                  <div class="alert-card {alert.type}">
                    <div class="alert-icon">{getAlertIcon(alert.type)}</div>
                    <div class="alert-content">
                      <div class="alert-message">{alert.message}</div>
                      <div class="alert-time">{alert.time}</div>
                    </div>
                  </div>
                {/each}
              </div>
            </div>
          </div>
        </div>
      {/if}
    </main>
  </div>
</div>

<style>
  .app {
    min-height: 100vh;
    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  }
  
  .main-container {
    display: flex;
    min-height: calc(100vh - 80px);
  }
  
  @media (max-width: 768px) {
    .main-container {
      flex-direction: column;
    }
  }
</style>
