import requests
import os
from typing import Optional, Tuple, Dict, Any, List
from datetime import date
from statistics import median
from .models import LocationInput, ClimateData

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Identify this app on the public Nominatim service (required by its usage policy).
_NOMINATIM_HEADERS = {
    "User-Agent": "AskJaneGardenPlanner/4.2 (https://github.com/shaythegay13/agenticaigardenplanner)",
    "Accept": "application/json",
}


def _google_maps_api_key() -> str:
    """Return the Google Maps key when one is configured. Empty means use Nominatim."""
    return os.environ.get("GOOGLE_MAPS_API_KEY", "").strip()


def _geocode_google(address: str, api_key: str) -> Tuple[float, float]:
    print(f"[GEOCODING] Using Google Maps API for address: {address}")
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": address, "key": api_key}
    try:
        resp = requests.get(url, params=params, timeout=20)
        resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Failed to connect to Google Maps API: {str(e)}")

    data = resp.json()
    print(f"[GEOCODING] Google Maps API status: {data.get('status')}")
    if data.get("status") == "OK" and data.get("results"):
        result = data["results"][0]
        lat = result["geometry"]["location"]["lat"]
        lon = result["geometry"]["location"]["lng"]
        print(f"[GEOCODING] Success: {lat}, {lon}")
        return float(lat), float(lon)
    if data.get("status") == "ZERO_RESULTS":
        raise ValueError(f"Address not found: {address}")
    if data.get("status") == "REQUEST_DENIED":
        raise ValueError("Google Maps API request denied. Check your API key and enabled APIs.")
    raise ValueError(
        f"Geocoding error: {data.get('status')} - {data.get('error_message', 'Unknown error')}"
    )


def _geocode_nominatim(address: str) -> Tuple[float, float]:
    """Free address lookup used when GOOGLE_MAPS_API_KEY is unset."""
    print(f"[GEOCODING] Using OpenStreetMap Nominatim for address: {address}")
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": address, "format": "jsonv2", "limit": 1}
    try:
        resp = requests.get(url, params=params, headers=_NOMINATIM_HEADERS, timeout=20)
        resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Failed to connect to OpenStreetMap Nominatim: {str(e)}")

    data = resp.json()
    if not data:
        raise ValueError(f"Address not found: {address}")
    lat = float(data[0]["lat"])
    lon = float(data[0]["lon"])
    print(f"[GEOCODING] Success: {lat}, {lon}")
    return lat, lon


def geocode_location(location: LocationInput) -> Tuple[float, float]:
    """
    Resolve latitude/longitude from an address, or return coordinates already provided.

    Uses the Google Maps Geocoding API when GOOGLE_MAPS_API_KEY is set.
    Otherwise uses the OpenStreetMap Nominatim search API, which needs no key.
    """
    if location.has_coordinates():
        return location.latitude, location.longitude

    if not location.address:
        raise ValueError("Either coordinates or an address must be provided.")

    api_key = _google_maps_api_key()
    if api_key:
        return _geocode_google(location.address, api_key)
    return _geocode_nominatim(location.address)


def _reverse_geocode_google(lat: float, lon: float, api_key: str) -> Dict[str, Optional[str]]:
    print(f"[REVERSE GEOCODING] Using Google Maps API for coordinates: {lat}, {lon}")
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"latlng": f"{lat},{lon}", "key": api_key}
    try:
        resp = requests.get(url, params=params, timeout=20)
        resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Failed to connect to Google Maps API: {str(e)}")

    data = resp.json()
    print(f"[REVERSE GEOCODING] Google Maps API status: {data.get('status')}")
    if data.get("status") == "OK" and data.get("results"):
        result = data["results"][0]
        components = {c["types"][0]: c["long_name"] for c in result.get("address_components", [])}
        country_code = next(
            (c["short_name"] for c in result.get("address_components", []) if "country" in c["types"]),
            None,
        )
        location_data = {
            "city": (
                components.get("locality")
                or components.get("sublocality")
                or components.get("administrative_area_level_3")
            ),
            "state": components.get("administrative_area_level_1"),
            "country": components.get("country"),
            "country_code": country_code.lower() if country_code else None,
        }
        print(f"[REVERSE GEOCODING] Success: {location_data}")
        return location_data
    if data.get("status") == "ZERO_RESULTS":
        raise ValueError(f"No address found for coordinates: {lat}, {lon}")
    if data.get("status") == "REQUEST_DENIED":
        raise ValueError("Google Maps API request denied. Check your API key and enabled APIs.")
    raise ValueError(
        f"Reverse geocoding error: {data.get('status')} - {data.get('error_message', 'Unknown error')}"
    )


