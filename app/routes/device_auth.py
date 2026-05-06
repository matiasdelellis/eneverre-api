import time
import secrets
from flask import Blueprint, request, jsonify
from app.auth import auth
from app.db import get_db


bp = Blueprint("device_auth", __name__)


def gen_code(n=6):
    return secrets.token_hex(n//2).upper()

# Remove old tokens
def cleanup_tokens(db):
    db.execute(
        "DELETE FROM device_login WHERE expires_at < ?",
        (int(time.time()),)
    )

# TV request loogin token
@bp.route("/api/auth/device")
def create_device():
    db = get_db()

    device_code = secrets.token_urlsafe(16)
    user_code = gen_code(6)
    expires_at = int(time.time()) + 300

    db.execute(
        "INSERT INTO device_login VALUES (?, ?, ?, ?, ?)",
        (device_code, user_code, "pending", None, expires_at)
    )
    db.commit()

    return jsonify({
        "device_code": device_code,
        "user_code": user_code,
        "expires_in": 300
    })


# TV polling until aproved.
@bp.route("/api/auth/device/<device_code>")
def check_device(device_code):
    db = get_db()

    row = db.execute(
        "SELECT status, username, expires_at FROM device_login WHERE device_code=?",
        (device_code,)
    ).fetchone()

    if not row:
        return jsonify({"error": "Invalid device"}), 404

    status, username, expires_at = row

    # Check expired status
    if status == "expired":
        return jsonify({"status": "expired"})

    # Check expire by time and mark
    if expires_at < int(time.time()):
        db.execute(
            "UPDATE device_login SET status='expired' WHERE device_code=?", (device_code,)
        )
        db.commit()
        return jsonify({"status": "expired"})

    # If aproved send token
    if status == "approved":
        # Generate token
        token = secrets.token_urlsafe(16)
        expires_at = int(time.time()) + 86400

        db.execute(
            "INSERT INTO tokens VALUES (?, ?, ?)", (token, username, expires_at)
        )
        db.commit()

        # Mark as expired due consumed
        db.execute(
            "UPDATE device_login SET status='expired' WHERE device_code=?", (device_code,)
        )
        db.commit()

        # Send token
        return jsonify({
            "status": "approved",
            "token": token,
            "expires_at": expires_at
        })

    return jsonify({"status": "pending"})

# User aprove login
@bp.route("/api/auth/device/verify", methods=["POST"])
@auth.login_required
def verify_device():
    data = request.json or {}
    user_code = data.get("user_code")

    if not user_code:
        return jsonify({"error": "Missing fields"}), 400

    db = get_db()
    row = db.execute(
        "SELECT status, username, expires_at FROM device_login WHERE user_code=?",
        (user_code,)
    ).fetchone()

    if not row:
        return jsonify({"error": "Invalid user_code"}), 404

    status, username, expires_at = row

    # Treat approved as expired
    if status == "approved":
        return jsonify({"status": "expired"})

    # Check expired status
    if status == "expired":
        return jsonify({"status": "expired"})

    # Check expire by time and mark
    if expires_at < int(time.time()):
        db.execute(
            "UPDATE device_login SET status='expired' WHERE device_code=?", (device_code,)
        )
        db.commit()
        return jsonify({"status": "expired"})

    # Mark as Aproved
    db.execute(
        "UPDATE device_login SET status='approved', username=? WHERE user_code=?",
        (request.authorization.username, user_code)
    )
    db.commit()

    return jsonify({"status": "approved"})
