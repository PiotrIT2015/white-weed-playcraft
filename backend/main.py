from fastapi import FastAPI
from database import database
from api import routes as api_routes
import time

# --- Inicjalizacja Bazy Danych ---
# Spróbuj zainicjalizować połączenie i tabele przy starcie
# Odczekaj chwilę, jeśli baza danych startuje w kontenerze Docker
MAX_RETRIES = 5
RETRY_DELAY = 3 # sekundy

for attempt in range(MAX_RETRIES):
    try:
        print(f"Attempting to initialize database (attempt {attempt + 1}/{MAX_RETRIES})...")
        database.init_db() # Ta funkcja teraz zawiera try-except i logowanie
        print("Database connection successful.")
        break # Wyjdź z pętli, jeśli się udało
    except Exception as e:
        print(f"Database initialization failed: {e}")
        if attempt < MAX_RETRIES - 1:
            print(f"Retrying in {RETRY_DELAY} seconds...")
            time.sleep(RETRY_DELAY)
        else:
            print("Max retries reached. Could not connect to the database. Application might not work correctly.")
            # Można zdecydować o zatrzymaniu aplikacji:
            # import sys
            # sys.exit("Critical error: Database connection failed.")

# --- Konfiguracja Aplikacji FastAPI ---
app = FastAPI(
    title="Empatia: Symulator Codzienności - Backend API",
    description="API do zarządzania stanem gry, postaciami, interakcjami i AI.",
    version="0.2.0", # Podniesiona wersja
    docs_url="/api/docs", # Przeniesienie dokumentacji pod /api/docs
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Dołącz router z endpointami gry
app.include_router(api_routes.router) # Prefix /api jest już ustawiony w routerze

# Główny endpoint dla sprawdzenia działania
@app.get("/", tags=["Root"], summary="Sprawdź status API")
async def read_root():
    """Zwraca prostą wiadomość potwierdzającą działanie API."""
    return {"message": "Witaj w API gry 'Empatia: Symulator Codzienności'!"}

# --- Uruchomienie serwera (dla celów deweloperskich) ---
if __name__ == "__main__":
    import uvicorn
    print("Starting Uvicorn development server on http://localhost:8000")
    # Użyj host="0.0.0.0", aby był dostępny z zewnątrz (np. z kontenera Docker lub innej maszyny w sieci)
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="info")