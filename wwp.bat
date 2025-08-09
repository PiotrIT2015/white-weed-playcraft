@echo off
REM =================================================================
REM == Skrypt do uruchamiania gry (Backend i Frontend)             ==
REM =================================================================
ECHO Uruchamianie serwera Backend (Python/Flask)...

REM Przejdz do folderu backendu
cd backend

REM Uruchom backend w nowym oknie konsoli
REM Aktywuje srodowisko wirtualne 'venv' i uruchamia serwer Flask
REM start "Backend Server" cmd /c "call venv\Scripts\activate.bat && flask run"

start "Flask Backend Server" /D "backend" /B python app.py

REM Wroc do glownego folderu
cd ..

REM =================================================================
ECHO.
ECHO Uruchamianie serwera Frontend (React)...
ECHO Poczekaj chwile, to moze potrwac...

REM Przejdz do folderu frontendu
cd frontend

REM Uruchom frontend w nowym oknie konsoli
start "Frontend Server" cmd /c "npm start"

REM =================================================================
ECHO.
ECHO Oba serwery zostaly uruchomione w osobnych oknach.
ECHO Aby zatrzymac, zamknij oba okna konsoli.
PAUSE


