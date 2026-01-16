from fastapi import FastAPI
from core.database import engine, Base
from .routers import router

# Ստեղծում ենք բազան
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Միացնում ենք մեր Router-ը
app.include_router(router, prefix="/api")

@app.get("/")
def home():
    return {"message": "Welcome to BelleAme API"}