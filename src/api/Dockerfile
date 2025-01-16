# Basis-Image
FROM python:3.10-slim

# Arbeitsverzeichnis setzen
WORKDIR /app

# Systemabhängigkeiten installieren
RUN apt-get update && apt-get install -y git && apt-get clean

# Abhängigkeiten kopieren und installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Projektdateien kopieren
COPY . .

# Port 8000 für FastAPI freigeben
EXPOSE 8000

# Startbefehl für die API-Anwendung
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
