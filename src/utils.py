import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    force=True
)

logger = logging.getLogger("Proyecto_M3")

PROJECT_ROOT = Path(__file__).resolve().parent.parent

