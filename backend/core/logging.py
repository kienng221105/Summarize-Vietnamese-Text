import logging
from logging.handlers import RotatingFileHandler

# Cấu hình logging để ghi vào file backend.log
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("backend")
handler = RotatingFileHandler("backend.log", maxBytes=1000000, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def log_error(msg):
    logger.error(msg)

def log_info(msg):
    logger.info(msg)
