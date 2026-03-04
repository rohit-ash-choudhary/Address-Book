import logging
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

from .config import GEOCODING_TIMEOUT, GEOCODING_USER_AGENT

log = logging.getLogger(__name__)
_geo = None

def geocode_address(street, city):
    global _geo
    if _geo is None:
        _geo = Nominatim(user_agent=GEOCODING_USER_AGENT, timeout=GEOCODING_TIMEOUT)
    q = f"{street.strip()}, {city.strip()}"
    try:
        loc = _geo.geocode(q)
        if not loc:
            raise ValueError(f"Could not find: {q}")
        return (loc.latitude, loc.longitude)
    except GeocoderTimedOut:
        log.warning("Geocode timeout: %s", q)
        raise ValueError("Geocode timed out - try again or send lat/lon")
    except GeocoderServiceError as e:
        log.warning("Geocode error: %s", e)
        raise ValueError(str(e))
