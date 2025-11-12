import os
import sys

# Add the api directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'api')))

from api.db.session import engine, Base, SessionLocal
from api.models.gerencia import GerenciaDB
from api.models.area import AreaDB
from api.models.responsable import ResponsableDB
from api.models.host import HostDB
from api.models.alert import AlertDB
from api.models.user import UserDB
from api.models.categoria import CategoriaDB
from api.models.marca import MarcaDB
from api.models.modelo import ModeloDB
from api.models.estado import EstadoDB
from api.models.proceso import ProcesoDB
from api.models.sede import SedeDB
from api.models.ubicacion import UbicacionDB
from api.models.monitoreo import MonitoreoDB
from api.security import get_password_hash

def create_db_and_admin_user():
    print("Attempting to create database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created (if they didn't exist).")

    db = SessionLocal()
    try:
        admin_user = db.query(UserDB).filter(UserDB.nom_usuario == "admin").first()
        
        hashed_password = get_password_hash("admin")

        if not admin_user:
            print("Creating default 'admin' user.")
            new_admin = UserDB(
                nom_usuario="admin",
                password_hash=hashed_password,
                rol="ADMIN"
            )
            db.add(new_admin)
            db.commit()
            print("Admin user created successfully.")
        else:
            print("Admin user already exists. Updating password for consistency.")
            admin_user.password_hash = hashed_password
            db.commit()
            print("Admin user password updated successfully.")
        
        print("\nAdmin user 'admin' with password 'admin' has been configured.")
        print("Please restart the API and try logging in again.")

    except Exception as e:
        db.rollback()
        print(f"ERROR during admin user creation/update: {e}")
    finally:
        db.close()

    # Add default sedes
    db = SessionLocal()
    try:
        sedes = db.query(SedeDB).all()
        if not sedes:
            print("Creating default 'sedes'.")
            default_sedes = [
                SedeDB(NOM_SEDE="Oficina Principal"),
                SedeDB(NOM_SEDE="Sucursal Norte"),
                SedeDB(NOM_SEDE="Sucursal Sur"),
            ]
            db.add_all(default_sedes)
            db.commit()
            print("Default sedes created successfully.")
        else:
            print("Sedes already exist.")
    except Exception as e:
        db.rollback()
        print(f"ERROR during sedes creation: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    create_db_and_admin_user()