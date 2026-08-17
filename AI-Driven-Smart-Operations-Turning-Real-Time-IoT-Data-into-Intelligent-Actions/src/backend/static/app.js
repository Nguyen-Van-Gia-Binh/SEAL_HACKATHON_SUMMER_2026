// Global Application State
let stations = [];
let activeStationId = "STN_HN_01";
let telemetryData = {};
let aggregationsData = {};
let forecastsData = {};
let recentAlerts = [];

let map = null;
let mapMarkers = {};
let streamChart = null;
let chartHistory = {
  labels: [],
  rawTemps: [],
  slidingTemps: [],
  pressures: []
};

// INITIALIZATION ON LOAD
document.addEventListener("DOMContentLoaded", async () => {
  initMap();
  initChart();
  await loadStations();
  initWebSocket();
  // Polling fallback
  setInterval(fetchStateSnapshot, 3000);
});

// 1. LEAFLET MAP INITIALIZATION (Light Theme Map Tiles)
function initMap() {
  // Center on Vietnam / Southeast Asia
  map = L.map('map', {
    zoomControl: true,
    attributionControl: false
  }).setView([16.0, 108.0], 5);

  // Clean Light Map Layer
  L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
    maxZoom: 18,
    subdomains: 'abcd'
  }).addTo(map);
}

// 2. LOAD STATIONS METADATA
async function loadStations() {
  try {
    const res = await fetch("/api/stations");
    stations = await res.json();
    document.getElementById("kpiStationCount").innerText = `${stations.length} Trạm`;

    const btnContainer = document.getElementById("stationButtons");
    btnContainer.innerHTML = "";

    stations.forEach((stn, idx) => {
      // Add button
      const btn = document.createElement("button");
      btn.className = `station-btn ${stn.station_id === activeStationId ? 'active' : ''}`;
      btn.id = `btn_${stn.station_id}`;
      btn.innerText = `${stn.station_id} (${stn.station_name.split(' ')[0]})`;
      btn.onclick = () => selectStation(stn.station_id);
      btnContainer.appendChild(btn);

      // Add Map Marker with Agricultural Green Pin
      const customIcon = L.divIcon({
        className: 'custom-map-pin',
        html: `<div style="background:#15803d; width:14px; height:14px; border-radius:50%; box-shadow:0 2px 6px rgba(21,128,61,0.5); border:2px solid #ffffff;"></div>`,
        iconSize: [16, 16]
      });

      const marker = L.marker([stn.lat, stn.lon], { icon: customIcon }).addTo(map);
      marker.bindPopup(`<div style="font-family:'Inter',sans-serif; font-size:12px;"><b>${stn.station_name}</b><br>Mã trạm: ${stn.station_id}<br>Giao thức: ${stn.ingestion_protocol}<br>Cao độ: ${stn.elevation_m}m</div>`);
      marker.on('click', () => selectStation(stn.station_id));
      mapMarkers[stn.station_id] = marker;

      if (idx === 0 && !activeStationId) {
        activeStationId = stn.station_id;
      }
    });

    if (stations.length > 0) {
      updateActiveStationUI();
    }
  } catch (e) {
    console.error("Failed to load stations:", e);
  }
}

// 3. SELECT STATION
function selectStation(stationId) {
  activeStationId = stationId;
  
  // Update button active state
  document.querySelectorAll(".station-btn").forEach(btn => {
    btn.classList.toggle("active", btn.id === `btn_${stationId}`);
  });

  const stn = stations.find(s => s.station_id === stationId);
  if (stn && map) {
    map.flyTo([stn.lat, stn.lon], 7, { duration: 1.0 });
    if (mapMarkers[stationId]) {
      mapMarkers[stationId].openPopup();
    }
  }

  // Clear chart history on switch
  chartHistory.labels = [];
  chartHistory.rawTemps = [];
  chartHistory.slidingTemps = [];
  chartHistory.pressures = [];

  updateActiveStationUI();
}

// 4. CHART.JS INITIALIZATION (Light Theme with Agricultural Green Accent)
function initChart() {
  const ctx = document.getElementById('streamChart').getContext('2d');
  streamChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: [],
      datasets: [
        {
          label: 'Nhiệt độ quan trắc (°C)',
          data: [],
          borderColor: '#15803d',
          backgroundColor: 'rgba(21, 128, 61, 0.08)',
          tension: 0.3,
          borderWidth: 2.5,
          pointRadius: 3,
          pointBackgroundColor: '#15803d',
          fill: true
        },
        {
          label: 'Cửa sổ trượt 5m TB (°C)',
          data: [],
          borderColor: '#c2410c',
          borderDash: [4, 4],
          tension: 0.2,
          borderWidth: 2,
          pointRadius: 0
        },
        {
          label: 'Khí áp (hPa / 100)',
          data: [],
          borderColor: '#0369a1',
          tension: 0.3,
          borderWidth: 1.8,
          pointRadius: 1,
          yAxisID: 'y1'
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: { duration: 400 },
      plugins: {
        legend: {
          labels: { color: '#334155', font: { size: 11, weight: '600', family: 'Inter' } }
        }
      },
      scales: {
        x: {
          grid: { color: '#e2e8f0' },
          ticks: { color: '#64748b', font: { size: 10, family: 'Inter' }, maxTicksLimit: 8 }
        },
        y: {
          grid: { color: '#e2e8f0' },
          ticks: { color: '#334155', font: { size: 10, family: 'Inter' } }
        },
        y1: {
          position: 'right',
          grid: { drawOnChartArea: false },
          ticks: { color: '#0369a1', font: { size: 10, family: 'Inter' } }
        }
      }
    }
  });
}

