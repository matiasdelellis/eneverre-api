import configparser
import os
import yaml

INPUT_DIR = "data/cameras.d"
OUTPUT_FILE = "data/mediamtx.yml"

def load_camera_configs(directory):
    paths = {}

    for filename in os.listdir(directory):
        if not filename.endswith('.ini'):
            continue

        filepath = os.path.join(directory, filename)

        config = configparser.ConfigParser()
        config.read(filepath)

        if 'camera' not in config:
            print(f"[WARN] {filename}: invalid camera")
            continue

        camera = config['camera']

        camera_id = camera.get('id')
        live_url = camera.get('live')

        if not camera_id or not live_url:
            print(f"[WARN] {filename}: missing id or live")
            continue

        paths[camera_id] = {
            'source': live_url,
        }

        print(f"[OK] {camera_id} -> {live_url}")

    return paths


def generate_mediamtx_config(paths):
    config = {
        'authMethod': 'http',
        'authHTTPAddress': 'http://localhost:8080/api/auth',

        'pathDefaults': {
            'record': True,
            'recordPath': 'data/recordings/%path/%Y-%m-%d/%H/%M-%S-%f',
            'recordFormat': 'fmp4',
            'recordPartDuration': '1s',
            'recordSegmentDuration': '1h',
            'recordDeleteAfter': '10d',
            'sourceOnDemand': False
        },
        'paths': paths
    }

    with open(OUTPUT_FILE, 'w') as f:
        yaml.dump(config, f, sort_keys=False)

    print(f"\nDone: {OUTPUT_FILE}")


if __name__ == '__main__':
    paths = load_camera_configs(INPUT_DIR)
    generate_mediamtx_config(paths)
