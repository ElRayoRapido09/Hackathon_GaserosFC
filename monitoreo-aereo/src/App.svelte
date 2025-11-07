<script>
  import { onMount } from 'svelte';
  
  // Variables para datos de DB
  let dbFlights = [];  // Estados de vuelos del último snapshot
  let dbSnapshots = [];  // Lista de snapshots
  let lastSnapshot = null;  // Último snapshot para estadísticas
  let airportsData = [];  // Calcular dinámicamente de DB
  
  // Variables reactivas
  let activeSection = 'flights';
  let period = 'daily';
  let searchTerm = '';
  let statusFilter = 'all';
  let sortBy = 'id';
  let currentTime = new Date();
  let chartData = [];  // Declarar chartData para evitar error de referencia

  // Variables para seguimiento de vuelos en tiempo real
  let realFlights = [];
  let totalFlights = 0;
  let onTimeCount = 0;
  let delayedCount = 0;
  let cancelledCount = 0;

  // Declarar filteredFlights primero para evitar errores de referencia
  let filteredFlights = [];

  // Nueva función: Obtener vuelos activos de DB (último snapshot)
  async function fetchFlightsFromDB() {
    try {
      const response = await fetch('http://localhost:8000/api/snapshots/?limit=1');  // Obtener el último snapshot
      if (!response.ok) throw new Error('Error al obtener snapshots');
      const data = await response.json();
      if (data.snapshots && data.snapshots.length > 0) {
        lastSnapshot = data.snapshots[0];
        dbFlights = lastSnapshot.states || [];  // Estados de vuelos del snapshot
        // Calcular airportsData dinámicamente de los países de origen
        const countryCounts = {};
        dbFlights.forEach(flight => {
          const country = flight.origin_country || 'Desconocido';
          if (!countryCounts[country]) {
            countryCounts[country] = { departures: 0, arrivals: 0, delays: 0, efficiency: 90 };  // Eficiencia simulada
          }
          countryCounts[country].departures += 1;  // Simular salidas
          countryCounts[country].arrivals += 1;    // Simular llegadas
          countryCounts[country].delays += Math.random() > 0.8 ? 1 : 0;  // Simular retrasos aleatorios
        });
        airportsData = Object.keys(countryCounts).map(country => ({
          airport: country,  // Usar país como "aeropuerto"
          departures: countryCounts[country].departures,
          arrivals: countryCounts[country].arrivals,
          delays: countryCounts[country].delays,
          efficiency: countryCounts[country].efficiency
        }));
      } else {
        dbFlights = [];
        airportsData = [];
      }
    } catch (error) {
      console.error('Error obteniendo vuelos de DB:', error);
      dbFlights = [];
      airportsData = [];
    }
  }
  
  // Nueva función: Obtener estadísticas de DB (basadas en último snapshot)
  async function fetchStatsFromDB() {
    try {
      const response = await fetch('http://localhost:8000/api/snapshots/?limit=1');
      if (!response.ok) throw new Error('Error al obtener estadísticas');
      const data = await response.json();
      if (data.snapshots && data.snapshots.length > 0) {
        const snapshot = data.snapshots[0];
        const states = snapshot.states || [];
        totalFlights = states.length;
        onTimeCount = Math.floor(totalFlights * 0.88);  // Simulación de "a tiempo"
        delayedCount = Math.floor(totalFlights * 0.10);
        cancelledCount = totalFlights - onTimeCount - delayedCount;
        realFlights = states.map(state => ({
          icao24: state.icao24,
          callsign: state.callsign,
          origin_country: state.origin_country,
          velocity: state.velocity,
          vertical_rate: state.vertical_rate,
          geo_altitude: state.geo_altitude,
          // Agrega otros campos si los necesitas
        }));
      } else {
        totalFlights = 0;
        realFlights = [];
      }
    } catch (error) {
      console.error('Error obteniendo estadísticas de DB:', error);
      totalFlights = 0;
      realFlights = [];
    }
  }
  
  // Nueva función: Obtener y guardar vuelos actuales en DB (para actualizar datos)
  async function fetchAndSaveCurrentFlights() {
    try {
      const response = await fetch('http://localhost:8000/api/flights/?save_to_db=true');  // Guarda en DB automáticamente
      if (!response.ok) throw new Error('Error al obtener/guardar vuelos actuales');
      // No procesar respuesta específica, solo asegurar que se guarde
    } catch (error) {
      console.error('Error obteniendo/guardando vuelos actuales:', error);
    }
  }

  // Variables para estadísticas calculadas de chartData
  $: totalWeeklyFlights = chartData[0]?.flights || 0;  // Usar el primer elemento (datos actuales)
  $: totalOnTime = chartData[0]?.onTime || 0;
  $: totalDelayed = chartData[0]?.delayed || 0;
  $: totalCancelled = chartData[0]?.cancelled || 0;
  $: onTimePercentage = totalWeeklyFlights > 0 ? ((totalOnTime / totalWeeklyFlights) * 100).toFixed(1) : 0;
  $: delayedPercentage = totalWeeklyFlights > 0 ? ((totalDelayed / totalWeeklyFlights) * 100).toFixed(1) : 0;
  $: cancelledPercentage = totalWeeklyFlights > 0 ? ((totalCancelled / totalWeeklyFlights) * 100).toFixed(1) : 0;

  // Actualizar filteredFlights de manera reactiva (usar dbFlights exclusivamente)
  $: filteredFlights = (dbFlights.length > 0 ? dbFlights : []).filter(flight => {
    const flightId = flight.callsign || '';
    const flightAirline = flight.origin_country || '';
    const flightRoute = flight.origin_country || '';
    const matchesSearch = flightId.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         flightAirline.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         flightRoute.toLowerCase().includes(searchTerm.toLowerCase());
    const flightStatus = flight.on_ground ? 'Despegando' : 'En vuelo';
    const matchesStatus = statusFilter === 'all' || flightStatus === statusFilter;
    return matchesSearch && matchesStatus;
  }).sort((a, b) => {
    if (sortBy === 'id') return (a.callsign || '').localeCompare(b.callsign || '');
    // Agrega más lógica si necesitas
    return 0;
  });

  // Agregar definiciones de variables reactivas para métricas
  $: averageVelocity = totalFlights > 0 ? (realFlights.reduce((sum, f) => sum + ((f.velocity || 0) * 3.6), 0) / totalFlights).toFixed(0) : 0;  // Convertir m/s a km/h

  // Agregar definiciones de variables reactivas para métricas adicionales
  $: ascendingFlights = realFlights.filter(f => f.vertical_rate > 0).length;
  $: descendingFlights = realFlights.filter(f => f.vertical_rate < 0).length;
  $: highSpeedFlights = realFlights.filter(f => f.velocity > 500).length;
  $: lowAltitudeFlights = realFlights.filter(f => f.geo_altitude < 10000).length;

  // Utilidades
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

  // Consolidated onMount: initial fetch, periodic fetch, and simulated updates
  onMount(() => {
    let updateInterval;
    let simulationInterval;
    let timeInterval;

    (async () => {
      await fetchFlightsFromDB();  // Cargar vuelos de DB
      await fetchStatsFromDB();    // Cargar estadísticas de DB
      await fetchAndSaveCurrentFlights();  // Actualizar DB con datos actuales
      chartData = [{ day: 'Actual', flights: totalFlights, onTime: onTimeCount, delayed: delayedCount, cancelled: cancelledCount }];
    })();

    // Actualizar cada 5 minutos: recargar de DB y guardar nuevos datos
    updateInterval = setInterval(async () => {
      try {
        await fetchFlightsFromDB();
        await fetchStatsFromDB();
        await fetchAndSaveCurrentFlights();
        chartData = [{ day: 'Actual', flights: totalFlights, onTime: onTimeCount, delayed: delayedCount, cancelled: cancelledCount }];
      } catch (error) {
        console.error('Error actualizando datos:', error);
      }
    }, 5 * 60 * 1000);  // 5 minutos

    // Mantén la simulación para UI demo (opcional, puedes removerla si no la necesitas)
    simulationInterval = setInterval(() => {
      if (Math.random() > 0.7) {
        // Simulación de cambios en UI, pero sin datos simulados
        // Por ejemplo, refrescar reactivity si es necesario
        dbFlights = [...dbFlights];  // Trigger reactivity
      }
    }, 5000);

    // Actualizar reloj UI
    timeInterval = setInterval(() => {
      currentTime = new Date();
    }, 1000);

    return () => {
      clearInterval(updateInterval);
      clearInterval(simulationInterval);
      clearInterval(timeInterval);
    };
  });

  // Helpers para el pie (mover/usar desde <script>)
  function polarToCartesian(cx, cy, r, angleDeg) {
    const angleRad = (angleDeg - 90) * Math.PI / 180;
    return {
      x: +(cx + r * Math.cos(angleRad)).toFixed(3),
      y: +(cy + r * Math.sin(angleRad)).toFixed(3)
    };
  }

  function describeArc(cx, cy, r, startAngle, endAngle) {
    // Normalizar y evitar path inválido cuando start == end
    let startA = startAngle % 360; if (startA < 0) startA += 360;
    let endA = endAngle % 360; if (endA < 0) endA += 360;
    // si el ángulo es 0, crear un pequeño delta para que SVG lo dibuje
    if (Math.abs(endAngle - startAngle) < 1e-6) endAngle = startAngle + 0.0001;
    const startPt = polarToCartesian(cx, cy, r, startAngle);
    const endPt = polarToCartesian(cx, cy, r, endAngle);
    let delta = (endAngle - startAngle);
    if (delta < 0) delta += 360;
    const largeArcFlag = delta > 180 ? 1 : 0;
    const sweepFlag = 1; // dibujar en sentido horario
    return `M ${cx} ${cy} L ${startPt.x} ${startPt.y} A ${r} ${r} 0 ${largeArcFlag} ${sweepFlag} ${endPt.x} ${endPt.y} Z`;
  }

  // Calcular los slices del pie de forma reactiva en el script (más fiable)
  $: pieData = (function() {
    const d = chartData[0] || { flights: 0, onTime: 0, delayed: 0, cancelled: 0 };
    const total = d.flights || 0;
    const base = [
      { key: 'onTime', label: 'A Tiempo', value: d.onTime || 0, color: '#22c55e' },
      { key: 'delayed', label: 'Retrasados', value: d.delayed || 0, color: '#f59e0b' },
      { key: 'cancelled', label: 'Cancelados', value: d.cancelled || 0, color: '#ef4444' }
    ];
    let start = 0;
    return base.map(s => {
      const angle = total > 0 ? (s.value / total) * 360 : 0;
      const slice = { ...s, startAngle: start, endAngle: start + angle };
      start += angle;
      return slice;
    }).filter(s => s.value > 0);
  })();

  // (opcional) depuración en consola para verificar valores reales
  $: console.debug && console.debug('pieData', pieData, 'chartData[0]', chartData[0]);
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
          <span class="nav-icon"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon icon-tabler icons-tabler-outline icon-tabler-plane-tilt"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M14.5 6.5l3 -2.9a2.05 2.05 0 0 1 2.9 2.9l-2.9 3l2.5 7.5l-2.5 2.55l-3.5 -6.55l-3 3v3l-2 2l-1.5 -4.5l-4.5 -1.5l2 -2h3l3 -3l-6.5 -3.5l2.5 -2.5l7.5 2.5z" /></svg>
          <span class="nav-label">Vuelos Activos</span>
        </button>
        <button class="nav-item" class:active={activeSection === 'traffic'} on:click={() => showSection('traffic')}>
          <span class="nav-icon"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon icon-tabler icons-tabler-outline icon-tabler-plane-departure"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M14.639 10.258l4.83 -1.294a2 2 0 1 1 1.035 3.863l-14.489 3.883l-4.45 -5.02l2.897 -.776l2.45 1.414l2.897 -.776l-3.743 -6.244l2.898 -.777l5.675 5.727z" /><path d="M3 21h18" /></svg>
          <span class="nav-label">Tráfico Aéreo</span>
        </button>
        <button class="nav-item" class:active={activeSection === 'stats'} on:click={() => showSection('stats')}>
          <span class="nav-icon"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon icon-tabler icons-tabler-outline icon-tabler-chart-bar-popular"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M3 13a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v6a1 1 0 0 1 -1 1h-4a1 1 0 0 1 -1 -1z" /><path d="M9 9a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v10a1 1 0 0 1 -1 1h-4a1 1 0 0 1 -1 -1z" /><path d="M15 5a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v14a1 1 0 0 1 -1 1h-4a1 1 0 0 1 -1 -1z" /><path d="M4 20h14" /></svg>
          <span class="nav-label">Estadísticas</span>
        </button>
        <button class="nav-item" class:active={activeSection === 'system'} on:click={() => showSection('system')}>
          <span class="nav-icon"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon icon-tabler icons-tabler-outline icon-tabler-settings"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M10.325 4.317c.426 -1.756 2.924 -1.756 3.35 0a1.724 1.724 0 0 0 2.573 1.066c1.543 -.94 3.31 .826 2.37 2.37a1.724 1.724 0 0 0 1.065 2.572c1.756 .426 1.756 2.924 0 3.35a1.724 1.724 0 0 0 -1.066 2.573c.94 1.543 -.826 3.31 -2.37 2.37a1.724 1.724 0 0 0 -2.572 1.065c-.426 1.756 -2.924 1.756 -3.35 0a1.724 1.724 0 0 0 -2.573 -1.066c-1.543 .94 -3.31 -.826 -2.37 -2.37a1.724 1.724 0 0 0 -1.065 -2.572c-1.756 -.426 -1.756 -2.924 0 -3.35a1.724 1.724 0 0 0 1.066 -2.573c-.94 -1.543 .826 -3.31 2.37 -2.37c1 .608 2.296 .07 2.572 -1.065z" /><path d="M9 12a3 3 0 1 0 6 0a3 3 0 0 0 -6 0" /></svg>
          <span class="nav-label">Estado Sistema</span>
        </button>
        <button class="nav-item" class:active={activeSection === 'map'} on:click={() => showSection('map')}>
          <span class="nav-icon"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon icon-tabler icons-tabler-outline icon-tabler-photo-pin"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M15 8h.01" /><path d="M12.5 21h-6.5a3 3 0 0 1 -3 -3v-12a3 3 0 0 1 3 -3h12a3 3 0 0 1 3 3v5.5" /><path d="M3 16l5 -5c.928 -.893 2.072 -.893 3 0l2.5 2.5" /><path d="M21.121 20.121a3 3 0 1 0 -4.242 0c.418 .419 1.125 1.045 2.121 1.879c1.051 -.89 1.759 -1.516 2.121 -1.879z" /><path d="M19 18v.01" /></svg>
          <span class="nav-label">Mapa Global</span>
        </button>
      </nav>
      <div class="sidebar-footer">
        <div class="quick-stats">
          <div class="stat-item">
            <span class="stat-value">{dbFlights.length}</span>
            <span class="stat-label">Vuelos</span>
          </div>
          <div class="stat-item">
            <span class="stat-value">0</span>  <!-- Sin datos de alertas en DB, usar 0 -->
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
                  <h3 class="flight-id">{flight.callsign || 'N/A'}</h3>
                  <div class="status-badge" style="background-color: {getStatusColor(flight.on_ground ? 'Despegando' : 'En vuelo')}">
                    {flight.on_ground ? 'Despegando' : 'En vuelo'}
                  </div>
                </div>
                <div class="flight-info">
                  <div class="airline">{flight.origin_country || 'N/A'}</div>
                  <div class="route">{flight.origin_country || 'N/A'}</div>
                </div>
                <div class="flight-metrics">
                  <div class="metric">
                    <span class="metric-label">Altitud</span>
                    <span class="metric-value">{flight.geo_altitude ? (flight.geo_altitude / 3.28084).toFixed(0) + ' ft' : 'N/A'}</span>
                  </div>
                  <div class="metric">
                    <span class="metric-label">Velocidad</span>
                    <span class="metric-value">{flight.velocity ? (flight.velocity * 3.6).toFixed(0) + ' km/h' : 'N/A'}</span>
                  </div>
                  <div class="metric">
                    <span class="metric-label">ETA</span>
                    <span class="metric-value">N/A</span>
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
              <div class="stat-content">
                <div class="stat-value">{totalFlights}</div>
                <div class="stat-label">Vuelos Totales</div>
              </div>
            </div>
            <div class="stat-card">
              <div class="stat-content">
                <div class="stat-value">{Math.floor(totalFlights / 2)}</div>
                <div class="stat-label">Salidas</div>
              </div>
            </div>
            <div class="stat-card">
              <div class="stat-content">
                <div class="stat-value">{Math.floor(totalFlights / 2)}</div>
                <div class="stat-label">Llegadas</div>
              </div>
            </div>
            <div class="stat-card warning">
              <div class="stat-content">
                <div class="stat-value">{delayedCount}</div>
                <div class="stat-label">Retrasos</div>
              </div>
            </div>
          </div>
          
          <div class="airports-grid">
            {#each airportsData as airport}
              <!-- Usa datos calculados de DB -->
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
            <h2 class="section-title">Estadísticas de Vuelo (Tiempo Real)</h2>
          </div>
          <div class="overview-stats">
            <div class="stat-card primary">
              <div class="stat-header">
                <span class="stat-icon"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon icon-tabler icons-tabler-outline icon-tabler-plane-tilt"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M14.5 6.5l3 -2.9a2.05 2.05 0 0 1 2.9 2.9l-2.9 3l2.5 7.5l-2.5 2.55l-3.5 -6.55l-3 3v3l-2 2l-1.5 -4.5l-4.5 -1.5l2 -2h3l3 -3l-6.5 -3.5l2.5 -2.5l7.5 2.5z" /></svg></span>
                <span class="stat-title">Total de Vuelos Activos</span>
              </div>
              <div class="stat-value">{totalWeeklyFlights}</div>
              <div class="stat-change positive">Datos en tiempo real</div>
            </div>
            <div class="stat-card success">
              <div class="stat-header">
                <span class="stat-icon"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon icon-tabler icons-tabler-outline icon-tabler-check"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M5 12l5 5l10 -10" /></svg></span>
                <span class="stat-title">A Tiempo</span>
              </div>
              <div class="stat-value">{totalOnTime}</div>
              <div class="stat-percentage">{onTimePercentage}%</div>
            </div>
            <div class="stat-card warning">
              <div class="stat-header">
                <span class="stat-icon"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon icon-tabler icons-tabler-outline icon-tabler-clock"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M3 12a9 9 0 1 0 18 0a9 9 0 0 0 -18 0" /><path d="M12 7v5l3 3" /></svg></span>
                <span class="stat-title">Retrasados</span>
              </div>
              <div class="stat-value">{totalDelayed}</div>
              <div class="stat-percentage">{delayedPercentage}%</div>
            </div>
            <div class="stat-card danger">
              <div class="stat-header">
                <span class="stat-icon"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon icon-tabler icons-tabler-outline icon-tabler-x"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M18 6l-12 12" /><path d="M6 6l12 12" /></svg></span>
                <span class="stat-title">Cancelados</span>
              </div>
              <div class="stat-value">{totalCancelled}</div>
              <div class="stat-percentage">{cancelledPercentage}%</div>
            </div>
          </div>
          
          <div class="charts-section">
            <div class="chart-container">
              <h3 class="chart-title">Estado Actual</h3>
              <div class="pie-chart">
                {#if pieData && pieData.length}
                  <svg viewBox="0 0 200 200" class="pie-svg" aria-label="Estado actual de vuelos">
                    <circle cx="100" cy="100" r="80" fill="#0b254a" opacity="0.05" />
                    {#each pieData as slice}
                      <path d={describeArc(100, 100, 80, slice.startAngle, slice.endAngle)} fill={slice.color} />
                    {/each}
                    <circle cx="100" cy="100" r="36" fill="#0b254a" />
                    <text x="100" y="105" text-anchor="middle" fill="#ffffff" font-size="12">{chartData[0]?.flights || 0}</text>
                    <text x="100" y="122" text-anchor="middle" fill="#9ca3af" font-size="10">vuelos</text>
                  </svg>

                  <div class="pie-legend">
                    {#each pieData as s}
                      <div class="legend-item">
                        <div class="legend-color" style="background-color: {s.color}"></div>
                        <span style="color: {s.color}">{s.label}: {s.value} ({(chartData[0]?.flights > 0 ? (s.value / chartData[0].flights * 100).toFixed(1) : 0)}%)</span>
                      </div>
                    {/each}
                  </div>
                {/if}
              </div>
            </div>

            <div class="performance-metrics">
              <h3 class="chart-title">Métricas de Rendimiento</h3>
              <div class="metrics-grid">
                <div class="metric-item">
                  <div class="metric-card">
                    <div class="metric-header">
                      <span class="metric-label">Velocidad Promedio</span>
                      <span class="metric-value">{averageVelocity} km/h</span>
                    </div>
                    <div class="gauge-chart">
                      <svg viewBox="0 0 100 60" class="gauge-svg">
                        <path d="M10,50 A40,40 0 0,1 90,50" fill="none" stroke="#e5e7eb" stroke-width="8"/>
                        <path d="M10,50 A40,40 0 0,1 {10 + 80 * (averageVelocity / 1000)} ,{50 - 40 * Math.sin(Math.PI * (averageVelocity / 1000))}" fill="none" stroke="#22c55e" stroke-width="8"/>
                      </svg>
                    </div>
                  </div>
                </div>
                <div class="metric-item">
                  <div class="metric-card">
                    <div class="metric-header">
                      <span class="metric-label">Vuelos en Ascenso</span>
                      <span class="metric-value">{ascendingFlights}</span>
                    </div>
                    <div class="bar-chart-small">
                      <div class="bar-fill" style="width: {totalFlights > 0 ? (ascendingFlights / totalFlights) * 100 : 0}%; background-color: #3b82f6"></div>
                    </div>
                  </div>
                </div>
                <div class="metric-item">
                  <div class="metric-card">
                    <div class="metric-header">
                      <span class="metric-label">Vuelos en Descenso</span>
                      <span class="metric-value">{descendingFlights}</span>
                    </div>
                    <div class="bar-chart-small">
                      <div class="bar-fill" style="width: {totalFlights > 0 ? (descendingFlights / totalFlights) * 100 : 0}%; background-color: #8b5cf6"></div>
                    </div>
                  </div>
                </div>
                <div class="metric-item">
                  <div class="metric-card">
                    <div class="metric-header">
                      <span class="metric-label">Vuelos a Alta Velocidad</span>
                      <span class="metric-value">{highSpeedFlights}</span>
                    </div>
                    <div class="bar-chart-small">
                      <div class="bar-fill" style="width: {totalFlights > 0 ? (highSpeedFlights / totalFlights) * 100 : 0}%; background-color: #10b981"></div>
                    </div>
                  </div>
                </div>
                <div class="metric-item">
                  <div class="metric-card">
                    <div class="metric-header">
                      <span class="metric-label">Vuelos a Baja Altitud</span>
                      <span class="metric-value">{lowAltitudeFlights}</span>
                    </div>
                    <div class="bar-chart-small">
                      <div class="bar-fill" style="width: {totalFlights > 0 ? (lowAltitudeFlights / totalFlights) * 100 : 0}%; background-color: #f59e0b"></div>
                    </div>
                  </div>
                </div>
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
                <div class="card-value">0</div>  <!-- Sin datos de alertas en DB -->
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
                <!-- Sin datos de servicios en DB, dejar vacío o usar simulados si es necesario -->
                <p>No hay datos de servicios disponibles en la base de datos.</p>
              </div>
            </div>
            
            <div class="alerts-section">
              <h3 class="subsection-title">Alertas del Sistema</h3>
              <div class="alerts-list">
                <!-- Sin datos de alertas en DB -->
                <p>No hay alertas disponibles en la base de datos.</p>
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
