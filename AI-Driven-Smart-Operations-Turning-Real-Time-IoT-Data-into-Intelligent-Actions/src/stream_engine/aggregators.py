import math
from typing import List, Dict, Any

def compute_heat_index(temp_c: float, relative_humidity: float) -> float:
    """
    Computes NOAA Heat Index (apparent temperature) in Celsius.
    """
    # Convert Celsius to Fahrenheit
    T = (temp_c * 9.0 / 5.0) + 32.0
    RH = relative_humidity

    # Simple formula first
    HI_simple = 0.5 * (T + 61.0 + ((T - 68.0) * 1.2) + (RH * 0.094))
    if HI_simple < 80.0:
        hi_f = HI_simple
    else:
        # Full Rothfusz regression equation
        hi_f = (-42.379 + 2.04901523 * T + 10.14333127 * RH
                - 0.22475541 * T * RH - 0.00683783 * T * T
                - 0.05481717 * RH * RH + 0.00122874 * T * T * RH
                + 0.00085282 * T * RH * RH - 0.00000199 * T * T * RH * RH)

        if RH < 13.0 and 80.0 <= T <= 112.0:
            adjustment = ((13.0 - RH) / 4.0) * math.sqrt((17.0 - abs(T - 95.0)) / 17.0)
            hi_f -= adjustment
        elif RH > 85.0 and 80.0 <= T <= 87.0:
            adjustment = ((RH - 85.0) / 10.0) * ((87.0 - T) / 5.0)
            hi_f += adjustment

    # Convert back to Celsius
    hi_c = (hi_f - 32.0) * 5.0 / 9.0
    return round(hi_c, 2)

def compute_dew_point(temp_c: float, relative_humidity: float) -> float:
    """
    Calculates Dew Point in Celsius using Magnus-Tetens formula.
    """
    a = 17.27
    b = 237.7
    alpha = ((a * temp_c) / (b + temp_c)) + math.log(max(0.01, relative_humidity) / 100.0)
    dp = (b * alpha) / (a - alpha)
    return round(dp, 2)

def aggregate_window_records(records: List[Dict[str, Any]], window_type: str, window_start: float, window_end: float) -> Dict[str, Any]:
    """
    Aggregates numerical weather metrics over a stream window.
    """
    if not records:
        return {}

    station_id = records[0].get("station_id", "UNKNOWN")
    station_name = records[0].get("station_name", station_id)
    region = records[0].get("region", "")
    lat = records[0].get("lat", 0.0)
    lon = records[0].get("lon", 0.0)

    temps = [r["temp"] for r in records if "temp" in r]
    humidities = [r["humidity"] for r in records if "humidity" in r]
    pressures = [r["pressure"] for r in records if "pressure" in r]
    winds = [r["wind_speed"] for r in records if "wind_speed" in r]
    rains = [r["rainfall_mm_h"] for r in records if "rainfall_mm_h" in r]
    pm25s = [r["pm25"] for r in records if "pm25" in r]
    uvs = [r["uv_index"] for r in records if "uv_index" in r]

    avg_temp = sum(temps) / len(temps) if temps else 0.0
    avg_humidity = sum(humidities) / len(humidities) if humidities else 0.0
    avg_pressure = sum(pressures) / len(pressures) if pressures else 1013.25
    avg_wind = sum(winds) / len(winds) if winds else 0.0
    max_wind = max(winds) if winds else 0.0
    total_rain = sum(rains) / len(rains) if rains else 0.0  # rate
    avg_pm25 = sum(pm25s) / len(pm25s) if pm25s else 0.0
    max_uv = max(uvs) if uvs else 0.0

    # Pressure tendency (First vs Last)
    pressure_trend = 0.0
    if len(pressures) >= 2:
        pressure_trend = round(pressures[-1] - pressures[0], 2)

    heat_index = compute_heat_index(avg_temp, avg_humidity)
    dew_point = compute_dew_point(avg_temp, avg_humidity)

    # Anomaly checks
    anomalies = []
    if pressure_trend <= -2.0 or avg_pressure < 995.0:
        anomalies.append("RAPID_BAROMETRIC_DROP_STORM_SURGE")
    if max_wind > 17.0:
        anomalies.append("GALE_FORCE_WIND_GUST")
    if heat_index >= 41.0:
        anomalies.append("DANGEROUS_HEAT_INDEX")
    if total_rain >= 30.0:
        anomalies.append("HEAVY_TORRENTIAL_RAIN")
    if avg_pm25 > 100.0:
        anomalies.append("HAZARDOUS_AIR_QUALITY")

    return {
        "station_id": station_id,
        "station_name": station_name,
        "region": region,
        "lat": lat,
        "lon": lon,
        "window_type": window_type, # TUMBLING or SLIDING
        "window_start": window_start,
        "window_end": window_end,
        "window_duration_sec": round(window_end - window_start, 2),
        "record_count": len(records),
        "metrics": {
            "temp_avg": round(avg_temp, 2),
            "temp_min": round(min(temps), 2) if temps else 0.0,
            "temp_max": round(max(temps), 2) if temps else 0.0,
            "humidity_avg": round(avg_humidity, 1),
            "pressure_avg": round(avg_pressure, 2),
            "pressure_trend_hpa": pressure_trend,
            "wind_speed_avg": round(avg_wind, 2),
            "wind_gust_max": round(max_wind, 2),
            "rainfall_avg_mm_h": round(total_rain, 2),
            "pm25_avg": round(avg_pm25, 1),
            "uv_index_max": round(max_uv, 1),
            "heat_index_c": heat_index,
            "dew_point_c": dew_point
        },
        "anomalies": anomalies,
        "created_at": window_end
    }
