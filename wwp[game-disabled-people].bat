@echo off
REM =================================================================
REM == Skrypt do uruchamiania gry (Backend i Frontend)             ==
REM =================================================================

REM Ustawiamy zmienna %SCRIPT_DIR% na katalog, w ktorym znajduje sie ten skrypt.
REM Dzieki temu, niezaleznie skad uruchomisz skrypt, sciezki beda poprawne.
set "SCRIPT_DIR=%~dp0"

ECHO Uruchamianie serwera Backend (Python/Flask)...

REM Uruchom backend w nowym oknie konsoli i utrzymuj je otwarte (/k),
REM aby zobaczyc ewentualne bledy.
REM Najpierw przejdz do katalogu backendu, a potem uruchom aplikacje Python.
REM Usunieto odwolanie do venv\Scripts\activate.bat
start "Flask Backend Server" cmd /k "cd /d "%SCRIPT_DIR%backend" && python app.py && echo. && echo Backend uruchomiony. Nacisnij dowolny klawisz, aby kontynuowac... && pause"

ECHO.
ECHO Uruchamianie serwera Frontend (React)...
ECHO Poczekaj chwile, to moze potrwac...

REM Uruchom frontend w nowym oknie konsoli i utrzymuj je otwarte (/k),
REM aby zobaczyc ewentualne bledy.
REM Najpierw przejdz do katalogu frontendu, a potem uruchom aplikacje React.
start "Frontend Server" cmd /k "cd /d "%SCRIPT_DIR%frontend" && npm start && echo. && echo Frontend uruchomiony. Nacisnij dowolny klawisz, aby kontynuowac... && pause"

ECHO.
ECHO Oba serwery zostaly uruchomione w osobnych oknach.
ECHO Aby zatrzymac, zamknij oba okna konsoli.
PAUSE



