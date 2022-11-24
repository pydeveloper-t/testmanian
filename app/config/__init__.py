from util import mkdir_p
from datetime import datetime
import os
import yaml
import logging

MAX_HTTP_ATTEMPTS = 3
PROJECT_TAG = 'testmanian'
config_file = os.getenv(f'{PROJECT_TAG}_cfg', '')
try:
    with open(config_file) as f:
        CONFIG = yaml.safe_load(f)
except Exception as exc:
    print(f'[CONFIGURATION] Could not open configuration file {config_file}. Exception: {exc}')
    raise SystemExit

logger = logging.getLogger(f'{PROJECT_TAG}')
log_file_name = f"{PROJECT_TAG}_{datetime.utcnow().strftime('%Y%m%d')}.log"
base_dir = os.path.abspath(CONFIG['pathes']['basepath'])
log_dir = mkdir_p(os.path.join(base_dir, 'log'))
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler(os.path.join(log_dir, log_file_name))
c_handler.setLevel(logging.INFO)
f_handler.setLevel(logging.INFO)
c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)
logger.addHandler(c_handler)
logger.addHandler(f_handler)
logger.setLevel(logging.INFO)