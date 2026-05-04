#!/usr/bin/env python3
import sqlite3
import argparse
from werkzeug.security import generate_password_hash

DB_PATH = "./data/eneverre.db"


def get_conn():
    return sqlite3.connect(DB_PATH)


def list_users():
    conn = get_conn()
    cur = conn.cursor()

    rows = cur.execute("SELECT username, role FROM users").fetchall()

    for r in rows:
        print(f"{r[0]} ({r[1]})")

    conn.close()

def create_user(username, password, role):
    if role not in ("admin", "user"):
        print("Invalid role")
        return

    conn = get_conn()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            (username, generate_password_hash(password), role)
        )
        conn.commit()
        print("User created")
    except sqlite3.IntegrityError:
        print("User already exists")

    conn.close()


def change_password(username, password):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        "UPDATE users SET password=? WHERE username=?",
        (generate_password_hash(password), username)
    )

    if cur.rowcount == 0:
        print("User not found")
    else:
        conn.commit()
        print("Password updated")

    conn.close()


def change_role(username, role):
    if role not in ("admin", "user"):
        print("Invalid role")
        return

    conn = get_conn()
    cur = conn.cursor()

    if role == "user":
        count = cur.execute(
            "SELECT COUNT(*) FROM users WHERE role='admin'"
        ).fetchone()[0]

        current_role = cur.execute(
            "SELECT role FROM users WHERE username=?",
            (username,)
        ).fetchone()

        if current_role and current_role[0] == "admin" and count <= 1:
            print("Cannot remove last admin")
            return

    cur.execute(
        "UPDATE users SET role=? WHERE username=?",
        (role, username)
    )

    if cur.rowcount == 0:
        print("User not found")
    else:
        conn.commit()
        print("Role updated")

    conn.close()


def delete_user(username):
    conn = get_conn()
    cur = conn.cursor()

    role = cur.execute(
        "SELECT role FROM users WHERE username=?",
        (username,)
    ).fetchone()

    if not role:
        print("User not found")
        return

    if role[0] == "admin":
        count = cur.execute(
            "SELECT COUNT(*) FROM users WHERE role='admin'"
        ).fetchone()[0]

        if count <= 1:
            print("Cannot delete last admin")
            return

    cur.execute("DELETE FROM users WHERE username=?", (username,))
    conn.commit()

    print("User deleted")

    conn.close()


parser = argparse.ArgumentParser(description="Manage users")

sub = parser.add_subparsers(dest="cmd")

sub.add_parser("list")

create = sub.add_parser("create")
create.add_argument("username")
create.add_argument("password")
create.add_argument("--fullname", default=None)
create.add_argument("--role", default="user")

passwd = sub.add_parser("passwd")
passwd.add_argument("username")
passwd.add_argument("password")

role = sub.add_parser("role")
role.add_argument("username")
role.add_argument("role")

delete = sub.add_parser("delete")
delete.add_argument("username")

args = parser.parse_args()

if args.cmd == "list":
    list_users()

elif args.cmd == "create":
    create_user(args.username, args.password, args.role)

elif args.cmd == "passwd":
    change_password(args.username, args.password)

elif args.cmd == "role":
    change_role(args.username, args.role)

elif args.cmd == "delete":
    delete_user(args.username)

else:
    parser.print_help()
