import os
import configparser

config = configparser.ConfigParser()

CONFIG_FILE = '/etc/eneverre/eneverre.ini' if os.path.exists('/etc/eneverre/eneverre.ini') else './data/eneverre.ini'
if not os.path.exists(CONFIG_FILE):
    raise RuntimeError("Missing eneverre.ini")

CAMERAS_FOLDER = '/etc/eneverre/cameras.d' if os.path.exists('/etc/eneverre/cameras.d') else './data/cameras.d'
if not os.path.exists(CAMERAS_FOLDER):
    raise RuntimeError("Missing cameras.d folder")

DB_FILE = '/var/run/eneverre/eneverre.db' if os.path.exists('/var/run/eneverre/eneverre.db') else './data/eneverre.db'

config.read(CONFIG_FILE)

SERVER = config['server']
MEDIAMTX = config['mediamtx'] if config.has_section('mediamtx') else None
