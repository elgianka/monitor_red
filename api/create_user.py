import argparse
import sqlite3
import sys
import os

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from api.security import get_password_hash

def create_user(db_path, username, password, rol):
    """
    Creates a new user in the database.
    """
    password_hash = get_password_hash(password)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO TB_USUARIOS_DEL_SISTEMA (NOM_USUARIO, PASSWORD_HASH, ROL) VALUES (?, ?, ?)",
            (username, password_hash, rol),
        )
        conn.commit()
        print(f"User '{username}' created successfully.")
    except sqlite3.IntegrityError:
        print(f"Error: User '{username}' already exists.")
    finally:
        conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a new user.")
    parser.add_argument("username", type=str, help="The username.")
    parser.add_argument("password", type=str, help="The password.")
    parser.add_argument("--rol", type=str, default="user", help="The user's role.")
    parser.add_argument("--db-path", type=str, default="monitor_ping.db", help="The path to the database.")
    args = parser.parse_args()

    create_user(args.db_path, args.username, args.password, args.rol)
