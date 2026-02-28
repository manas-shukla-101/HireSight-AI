import hashlib
import sqlite3

from database import create_connection, create_tables
from werkzeug.security import check_password_hash, generate_password_hash


def register_user(username, password, role="user"):
    username = (username or "").strip()
    if not username or not password:
        return False, "Username and password are required."

    conn = create_connection()
    try:
        conn.execute(
            "INSERT INTO users (username, password, role, created_at) VALUES (?, ?, ?, CURRENT_TIMESTAMP)",
            (username, generate_password_hash(password), role),
        )
        conn.commit()
        return True, "Account created successfully."
    except Exception:
        return False, "Username already exists."
    finally:
        conn.close()


def login_user(username, password):
    username = (username or "").strip()
    create_tables()

    for _ in range(2):
        conn = create_connection()
        try:
            row = conn.execute(
                "SELECT username, password, role FROM users WHERE username = ?",
                (username,),
            ).fetchone()

            if not row:
                return None

            stored_hash = row["password"] or ""
            valid = False

            # New format (werkzeug): e.g. scrypt:...$salt$hash
            if "$" in stored_hash:
                valid = check_password_hash(stored_hash, password)
            else:
                # Legacy format (old app): plain sha256 hex digest
                legacy = hashlib.sha256(password.encode()).hexdigest()
                valid = legacy == stored_hash
                if valid:
                    conn.execute(
                        "UPDATE users SET password = ? WHERE username = ?",
                        (generate_password_hash(password), username),
                    )
                    conn.commit()

            if valid:
                return {"username": row["username"], "role": row["role"]}
            return None
        except sqlite3.OperationalError:
            create_tables()
            continue
        finally:
            conn.close()

    return None


def ensure_admin_exists():
    conn = create_connection()
    try:
        # If an admin user already exists, do nothing.
        row = conn.execute("SELECT id FROM users WHERE role = 'admin' LIMIT 1").fetchone()
        if row:
            return

        # If username `admin` exists but is not admin, promote it.
        admin_user = conn.execute(
            "SELECT id FROM users WHERE username = ? LIMIT 1", ("admin",)
        ).fetchone()
        if admin_user:
            conn.execute("UPDATE users SET role = 'admin' WHERE id = ?", (admin_user["id"],))
        else:
            conn.execute(
                "INSERT INTO users (username, password, role, created_at) VALUES (?, ?, ?, CURRENT_TIMESTAMP)",
                ("admin", generate_password_hash("admin123"), "admin"),
            )
        conn.commit()
    finally:
        conn.close()
