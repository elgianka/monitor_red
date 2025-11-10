import sys
import os
from contextlib import asynccontextmanager

# Añadir el directorio raíz del proyecto al sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI, Depends
# Importamos la función de la sesión
from api.db.session import engine, Base, SessionLocal, get_db

# --- IMPORTACIONES DE MODELOS (CRÍTICAS PARA METADATA) ---
# Al ejecutar esta línea, todos los modelos se registran en Base.metadata.
# Esto es CRUCIAL para que create_all funcione correctamente y resuelva las claves foráneas.
from api.models import host, alert, user, categoria, marca, modelo, estado, proceso, sede, token, responsable, ubicacion, gerencia, area 

# --- OTRAS IMPORTACIONES ---
# CORRECCIÓN: Se usa 'get_password_hash', el nombre de función correcto de security.py
from api.security import get_password_hash 
# Los routers deben usar nombres PLURALES (hosts, alerts, etc.)
from api.routers import hosts, alerts, auth, categorias, marcas, modelos, estados, procesos, sedes, monitoreo, gerencias, areas, responsables, ubicaciones

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Crea las tablas si no existen y asegura que el usuario 'admin' esté presente.
    """
    print("INFO: Ejecutando inicialización de la base de datos en evento 'startup'...")
    
    # 1. Crea todas las tablas si no existen
    print("INFO: Forzando la recreación del esquema de la base de datos...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # 2. Crea el usuario 'admin' si no existe (AHORA HABILITADO)
    #    La creacion del usuario se habilita temporalmente aqui para asegurar
    #    que el usuario admin exista.
    try:
        db = SessionLocal()
        admin_user = db.query(user.UserDB).filter(user.UserDB.nom_usuario == "admin").first()
        
        # Usar siempre el hash pre-calculado para asegurar consistencia
        known_good_hash = "$5$rounds=535000$4x6cT92.uGgblWa7$brEv.a/5RBcxut/zk1OqaTpHgruCARaPwqb.QMGvPc9"

        if not admin_user:
            print("INFO: Creando usuario 'admin' por defecto.")
            new_admin = user.UserDB(
                nom_usuario="admin",
                password_hash=known_good_hash,
                rol="ADMIN"
            )
            db.add(new_admin)
            db.commit()
            print("INFO: Usuario 'admin' creado exitosamente.")
        else:
            print("INFO: Usuario 'admin' ya existe. Actualizando su contraseña para asegurar consistencia.")
            admin_user.password_hash = known_good_hash
            db.commit()
            print("INFO: Contraseña del usuario 'admin' actualizada exitosamente.")

    except Exception as e:
        print(f"ERROR al inicializar la base de datos (CREATE/UPDATE USER): {e}")
        db.rollback()
    finally:
        db.close()
    
    yield
    # Cleanup logic here

app = FastAPI(
    title="API de Monitoreo de Red",
    description="API para la gestión y monitoreo de equipos de red.",
    version="0.1.0",
    lifespan=lifespan
)


# --- INCLUSIÓN DE ROUTERS ---

app.include_router(hosts.router, prefix="/api/v1")
app.include_router(alerts.router, prefix="/api/v1")
app.include_router(categorias.router, prefix="/api/v1")
app.include_router(marcas.router, prefix="/api/v1")
app.include_router(modelos.router, prefix="/api/v1")
app.include_router(estados.router, prefix="/api/v1")
app.include_router(procesos.router, prefix="/api/v1")
app.include_router(sedes.router, prefix="/api/v1")
app.include_router(monitoreo.router, prefix="/api/v1")
app.include_router(gerencias.router, prefix="/api/v1")
app.include_router(areas.router, prefix="/api/v1")
app.include_router(responsables.router, prefix="/api/v1")
app.include_router(ubicaciones.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1", tags=["Authentication"])

@app.get("/", tags=["Root"])
async def read_root():
    """
    Endpoint de bienvenida.
    """
    return {"message": "Bienvenido a la API de Monitoreo de Red"}
