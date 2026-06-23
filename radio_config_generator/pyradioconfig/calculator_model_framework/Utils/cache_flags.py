import os


ADVANCED_CACHE_ENV_VAR = "RADIO_CONF_ADVANCED_CACHE_EN"


def is_advanced_cache_enabled():
    """Return True when advanced in-memory caches are enabled."""
    value = os.environ.get(ADVANCED_CACHE_ENV_VAR, "False")
    return str(value).strip().lower() in ("1", "true", "yes", "on")
