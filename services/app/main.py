from fastapi import FastAPI
from app.routes import requerimientos

app = FastAPI(title="Requerimientos Service")

app.include_router(requerimientos.router, prefix="/requerimientos", tags=["Requerimientos"])
