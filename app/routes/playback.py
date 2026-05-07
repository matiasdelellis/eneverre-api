from flask import Blueprint, request, jsonify, Response
from app.auth import auth
from app.services.camera_service import load_cameras, get_camera
from app.services.mediamtx_service import creds
from app.config import MEDIAMTX

import requests
import urllib.parse

bp = Blueprint('playback', __name__)


@bp.route('/api/camera/<cam_id>/playback/list')
@auth.login_required
def playback_list(cam_id):
    if not MEDIAMTX:
        return jsonify({"error": "Not Found"}), 404

    cameras = load_cameras()
    cam = get_camera(cameras, cam_id)

    if not cam or not cam["playback"]:
        return jsonify({"error": "Not found"}), 404

    start = request.args.get('start')
    end = request.args.get('end')

    if not start or not end:
        return jsonify({"error": "Bad Request"}), 400

    base = f"http://localhost:{MEDIAMTX.get('playback_port','9996')}/list"
    url = f"{base}?path={cam_id}&start={start}&end={end}"

    r = requests.get(
        url,
        auth=(creds["username"], creds["password"]),
        timeout=10
    )

    return jsonify([
        {"start": x["start"], "duration": x["duration"]} for x in r.json()
    ])


@bp.route('/api/camera/<cam_id>/playback/get')
@auth.login_required
def playback_get(cam_id):
    if not MEDIAMTX:
        return jsonify({"error": "Not Found"}), 404

    cameras = load_cameras()
    cam = get_camera(cameras, cam_id)

    if not cam or not cam["playback"]:
        return jsonify({"error": "Not found"}), 404

    start = request.args.get('start')
    duration = request.args.get('duration')

    if not start or not duration:
        return jsonify({"error": "Bad Request"}), 400

    params = urllib.parse.urlencode({
        "path": cam_id,
        "start": start,
        "duration": duration,
        "format": "mp4"
    })

    url = f"http://localhost:{MEDIAMTX.get('playback_port','9996')}/get/?{params}"

    r = requests.get(
        url,
        stream=True,
        auth=(creds["username"], creds["password"]),
        timeout=10
    )

    return Response(
        r.iter_content(8192),
        content_type=r.headers.get('content-type')
    )