// 5. WEBSOCKET REAL-TIME CONNECTION
function initWebSocket() {
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  const wsUrl = `${protocol}//${window.location.host}/ws/telemetry`;
  const ws = new WebSocket(wsUrl);

  ws.onopen = () => {
    document.getElementById("wsStatusDot").className = "status-dot online";
    document.getElementById("wsStatusText").innerText = "TRỰC TUYẾN";
  };

  ws.onmessage = (event) => {
    try {
      const msg = JSON.parse(event.data);
      if (msg.type === "STATE_UPDATE") {
        telemetryData = msg.telemetry || {};
        aggregationsData = msg.aggregations || {};
        forecastsData = msg.forecasts || {};
        recentAlerts = msg.alerts || [];
        updateActiveStationUI();
      }
    } catch (e) {
      console.error("WS Parse error:", e);
    }
  };

  ws.onclose = () => {
    document.getElementById("wsStatusDot").className = "status-dot";
    document.getElementById("wsStatusText").innerText = "KẾT NỐI LẠI...";
    setTimeout(initWebSocket, 2000);
  };

  ws.onerror = () => {
    ws.close();
  };
}

// 6. FALLBACK REST POLLING
async function fetchStateSnapshot() {
  try {
    const res = await fetch("/api/state");
    const state = await res.json();
    telemetryData = state.telemetry || telemetryData;
    aggregationsData = state.aggregations || aggregationsData;
    forecastsData = state.forecasts || forecastsData;
    recentAlerts = state.alerts || recentAlerts;
    updateActiveStationUI();
  } catch (e) {
    // Silent fallback
  }
}

// 7. UPDATE DASHBOARD UI FOR ACTIVE STATION
function updateActiveStationUI() {
  const stn = stations.find(s => s.station_id === activeStationId);
  if (!stn) return;

  const curTelem = telemetryData[activeStationId] || {};
  const curAgg = aggregationsData[activeStationId] || {};
  const curForecast = forecastsData[activeStationId] || {};

  // Station Header
  document.getElementById("curStationName").innerText = `${stn.station_name} (${stn.station_id})`;
  document.getElementById("curStationMeta").innerText = `Giao thức: ${curTelem.protocol || stn.ingestion_protocol} • Cao độ: ${stn.elevation_m}m • Tọa độ: ${stn.lat.toFixed(2)}, ${stn.lon.toFixed(2)}`;

  // Gauges
  const temp = curTelem.temp !== undefined ? curTelem.temp : 28.0;
  const humidity = curTelem.humidity !== undefined ? curTelem.humidity : 70.0;
  const pressure = curTelem.pressure !== undefined ? curTelem.pressure : 1012.0;
  const wind = curTelem.wind_speed !== undefined ? curTelem.wind_speed : 3.2;
  const windDir = curTelem.wind_direction || "E";
  const rain = curTelem.rainfall_mm_h !== undefined ? curTelem.rainfall_mm_h : 0.0;
  const pm25 = curTelem.pm25 !== undefined ? curTelem.pm25 : 25.0;
  const uv = curTelem.uv_index !== undefined ? curTelem.uv_index : 5.0;

  document.getElementById("gTemp").innerText = `${temp.toFixed(1)} °C`;
  document.getElementById("gHumidity").innerText = `${humidity.toFixed(0)} %`;
  document.getElementById("gPressure").innerText = `${pressure.toFixed(1)} hPa`;
  document.getElementById("gWind").innerText = `${wind.toFixed(1)} m/s`;
  document.getElementById("gWindDir").innerText = `Hướng: ${windDir}`;
  document.getElementById("gRain").innerText = `${rain.toFixed(1)} mm/h`;
  document.getElementById("gPM25").innerText = `${pm25.toFixed(0)} µg/m³`;
  document.getElementById("gUV").innerText = `UV: ${uv.toFixed(1)}`;

  // Sub calculations
  const heatIndex = curAgg.metrics ? curAgg.metrics.heat_index_c : (temp + (humidity > 70 ? 2 : 0)).toFixed(1);
  const dewPoint = curAgg.metrics ? curAgg.metrics.dew_point_c : (temp - ((100 - humidity) / 5)).toFixed(1);
  const pTrend = curAgg.metrics ? curAgg.metrics.pressure_trend_hpa : 0.0;

  document.getElementById("gHeatIndex").innerText = `Heat Index: ${heatIndex} °C`;
  document.getElementById("gDewPoint").innerText = `Điểm sương: ${dewPoint} °C`;
  document.getElementById("gPressureTrend").innerText = `Biến thiên: ${pTrend > 0 ? '+' : ''}${pTrend} hPa`;

  // Update Chart
  const timeLabel = new Date().toLocaleTimeString('vi-VN', { hour12: false });
  chartHistory.labels.push(timeLabel);
  chartHistory.rawTemps.push(temp);
  chartHistory.slidingTemps.push(curAgg.metrics ? curAgg.metrics.temp_avg : temp);
  chartHistory.pressures.push((pressure / 100.0).toFixed(2));

  if (chartHistory.labels.length > 20) {
    chartHistory.labels.shift();
    chartHistory.rawTemps.shift();
    chartHistory.slidingTemps.shift();
    chartHistory.pressures.shift();
  }

  if (streamChart) {
    streamChart.data.labels = chartHistory.labels;
    streamChart.data.datasets[0].data = chartHistory.rawTemps;
    streamChart.data.datasets[1].data = chartHistory.slidingTemps;
    streamChart.data.datasets[2].data = chartHistory.pressures;
    streamChart.update('none');
  }

  // Update AI Forecast Card
  if (curForecast.weather_condition) {
    document.getElementById("aiCondition").innerText = curForecast.weather_condition;
    document.getElementById("aiSynopticText").innerText = curForecast.synoptic_analysis || "";
    
    if (curForecast.forecast_horizons) {
      document.getElementById("aiHorizon6h").innerText = curForecast.forecast_horizons["6_hours"] || "";
      document.getElementById("aiHorizon24h").innerText = curForecast.forecast_horizons["24_hours"] || "";
    }

    const riskScore = curForecast.risk_score !== undefined ? curForecast.risk_score : 15;
    const riskLevel = curForecast.risk_level || "LOW";
    
    document.getElementById("kpiRiskScore").innerText = `${riskScore} / 100`;
    document.getElementById("kpiRiskLevel").innerText = `Mức độ: ${riskLevel}`;

    const riskBadge = document.getElementById("aiRiskBadge");
    riskBadge.innerText = `RỦI RO: ${riskScore}/100 (${riskLevel})`;
    riskBadge.className = `risk-pill-badge risk-${riskLevel}`;

    document.getElementById("aiProviderBadge").innerHTML = `<i class="fa-solid fa-microchip"></i> ${curForecast.source || 'AI Engine'}`;

    // Update Decision Feed
    renderDecisions(curForecast.smart_operational_decisions || []);
  }
}

