import sys
from pathlib import Path
from loguru import logger
from datetime import datetime


class Logger:
    def __init__(self, log_dir="logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self._setup_logger()

    def _setup_logger(self):
        logger.remove()
        
        logger.add(
            sys.stdout,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            level="INFO",
            colorize=True
        )
        
        log_file = self.log_dir / f"test_{datetime.now().strftime('%Y%m%d')}.log"
        logger.add(
            log_file,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            level="DEBUG",
            rotation="00:00",
            retention="30 days",
            encoding="utf-8"
        )
        
        error_log = self.log_dir / f"error_{datetime.now().strftime('%Y%m%d')}.log"
        logger.add(
            error_log,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            level="ERROR",
            rotation="00:00",
            retention="30 days",
            encoding="utf-8"
        )

    @staticmethod
    def get_logger():
        return logger


log = Logger().get_logger()
