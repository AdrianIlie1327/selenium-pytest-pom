"""Central place for test settings.

The environment is chosen with TEST_ENV (default "dev") and loaded from
envs/<TEST_ENV>.env. Real environment variables still win over the file.
"""
import os
from pathlib import Path

ENV_NAME = os.getenv("TEST_ENV", "dev")
ENV_FILE = Path(__file__).parent / "envs" / f"{ENV_NAME}.env"


def _load_env_file(path: Path) -> dict:
    if not path.is_file():
        raise FileNotFoundError(f"Unknown TEST_ENV '{ENV_NAME}': {path} does not exist")
    values = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            values[key.strip()] = value.strip()
    return values


_ENV = _load_env_file(ENV_FILE)


def _get(key: str) -> str:
    return os.getenv(key, _ENV[key])


BASE_URL = _get("BASE_URL")
API_BASE_URL = _get("API_BASE_URL")
DEFAULT_TIMEOUT = int(_get("TIMEOUT"))

# Public demo credentials published on the SauceDemo login page.
VALID_USER = "standard_user"
LOCKED_USER = "locked_out_user"
PASSWORD = "secret_sauce"
