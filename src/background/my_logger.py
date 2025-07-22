import logging
import os
import sys
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def setup_logger(logs_folder: str) -> None:
    """
    initialize logger

    :param logs_folder: the folder where the log files will be stored
    :return: None
    """

    if logs_folder == "":
        logs_folder = str(Path(__file__).parents[2].joinpath("logs").absolute())

    os.makedirs(logs_folder, exist_ok=True)

    log_filename = str(Path(logs_folder).joinpath(f"logger_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log").absolute())
    file_handler = logging.FileHandler(log_filename, mode='a', encoding='utf-8')
    file_handler.setLevel(logging.INFO)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s | %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            return
        logger.error("Unhandled exception", exc_info=(exc_type, exc_value, exc_traceback))

    sys.excepthook = handle_exception
