import logging
import os
from datetime import datetime


def setup_logging():
    log_dir = os.path.abspath("ETL/logs")
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(
        log_dir,
        f"etl_{datetime.now():%Y%m%d}.log"
    )

    logging.basicConfig(
        level=logging.INFO,
        format=(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(name)s | "
            "%(message)s"
        ),
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(
                log_file,
                encoding="utf-8"
            )
        ]
    )