// 8. RENDER DECISION FEED (Refined Terminology for Agriculture and Natural Disaster Prevention)
function renderDecisions(decisions) {
  const container = document.getElementById("decisionsList");
  if (!decisions || decisions.length === 0) {
    container.innerHTML = `
      <div class="decision-card severity-INFO">
        <div class="decision-header">
          <span class="decision-sector"><i class="fa-solid fa-seedling"></i> ĐIỀU HÀNH NÔNG NGHIỆP & PHÒNG CHỐNG THIÊN TAI</span>
          <span class="badge badge-stream">TRẠNG THÁI ỔN ĐỊNH</span>
        </div>
        <div class="decision-action">Điều kiện khí tượng nông nghiệp nằm trong ngưỡng an toàn</div>
        <div class="decision-details">Các vùng chuyên canh và hệ thống công trình thủy nông duy trì chế độ vận hành thường quy.</div>
      </div>
    `;
    return;
  }

  container.innerHTML = decisions.map(d => `
    <div class="decision-card severity-${d.severity || 'INFO'}">
      <div class="decision-header">
        <span class="decision-sector"><i class="fa-solid fa-building-flag"></i> ${d.sector}</span>
        <span class="badge ${d.severity === 'CRITICAL' ? 'risk-pill-badge risk-CRITICAL' : 'badge-stream'}">${d.severity}</span>
      </div>
      <div class="decision-action">${d.action}</div>
      <div class="decision-details">${d.details}</div>
      ${d.automated_command ? `<div class="decision-cmd"><i class="fa-solid fa-terminal"></i> ${d.automated_command}</div>` : ''}
    </div>
  `).join('');
}

// 9. SCENARIO CHANGER
async function changeScenario(scenario) {
  try {
    const res = await fetch("/api/simulator/scenario", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ scenario })
    });
    const data = await res.json();
    console.log("Scenario changed:", data);
  } catch (e) {
    console.error("Failed to set scenario:", e);
  }
}

// 10. TRIGGER INSTANT AI ANALYSIS
async function triggerAiAnalyze() {
  try {
    const btn = document.querySelector(".btn-ai-action");
    btn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Đang phân tích...`;
    const res = await fetch(`/api/ai/analyze/${activeStationId}`, { method: "POST" });
    const result = await res.json();
    forecastsData[activeStationId] = result;
    updateActiveStationUI();
    btn.innerHTML = `<i class="fa-solid fa-wand-magic-sparkles"></i> Phân tích AI ngay`;
  } catch (e) {
    console.error("AI Analysis failed:", e);
  }
}
