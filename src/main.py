from fastapi import FastAPI
from src.api import router  # Importiere den Router statt app

# Hauptanwendung erstellen
main_app = FastAPI()

# API-Routen aus src.api direkt registrieren
main_app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:main_app", host="127.0.0.1", port=8000, reload=True)
