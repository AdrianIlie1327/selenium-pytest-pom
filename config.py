"""Central place for test settings. Override via environment variables."""
import os

BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com")
API_BASE_URL = os.getenv("API_BASE_URL", "https://jsonplaceholder.typicode.com")
DEFAULT_TIMEOUT = int(os.getenv("TIMEOUT", "10"))

# Public demo credentials published on the SauceDemo login page.
VALID_USER = "standard_user"
LOCKED_USER = "locked_out_user"
PASSWORD = "secret_sauce"
