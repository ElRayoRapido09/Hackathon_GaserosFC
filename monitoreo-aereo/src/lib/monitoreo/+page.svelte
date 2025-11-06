<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema de Monitoreo Aéreo</title>
    <link rel="stylesheet" href="styles.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
</head>
<body>
    <script>
        let period = 'daily';
        function setPeriod(p) {
            period = p;
        }
    </script>
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
                <div class="time" id="currentTime">00:00:00</div>
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
                
                <button class="nav-item active" onclick="showSection('flights')" data-section="flights">
                    <span class="nav-icon">✈️</span>
                    <span class="nav-label">Vuelos Activos</span>
                </button>
                <button class="nav-item" onclick="showSection('traffic')" data-section="traffic">
                    <span class="nav-icon">🛫</span>
                    <span class="nav-label">Tráfico Aéreo</span>
                </button>
                <button class="nav-item" onclick="showSection('stats')" data-section="stats">
                    <span class="nav-icon">📊</span>
                    <span class="nav-label">Estadísticas</span>
                </button>
                <button class="nav-item" onclick="showSection('system')" data-section="system">
                    <span class="nav-icon">⚙️</span>
                    <span class="nav-label">Estado Sistema</span>
                </button>
                <button class="nav-item" onclick="showSection('map')" data-section="map">
                    <span class="nav-icon">🗺️</span>
                    <span class="nav-label">Mapa Global</span>
                </button>
            </nav>
            <div class="sidebar-footer">
                <div class="quick-stats">
                    <div class="stat-item">
                        <span class="stat-value">24</span>
                        <span class="stat-label">Vuelos</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-value">12</span>
                        <span class="stat-label">Alertas</span>
                    </div>
                </div>
            </div>
        </aside>

        <!-- Main Content -->
        <main class="content">
            <!-- Vuelos Activos Section -->
            <div id="flights-section" class="section active">
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
                        <input type="text" placeholder="Buscar vuelos..." class="search-input" id="flightSearch">
                    </div>
                    <select class="filter-select" id="statusFilter">
                        <option value="all">Todos los estados</option>
                        <option value="En vuelo">En vuelo</option>
                        <option value="Despegando">Despegando</option>
                        <option value="Aproximación">Aproximación</option>
                    </select>
                    <select class="filter-select" id="sortBy">
                        <option value="id">Ordenar por ID</option>
                        <option value="status">Ordenar por Estado</option>
                        <option value="altitude">Ordenar por Altitud</option>
                    </select>
                </div>
                
                <div class="flights-grid" id="flightsGrid">
                    <!-- Flight cards with sample data -->
                    <div class="flight-card">
                        <div class="flight-header">
                            <div class="flight-number">AA123</div>
                            <div class="flight-status en-vuelo">EN VUELO</div>
                        </div>
                        <div class="airline">American Airlines</div>
                        <div class="route">NYC → LAX</div>
                        <div class="flight-details">
                            <div class="detail">
                                <span class="label">ALTITUD</span>
                                <span class="value">25,000 ft</span>
                            </div>
                            <div class="detail">
                                <span class="label">VELOCIDAD</span>
                                <span class="value">520 mph</span>
                            </div>
                            <div class="detail">
                                <span class="label">ETA</span>
                                <span class="value">14:30</span>
                            </div>
                        </div>
                    </div>

                    <div class="flight-card">
                        <div class="flight-header">
                            <div class="flight-number">AF303</div>
                            <div class="flight-status en-vuelo">EN VUELO</div>
                        </div>
                        <div class="airline">Air France</div>
                        <div class="route">CDG → LAX</div>
                        <div class="flight-details">
                            <div class="detail">
                                <span class="label">ALTITUD</span>
                                <span class="value">25,000 ft</span>
                            </div>
                            <div class="detail">
                                <span class="label">VELOCIDAD</span>
                                <span class="value">560 mph</span>
                            </div>
                            <div class="detail">
                                <span class="label">ETA</span>
                                <span class="value">19:30</span>
                            </div>
                        </div>
                    </div>

                    <div class="flight-card">
                        <div class="flight-header">
                            <div class="flight-number">BA202</div>
                            <div class="flight-status en-vuelo">EN VUELO</div>
                        </div>
                        <div class="airline">British Airways</div>
                        <div class="route">LHR → JFK</div>
                        <div class="flight-details">
                            <div class="detail">
                                <span class="label">ALTITUD</span>
                                <span class="value">25,000 ft</span>
                            </div>
                            <div class="detail">
                                <span class="label">VELOCIDAD</span>
                                <span class="value">580 mph</span>
                            </div>
                            <div class="detail">
                                <span class="label">ETA</span>
                                <span class="value">18:00</span>
                            </div>
                        </div>
                    </div>

                    <div class="flight-card">
                        <div class="flight-header">
                            <div class="flight-number">DL789</div>
                            <div class="flight-status aproximacion">APROXIMACIÓN</div>
                        </div>
                        <div class="airline">Delta Airlines</div>
                        <div class="route">MIA → ATL</div>
                        <div class="flight-details">
                            <div class="detail">
                                <span class="label">ALTITUD</span>
                                <span class="value">35,000 ft</span>
                            </div>
                            <div class="detail">
                                <span class="label">VELOCIDAD</span>
                                <span class="value">250 mph</span>
                            </div>
                            <div class="detail">
                                <span class="label">ETA</span>
                                <span class="value">13:15</span>
                            </div>
                        </div>
                    </div>

                    <div class="flight-card">
                        <div class="flight-header">
                            <div class="flight-number">KL505</div>
                            <div class="flight-status en-vuelo">EN VUELO</div>
                        </div>
                        <div class="airline">KLM</div>
                        <div class="route">AMS → SFO</div>
                        <div class="flight-details">
                            <div class="detail">
                                <span class="label">ALTITUD</span>
                                <span class="value">25,000 ft</span>
                            </div>
                            <div class="detail">
                                <span class="label">VELOCIDAD</span>
                                <span class="value">540 mph</span>
                            </div>
                            <div class="detail">
                                <span class="label">ETA</span>
                                <span class="value">20:15</span>
                            </div>
                        </div>
                    </div>

                    <div class="flight-card">
                        <div class="flight-header">
                            <div class="flight-number">LH404</div>
                            <div class="flight-status despegando">DESPEGANDO</div>
                        </div>
                        <div class="airline">Lufthansa</div>
                        <div class="route">FRA → JFK</div>
                        <div class="flight-details">
                            <div class="detail">
                                <span class="label">ALTITUD</span>
                                <span class="value">25,000 ft</span>
                            </div>
                            <div class="detail">
                                <span class="label">VELOCIDAD</span>
                                <span class="value">320 mph</span>
                            </div>
                            <div class="detail">
                                <span class="label">ETA</span>
                                <span class="value">17:45</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Tráfico Aéreo Section -->
            <div id="traffic-section" class="section">
                <div class="section-header">
                    <h2 class="section-title">Tráfico Aéreo</h2>
                    <div class="last-update">
                        Última actualización: <span id="lastUpdate">00:00:00</span>
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
                
                <div class="filters-section">
                    <select class="filter-select">
                        <option value="24h">Últimas 24 horas</option>
                        <option value="6h">Últimas 6 horas</option>
                        <option value="1h">Última hora</option>
                    </select>
                    <select class="filter-select">
                        <option value="all">Todos los aeropuertos</option>
                        <option value="JFK">JFK</option>
                        <option value="LAX">LAX</option>
                        <option value="CHI">CHI</option>
                    </select>
                </div>
                
                <div class="airports-grid" id="airportsGrid">
                    <!-- Airport cards will be populated by JavaScript -->
                </div>
                    <div class="period-tabs">
                            <button class="tab" class:active={period === 'daily'} on:click={() => setPeriod('daily')}>Diario</button>
                            <button class="tab" class:active={period === 'weekly'} on:click={() => setPeriod('weekly')}>Semanal</button>
                            <button class="tab" class:active={period === 'monthly'} on:click={() => setPeriod('monthly')}>Mensual</button>
                        </div>
                    <h2 class="section-title">Estadísticas de Vuelo</h2>
                    <div class="period-tabs">
                        <button class="tab active" on:click="setPeriod('daily')">Diario</button>
                        <button class="tab" on:click="setPeriod('weekly')">Semanal</button>
                        <button class="tab" on:click="setPeriod('monthly')">Mensual</button>
                    </div>
                </div>
                
                <div class="overview-stats">
                    <div class="stat-card primary">
                        <div class="stat-header">
                            <span class="stat-icon">✈️</span>
                            <span class="stat-title">Total de Vuelos</span>
                        </div>
                        <div class="stat-value">1,247</div>
                        <div class="stat-change positive">+5.2% vs período anterior</div>
                    </div>
                    <div class="stat-card success">
                        <div class="stat-header">
                            <span class="stat-icon">✅</span>
                            <span class="stat-title">A Tiempo</span>
                        </div>
                        <div class="stat-value">1,098</div>
                        <div class="stat-percentage">88.1%</div>
                    </div>
                    <div class="stat-card warning">
                        <div class="stat-header">
                            <span class="stat-icon">⏰</span>
                            <span class="stat-title">Retrasados</span>
                        </div>
                        <div class="stat-value">127</div>
                        <div class="stat-percentage">10.2%</div>
                    </div>
                    <div class="stat-card danger">
                        <div class="stat-header">
                            <span class="stat-icon">❌</span>
                            <span class="stat-title">Cancelados</span>
                        </div>
                        <div class="stat-value">22</div>
                        <div class="stat-percentage">1.7%</div>
                    </div>
                </div>
                
                <div class="charts-section">
                    <div class="chart-container">
                        <h3 class="chart-title">Tendencia Semanal</h3>
                        <div class="bar-chart" id="weeklyChart">
                            <!-- Chart will be generated by JavaScript -->
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

            <!-- Mapa Global Section -->
            <div id="map-section" class="section">
                <div class="section-header">
                    <h2 class="section-title">Mapa Global de Vuelos en Tiempo Real</h2>
                </div>
                <div class="map-container" style="width:100%;height:80vh;position:relative;">
                    <!-- Puedes usar un iframe de FlightAware o FlightRadar24 para mostrar el mapa real -->
                    <iframe src="https://www.flightaware.com/live/" width="100%" height="100%" style="border:none;"></iframe>
                </div>
            </div>

            <!-- Sistema Section -->
            <div id="system-section" class="section">
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
                            <div class="card-value">1</div>
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
                        <div class="services-list" id="servicesList">
                            <!-- Services will be populated by JavaScript -->
                        </div>
                    </div>
                    
                    <div class="alerts-section">
                        <h3 class="subsection-title">Alertas del Sistema</h3>
                        <div class="alerts-list" id="alertsList">
                            <!-- Alerts will be populated by JavaScript -->
                        </div>
                    </div>
                </div>
            </div>
        </main>
    </div>

    <script src="script.js"></script>
</body>
</html>