from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from core.database import engine, Base
from .routers import router

# Ստեղծում ենք բազան
Base.metadata.create_all(bind=engine)

app = FastAPI(title="BelleAme", description="Հարսանյաց հրավիրատոմսերի կայք")

# Static ֆայլեր (CSS, images)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Միացնում ենք Router-ը ՄԻԱՅՆ ՄԵԿ ԱՆԳԱՄ
app.include_router(router)

@app.get("/health")
def health_check():
    return {"status": "healthy", "app": "BelleAme API"}