def _reverse_geocode_nominatim(lat: float, lon: float) -> Dict[str, Optional[str]]:
    print(f"[REVERSE GEOCODING] Using OpenStreetMap Nominatim for coordinates: {lat}, {lon}")
    url = "https://nominatim.openstreetmap.org/reverse"
    params = {"lat": lat, "lon": lon, "format": "jsonv2"}
    try:
        resp = requests.get(url, params=params, headers=_NOMINATIM_HEADERS, timeout=20)
        resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Failed to connect to OpenStreetMap Nominatim: {str(e)}")

    data = resp.json()
    if data.get("error"):
        raise ValueError(f"No address found for coordinates: {lat}, {lon}")
    address = data.get("address") or {}
    city = (
        address.get("city")
        or address.get("town")
        or address.get("village")
        or address.get("hamlet")
        or address.get("municipality")
    )
    country_code = address.get("country_code")
    location_data = {
        "city": city,
        "state": address.get("state"),
        "country": address.get("country"),
        "country_code": country_code.lower() if country_code else None,
    }
    print(f"[REVERSE GEOCODING] Success: {location_data}")
    return location_data


def reverse_geocode(lat: float, lon: float) -> Dict[str, Optional[str]]:
    """
    Reverse geocode lat/lon to city, state, and country.

    Uses Google Maps when GOOGLE_MAPS_API_KEY is set, otherwise OpenStreetMap Nominatim.
    """
    api_key = _google_maps_api_key()
    if api_key:
        return _reverse_geocode_google(lat, lon, api_key)
    return _reverse_geocode_nominatim(lat, lon)


def infer_us_region(state: Optional[str]) -> Optional[str]:
    if not state:
        return None
    northeast = {"Maine","New Hampshire","Vermont","Massachusetts","Rhode Island","Connecticut","New York","New Jersey","Pennsylvania"}
    midwest = {"Ohio","Michigan","Indiana","Wisconsin","Illinois","Minnesota","Iowa","Missouri","North Dakota","South Dakota","Nebraska","Kansas"}
    south = {"Delaware","Maryland","District of Columbia","Virginia","West Virginia","North Carolina","South Carolina","Georgia","Florida","Kentucky","Tennessee","Mississippi","Alabama","Arkansas","Louisiana","Oklahoma","Texas"}
    west = {"Montana","Idaho","Wyoming","Colorado","New Mexico","Arizona","Utah","Nevada","Washington","Oregon","California","Alaska","Hawaii"}
    if state in northeast: return "Northeast"
    if state in midwest: return "Midwest"
    if state in south: return "South"
    if state in west: return "West"
    return None


def _fetch_daily_mins_era5(lat: float, lon: float, start: str, end: str) -> List[float]:
    url = "https://archive-api.open-meteo.com/v1/era5"
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start,
        "end_date": end,
        "daily": ["temperature_2m_min"],
        "timezone": "UTC",
    }
    resp = requests.get(url, params=params, timeout=60)
    resp.raise_for_status()
    data = resp.json()
    return data.get("daily", {}).get("temperature_2m_min", [])


def _usda_zone_from_abs_min_c(abs_min_c: float) -> Optional[str]:
    # Map absolute minimum temp to USDA hardiness zones (Celsius)
    # Source ranges converted from Fahrenheit
    zone_ranges = [
        ("1", -51.1, -45.6), ("2", -45.5, -40.0), ("3", -39.9, -34.5), ("4", -34.4, -28.9),
        ("5", -28.8, -23.3), ("6", -23.2, -17.8), ("7", -17.7, -12.2), ("8", -12.1, -6.7),
        ("9", -6.6, -1.1), ("10", -1.0, 4.4), ("11", 4.5, 10.0), ("12", 10.1, 15.6), ("13", 15.7, 21.1)
    ]
    for zone, lo, hi in zone_ranges:
        if lo <= abs_min_c <= hi:
            return zone
    return None


