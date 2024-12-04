from fastapi import FastAPI
from src.api import router
from src.database import init_db
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Datenbank initialisieren
init_db()

# API-Router registrieren
app.include_router(router)

# CORS-Konfiguration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Alternativ: ["http://127.0.0.1:5500"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Mount the uploads directory to serve static files
app.mount("/uploads", StaticFiles(directory="src/uploads"), name="uploads")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="127.0.0.1", port=8000, reload=True)
