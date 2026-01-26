import logging
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
MOVIE_CATALOG_STORAGE_FILEPATH = BASE_DIR / "movie-catalog.json"


LOG_LEVEL = logging.INFO
LOG_FORMAT: str = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)

# # Never store real tokens here! Only fake values
API_TOKENS = frozenset(
    {
        "qEXvw586M1Iet8ADHMa36w",
        "KV5jJAFkpBmExzu8bXak-w",
    }
)

# Only for demo!
# No real users in code!!
USER_DB: dict[str, str] = {
    # username: password
    "sam": "password",
    "bob": "qwerty",
}

REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_DB_TOKENS = 1
REDIS_DB_USERS = 2

REDIS_TOKENS_SET_NAME = "tokens"
