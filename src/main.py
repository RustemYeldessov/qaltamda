import uvicorn
from fastapi import FastAPI
from src.database import engine, Base
from src.auth.router import router as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Qaltamda API")

app.include_router(auth_router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)