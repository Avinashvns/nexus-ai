from pathlib import Path

from loguru import logger

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

logger.remove()

logger.add(
    LOG_DIR / "nexus.log",
    rotation="10 MB",
    retention="10 days",
    level="INFO",
    enqueue=True,
)

logger.add(
    sink=lambda message: print(message, end=""),
    level="INFO",
)

app_logger = logger