from functools import wraps
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth
from werkzeug.security import check_password_hash
from app.db import get_db
import time

auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth(scheme='Bearer')

api_auth = MultiAuth(auth, token_auth)

@auth.verify_password
def verify_password(username, password):
    db = get_db()
    row = db.execute(
        "SELECT password, role FROM users WHERE username = ?",
        (username,)
    ).fetchone()

    if not row:
        return None

    if not check_password_hash(row[0], password):
        return None

    return {
        "username": username,
        "role": row[1]
    }

@token_auth.verify_token
def verify_token(token):
    db = get_db()

    row = db.execute(
        """
        SELECT username, expires_at FROM tokens
        WHERE token=?
        """,
        (token,)
    ).fetchone()

    if not row:
        return None

    username, expires_at = row

    if expires_at and expires_at < int(time.time()):
        return None

    user = db.execute(
        "SELECT role FROM users WHERE username=?",
        (username,)
    ).fetchone()

    if not user:
        return None

    return {
        "username": username,
        "role": user[0]
    }

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user = current_user()
        if not user or user["role"] != "admin":
            return jsonify({"error": "Admin required"}), 403
        return f(*args, **kwargs)
    return decorated
