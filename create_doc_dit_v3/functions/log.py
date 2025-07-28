import logging
import sys
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)

def configurar_logger(base_dir: Path):
    log_dir = base_dir / ".log"
    log_dir.mkdir(parents=True, exist_ok=True)

    log_filename = datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".log"
    log_path = log_dir / log_filename

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_path),
            logging.StreamHandler(sys.stdout)
        ]
    )

    logger.info(f"Arquivo de log criado: {log_path}")
    return logger
