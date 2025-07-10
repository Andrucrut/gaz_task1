import sys

from loguru import logger

logger.add(
    sink=sys.stderr,
    format=(
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS!UTC}Z</green> | "
        "<cyan>{process}</cyan> | "
        "<level>{level: <8}</level> | "
        "<cyan>{file}:{line}</cyan> | "
        "<level>{message}</level>"
    ),
)
