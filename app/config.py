import os
import configparser

config = configparser.ConfigParser()

CONFIG_FILE = '/etc/eneverre/eneverre.ini' if os.path.exists('/etc/eneverre/eneverre.ini') else './eneverre.ini'
DB_FILE = '/var/run/eneverre/eneverre.db' if os.path.exists('/var/run/eneverre/eneverre.db') else './data/eneverre.db'

config.read(CONFIG_FILE)

SERVER = config['server']
MEDIAMTX = config['mediamtx'] if config.has_section('mediamtx') else None
