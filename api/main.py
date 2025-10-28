from fastapi import FastAPI
from .routers import hosts, alerts, auth, categorias, marcas, modelos, estados, procesos, sedes

app = FastAPI(
    title="API de Monitoreo de Red",
    description="API para la gestión y monitoreo de equipos de red.",
    version="0.1.0",
)

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
