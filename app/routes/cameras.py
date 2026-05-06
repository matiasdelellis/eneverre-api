from flask import Blueprint, jsonify
from app.auth import api_auth
from app.services.camera_service import load_cameras
from app.models.camera import public

bp = Blueprint('cameras', __name__)

cameras = load_cameras()

@bp.route('/api/cameras')
@api_auth.login_required
def get_all():
    return jsonify([public(c) for c in cameras])
