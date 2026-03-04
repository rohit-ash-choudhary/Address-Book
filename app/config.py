import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

def get_env(key, default=None):
    v = os.getenv(key)
    if v:
        return v
    if default is not None:
        return default
    raise ValueError(f"Missing: {key}")

DATABASE_URL = get_env("DATABASE_URL", "sqlite:///./addresses.db")
GEOCODING_TIMEOUT = int(get_env("GEOCODING_TIMEOUT_SECONDS", "5"))
GEOCODING_USER_AGENT = get_env("GEOCODING_USER_AGENT", "AddressBookApp/1.0")
LOG_LEVEL = get_env("LOG_LEVEL", "INFO")
