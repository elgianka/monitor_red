import os
import sys

# Add the api directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'api')))

from api.db.session import engine, Base, SessionLocal
from api.models import host, alert, user, categoria, marca, modelo, estado, proceso, sede, token, responsable, ubicacion, monitoreo
from api.security import get_password_hash

def create_db_and_admin_user():
    print("Attempting to create database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created (if they didn't exist).")

    db = SessionLocal()
    try:
        admin_user = db.query(user.UserDB).filter(user.UserDB.nom_usuario == "admin").first()
        known_good_hash = "$5$rounds=535000$4x6cT92.uGgblWa7$brEv.a/5RBcxut/zk1OqaTpHgruCARaPwqb.QMGvPc9"

        if not admin_user:
            print("Creating default 'admin' user.")
            new_admin = user.UserDB(
                nom_usuario="admin",
                password_hash=known_good_hash,
                rol="ADMIN"
            )
            db.add(new_admin)
            db.commit()
            print("Admin user created successfully.")
        else:
            print("Admin user already exists. Updating password for consistency.")
            admin_user.password_hash = known_good_hash
            db.commit()
            print("Admin user password updated successfully.")
    except Exception as e:
        db.rollback()
        print(f"ERROR during admin user creation/update: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_db_and_admin_user()
