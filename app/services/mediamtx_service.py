import os, json, random, string

FILE = './data/mediamtx_credentials.json'

def get_primary_creds():
    return load_creds()["current"]

def _gen(n=8):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(n))

def load_creds():
    if os.path.exists(FILE):
        with open(FILE) as f:
            return json.load(f)

    creds = {"username": _gen(), "password": _gen()}
    os.makedirs(os.path.dirname(FILE), exist_ok=True)

    with open(FILE, "w") as f:
        json.dump(creds, f)

    return creds

creds = load_creds()

def rtsp_url(server, port, cam_id):
    return f"rtsp://{creds['username']}:{creds['password']}@{server}:{port}/{cam_id}"

def hls_url(server, cam_id):
    return f"https://{creds['username']}:{creds['password']}@{server}/hls/{cam_id}/index.m3u8"
