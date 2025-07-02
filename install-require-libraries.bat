@echo off
chcp 65001 > nul
pushd "%~dp0backend"
call pip install -r requirements.txt
popd
echo.
echo Instalacja zakończona. Naciśnij dowolny klawisz, aby kontynuować...
pause > nul