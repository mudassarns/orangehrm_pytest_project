import logging
from datetime import datetime
from pathlib import Path


LOG_DIR = Path("reports/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / (
    f"test_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_FILE, encoding="utf-8")
    ]
)


def get_logger(name):
    return logging.getLogger(name)