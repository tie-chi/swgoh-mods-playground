import logging
import os
from time import sleep
from libs.fs import check_dir_exists
from libs.hotutils.connector import HotUtilsConnector, HotUtilsConnectorConfigs

# Define directories and file paths
DATA_DIR = "data"
COOKIE_FILE = os.path.join(DATA_DIR, "hotutils_cookie.pkl")
HOTUTILS_DATA_FILE = os.path.join(DATA_DIR, "hotutils_raw_data.pkl")
MODS_DUMP_FILE = os.path.join(DATA_DIR, "hotutils_mods_dump.pkl")

# Check if directories exist
is_data_dir_exists = check_dir_exists(DATA_DIR, should_create=True)
if not is_data_dir_exists:
    raise

# Connect to HotUtils and get all data
connector_configs = HotUtilsConnectorConfigs(COOKIE_FILE, HOTUTILS_DATA_FILE, MODS_DUMP_FILE, logging.INFO)
connector = HotUtilsConnector(connector_configs)
connector.login()
connector.get_all_data()
mods = connector.get_mods()
connector.close()
