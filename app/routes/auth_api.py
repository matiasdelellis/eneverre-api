from flask import Blueprint, request, jsonify
from app.services.mediamtx_service import creds
from app.config import MEDIAMTX

bp = Blueprint('auth_api', __name__)

@bp.route('/api/auth', methods=['POST'])
def auth_api():
    if not MEDIAMTX:
        return jsonify({"error": "Not Found"}), 404

    data = request.json or {}

    if data.get('user') == creds['username'] and data.get('password') == creds['password']:
        return jsonify({"message": "Authorized"}), 200

    return jsonify({"message": "Unauthorized"}), 401
