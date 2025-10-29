from fastapi import FastAPI, Depends
# Importamos la función de la sesión
from .db.session import engine, Base, SessionLocal, get_db

# --- IMPORTACIONES DE MODELOS (CRÍTICAS PARA METADATA) ---
# Al ejecutar esta línea, todos los modelos se registran en Base.metadata.
# Esto es CRUCIAL para que create_all funcione correctamente y resuelva las claves foráneas.
from .models import host, alert, user, categoria, marca, modelo, estado, proceso, sede, token, responsable, ubicacion 

# --- OTRAS IMPORTACIONES ---
# CORRECCIÓN: Se usa 'get_password_hash', el nombre de función correcto de security.py
from .security import get_password_hash 
# Los routers deben usar nombres PLURALES (hosts, alerts, etc.)
from .routers import hosts, alerts, auth, categorias, marcas, modelos, estados, procesos, sedes 

app = FastAPI(
    title="API de Monitoreo de Red",
    description="API para la gestión y monitoreo de equipos de red.",
    version="0.1.0",
)


# --- LÓGICA DE INICIALIZACIÓN MOVILIZADA A EVENTO DE INICIO ---

@app.on_event("startup")
def startup_event_initialize_database():
    """
    Crea las tablas si no existen y asegura que el usuario 'admin' esté presente.
    """
    print("INFO: Ejecutando inicialización de la base de datos en evento 'startup'...")
    
    # 1. Crea todas las tablas si no existen
    Base.metadata.create_all(bind=engine)

    # 2. Crea el usuario 'admin' si no existe
    db = SessionLocal()
    try:
        # Busca si el usuario 'admin' existe (usando el nombre de tabla del SQL: TB_USUARIOS_DEL_SISTEMA)
        # Asumiendo que UserDB mapea a TB_USUARIOS_DEL_SISTEMA
        admin_user = db.query(user.UserDB).filter(user.UserDB.nom_usuario == "admin").first()
        
        if not admin_user:
            # Si no existe, lo crea
            print("INFO: Creando usuario 'admin' por defecto.")
            hashed_password = get_password_hash("admin") # Contraseña: "admin" 
            
            # Crear la instancia del modelo UserDB (Rol debe coincidir con tu esquema: 'ROL' no 'is_admin')
            new_admin = user.UserDB(
                nom_usuario="admin",
                nom_completo="Administrador del Sistema",
                password_hash=hashed_password,
                rol="ADMIN" # Asumiendo que el rol es 'ADMIN'
            )
            db.add(new_admin)
            db.commit()
            print("INFO: Usuario 'admin' creado exitosamente.")
        else:
            print("INFO: Usuario 'admin' ya existe. Omitiendo creación.")

    except Exception as e:
        # Si el error de Foreign Key persiste, el servidor no llegará a este punto.
        print(f"ERROR al inicializar la base de datos (CREATE USER): {e}")
    finally:
        db.close()


# --- INCLUSIÓN DE ROUTERS ---

app.include_router(hosts.router, prefix="/api/v1")
app.include_router(alerts.router, prefix="/api/v1")
app.include_router(categorias.router, prefix="/api/v1")
app.include_router(marcas.router, prefix="/api/v1")
app.include_router(modelos.router, prefix="/api/v1")
app.include_router(estados.router, prefix="/api/v1")
app.include_router(procesos.router, prefix="/api/v1")
app.include_router(sedes.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1", tags=["Authentication"])

@app.get("/", tags=["Root"])
async def read_root():
    """
    Endpoint de bienvenida.
    """
    return {"message": "Bienvenido a la API de Monitoreo de Red"}
