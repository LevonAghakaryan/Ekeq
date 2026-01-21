from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from core.database import engine, Base
from app.routers import main_router

# Ստեղծում ենք բազան
Base.metadata.create_all(bind=engine)

app = FastAPI(title="BelleAme", description="Հարսանյաց հրավիրատոմսերի կայք")

# Static ֆայլեր (CSS, images)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Միացնում ենք բոլոր router-ները
app.include_router(main_router)

@app.get("/health")
def health_check():
    return {"status": "healthy", "app": "BelleAme API"}