from flask import Blueprint, request, jsonify
from app.auth import auth, admin_required
from app.db import get_db
from werkzeug.security import generate_password_hash

bp = Blueprint('users', __name__)


@bp.route('/api/users')
@auth.login_required
@admin_required
def list_users():
    db = get_db()
    rows = db.execute("SELECT username, role FROM users").fetchall()

    return jsonify([
        {"username": r[0], "role": r[1]}
        for r in rows
    ])

@bp.route('/api/users', methods=['POST'])
@auth.login_required
@admin_required
def create_user():
    data = request.json or {}

    username = data.get("username")
    password = data.get("password")
    role = data.get("role", "user")

    if not username or not password:
        return jsonify({"error": "Missing fields"}), 400

    if role not in ("admin", "user"):
        return jsonify({"error": "Invalid role"}), 400

    db = get_db()

    try:
        db.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            (username, generate_password_hash(password), role)
        )
        db.commit()
    except Exception as e:
        return jsonify({"error": "User exists"}), 400

    return jsonify({"message": "User created"}), 201

@bp.route('/api/users/<username>/role', methods=['PUT'])
@auth.login_required
@admin_required
def update_role(username):
    role = request.json.get("role")

    if role not in ("admin", "user"):
        return jsonify({"error": "Invalid role"}), 400

    db = get_db()
    db.execute("UPDATE users SET role=? WHERE username=?", (role, username))
    db.commit()

    return jsonify({"message": "Role updated"})

@bp.route('/api/users/<username>/password', methods=['PUT'])
@auth.login_required
@admin_required
def change_password(username):
    password = request.json.get("password")

    if not password:
        return jsonify({"error": "Missing password"}), 400

    db = get_db()
    db.execute(
        "UPDATE users SET password=? WHERE username=?",
        (generate_password_hash(password), username)
    )
    db.commit()

    return jsonify({"message": "Password updated"})

@bp.route('/api/users/<username>', methods=['DELETE'])
@auth.login_required
@admin_required
def delete_user(username):
    db = get_db()
    db.execute("DELETE FROM users WHERE username=?", (username,))
    db.commit()

    return jsonify({"message": "User deleted"})
