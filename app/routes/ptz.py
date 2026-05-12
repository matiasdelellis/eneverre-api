from flask import Blueprint, request, jsonify
from app.auth import auth
from app.services.camera_service import load_cameras, get_camera
from app.services.thingino_service import move

bp = Blueprint('ptz', __name__)

cameras = load_cameras()

@bp.route('/api/camera/<cam_id>/ptz', methods=['POST'])
@auth.login_required
def ptz(cam_id):
    cam = get_camera(cameras, cam_id)

    if not cam or not cam['ptz']:
        return jsonify({"error": "PTZ not available"}), 404

    try:
        x = int(request.args.get('x', 0))
        y = int(request.args.get('y', 0))
    except:
        return jsonify({"error": "Invalid params"}), 400

    host = camera['thingino_url']
    api_key = camera['thingino_api_key']

    return jsonify(move(host, api_key, x, y))