def estimate_zone_and_frost(lat: float, lon: float) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """Estimate USDA zone and typical last/first frost dates using ERA5 daily mins over the last 8 years."""
    today = date.today()
    start = date(today.year - 8, 1, 1).isoformat()
    end = today.isoformat()
    mins = _fetch_daily_mins_era5(lat, lon, start, end)
    if not mins:
        return None, None, None
    abs_min = min(mins)
    zone = _usda_zone_from_abs_min_c(abs_min)

    # Compute frost dates per year (<= 0C), take median day-of-year
    # Build list of yearly indices
    frosts_last_spring = []
    frosts_first_fall = []
    # Build dates list
    all_days = []
    cur = date(today.year - 8, 1, 1)
    while cur <= today:
        all_days.append(cur)
        cur = date.fromordinal(cur.toordinal() + 1)
    if len(all_days) != len(mins):
        # Fallback if mismatch
        return zone, None, None

    by_year: Dict[int, List[Tuple[date, float]]] = {}
    for d, tmin in zip(all_days, mins):
        by_year.setdefault(d.year, []).append((d, tmin))

    for yr, seq in by_year.items():
        # Last spring frost: latest date between Jan 1 and Jun 30 with tmin <= 0C
        spring = [d for d, t in seq if d.timetuple().tm_yday <= date(yr,6,30).timetuple().tm_yday and t <= 0.0]
        if spring:
            frosts_last_spring.append(max(spring))
        # First fall frost: earliest date between Aug 1 and Dec 31 with tmin <= 0C
        fall = [d for d, t in seq if d >= date(yr,8,1) and t <= 0.0]
        if fall:
            frosts_first_fall.append(min(fall))

    def _fmt(dt_list: List[date]) -> Optional[str]:
        if not dt_list:
            return None
        # Median by ordinal
        ords = sorted([d.toordinal() for d in dt_list])
        med_ord = ords[len(ords)//2]
        d = date.fromordinal(med_ord)
        return d.strftime("%b %d")

    return zone, _fmt(frosts_last_spring), _fmt(frosts_first_fall)


def fetch_simple_forecast(lat: float, lon: float) -> ClimateData:
    """
    Fetch a 7-day simple forecast from Open-Meteo.
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": [
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_sum",
        ],
        "forecast_days": 7,
        "timezone": "auto",
    }
    resp = requests.get(url, params=params, timeout=20)
    resp.raise_for_status()
    data = resp.json()

    daily = data.get("daily", {})
    highs = daily.get("temperature_2m_max", [])
    lows = daily.get("temperature_2m_min", [])
    precip = daily.get("precipitation_sum", [])
    tz = data.get("timezone", "auto")

    summary = (
        f"Next 7 days: avg high {sum(highs)/len(highs):.1f}°C, "
        f"avg low {sum(lows)/len(lows):.1f}°C, "
        f"total precip {sum(precip):.1f} mm"
        if highs and lows and precip else "Forecast unavailable"
    )

    # Place names and frost dates enrich the plan. Either lookup can fail
    # without blocking the forecast the rest of the planner needs.
    try:
        meta = reverse_geocode(lat, lon)
    except Exception as exc:
        print(f"[REVERSE GEOCODING] Continuing without place names: {exc}")
        meta = {"city": None, "state": None, "country": None, "country_code": None}

    country_code = (meta.get("country_code") or "").lower()
    us_region = infer_us_region(meta.get("state")) if country_code == "us" else None
    try:
        zone, frost_last, frost_first = estimate_zone_and_frost(lat, lon)
    except Exception as exc:
        print(f"[CLIMATE] Zone and frost estimate unavailable: {exc}")
        zone, frost_last, frost_first = None, None, None

    return ClimateData(
        latitude=lat,
        longitude=lon,
        timezone=tz,
        daily_highs_c=highs,
        daily_lows_c=lows,
        daily_precip_mm=precip,
        summary=summary,
        country=meta.get("country"),
        state=meta.get("state"),
        city=meta.get("city"),
        us_region=us_region,
        usda_zone=zone,
        frost_last_spring=frost_last,
        frost_first_fall=frost_first,
    )
