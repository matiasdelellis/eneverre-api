from functools import wraps
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash
from app.db import get_db

auth = HTTPBasicAuth()

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

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user = current_user()
        if not user or user["role"] != "admin":
            return jsonify({"error": "Admin required"}), 403
        return f(*args, **kwargs)
    return decorated
