import os, configparser

from app.config import MEDIAMTX, CAMERAS_FOLDER
from app.services.mediamtx_service import rtsp_url, hls_url, hls_thumb_url


def load_cameras():
    folder = CAMERAS_FOLDER

    cams = []

    for file in os.listdir(folder):
        config = configparser.ConfigParser()
        config.read(os.path.join(folder, file))

        cam = config['camera']
        thingino = config['thingino'] if config.has_section('thingino') else {}

        cam_id = cam['id']

        if MEDIAMTX:
            server = MEDIAMTX.get('server')
            live = rtsp_url(server, MEDIAMTX.get('rtsp_port', '8554'), cam_id)
            hls = hls_url(server, cam_id)
            hls_thumb = hls_thumb_url(server, cam_id)
        else:
            live = cam['live']
            hls = ""
            hls_thumb = ""

        cams.append({
            "id": cam_id,
            "name": cam.get('name', ''),
            "comment": cam.get('comment', ''),
            "location": cam.get('location', ''),
            "live": live,
            "hls": hls,
            "hls_thumb": hls_thumb,
            "width": int(cam.get('width', 0)),
            "height": int(cam.get('height', 0)),

            # MediaMTX
            "playback": cam.getboolean('playback', fallback=False),

            # PTZ / Thingino
            "ptz": thingino.get('ptz', 'false') == 'true',
            "thingino_url": thingino.get('thingino_url'),
            "thingino_api_key": thingino.get('thingino_api_key'),

            # PTZ
            "home_x": int(thingino.get('home_x', -1)),
            "home_y": int(thingino.get('home_y', -1)),
            "privacy_x": int(thingino.get('privacy_x', -1)),
            "privacy_y": int(thingino.get('privacy_y', -1)),

            # Runtime
            "privacy": False
        })

    return cams


def get_camera(cameras, cam_id):
    return next((c for c in cameras if c["id"] == cam_id), None)
