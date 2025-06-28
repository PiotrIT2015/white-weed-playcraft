@ECHO OFF
TITLE Game Launcher

ECHO --- Instalowanie zaleznosci backendu (Python) ---
python -m pip install Flask Flask-Cors
IF %ERRORLEVEL% NEQ 0 (
    ECHO.
    ECHO !!! Blad podczas instalacji zaleznosci Pythona. Sprawdz, czy Python i pip sa poprawnie zainstalowane.
    PAUSE
    EXIT /B 1
)

ECHO.
ECHO --- Instalowanie zaleznosci frontendu (React) ---
IF NOT EXIST "frontend\node_modules" (
    ECHO Katalog 'node_modules' nie istnieje. Rozpoczynanie instalacji...
    PUSHD frontend
    npm install
    IF %ERRORLEVEL% NEQ 0 (
        ECHO.
        ECHO !!! Blad podczas uruchamiania 'npm install'. Sprawdz, czy Node.js i npm sa poprawnie zainstalowane.
        POPD
        PAUSE
        EXIT /B 1
    )
    POPD
) ELSE (
    ECHO Zaleznosci frontendu juz zainstalowane.
)

ECHO.
ECHO --- Budowanie aplikacji React ---
PUSHD frontend
npm run build
IF %ERRORLEVEL% NEQ 0 (
    ECHO.
    ECHO !!! Blad podczas uruchamiania 'npm run build'.
    POPD
    PAUSE
    EXIT /B 1
)
POPD

ECHO.
ECHO --- Uruchamianie serwera backendu ---
REM Uruchamia serwer Pythona w tle. /D ustawia katalog roboczy dla procesu.
REM Serwer zostanie automatycznie zamkniety po zamknieciu tego okna konsoli.
START "Flask Backend Server" /D "backend" /B python app.py

ECHO Serwer uruchomiony. Oczekiwanie na start...
REM Czeka 3 sekundy, ukrywajac odliczanie ( > NUL )
TIMEOUT /T 3 /NOBREAK > NUL

SET "URL=http://localhost:5000"
ECHO --- Otwieranie gry w przegladarce pod adresem: %URL% ---
START %URL%

ECHO.
ECHO Gra jest uruchomiona. Aby zakonczyc, zamknij to okno konsoli.
PAUSE