from fastapi import FastAPI
from auth import routes as authRoutes
from db.database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to the book app (still thinking of a name). visit /docs or /redocs for this api documentation"}

app.include_router(authRoutes.router)
