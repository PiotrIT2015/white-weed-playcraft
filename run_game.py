import os
import subprocess
import webbrowser
import time
import sys

def install_dependencies():
    """Instaluje zależności dla backendu i frontendu."""
    print("--- Instalowanie zależności backendu (Python) ---")
    subprocess.run([sys.executable, "-m", "pip", "install", "Flask", "Flask-Cors"], check=True)
    
    print("\n--- Instalowanie zależności frontendu (React) ---")
    frontend_dir = os.path.join(os.path.dirname(__file__), 'frontend')
    if not os.path.exists(os.path.join(frontend_dir, 'node_modules')):
        subprocess.run("npm install", shell=True, cwd=frontend_dir, check=True)
    else:
        print("Zależności frontendu już zainstalowane.")

def build_react_app():
    """Buduje aplikację React do statycznych plików."""
    print("\n--- Budowanie aplikacji React ---")
    frontend_dir = os.path.join(os.path.dirname(__file__), 'frontend')
    subprocess.run("npm run build", shell=True, cwd=frontend_dir, check=True)

def run_game():
    """Uruchamia backend i otwiera grę w przeglądarce."""
    install_dependencies()
    build_react_app()
    
    print("\n--- Uruchamianie serwera backendu ---")
    backend_script = os.path.join('backend', 'main.py')
    # Użycie Popen do uruchomienia serwera w tle
    server_process = subprocess.Popen([sys.executable, backend_script])
    
    print("Serwer uruchomiony. Oczekiwanie na start...")
    time.sleep(3) # Daj serwerowi chwilę na start

    url = "http://localhost:5000"
    print(f"--- Otwieranie gry w przeglądarce pod adresem: {url} ---")
    webbrowser.open(url)
    
    print("\nGra jest uruchomiona. Aby zakończyć, zamknij to okno konsoli.")
    
    try:
        # Czekaj na zakończenie procesu serwera (np. przez zamknięcie konsoli)
        server_process.wait()
    except KeyboardInterrupt:
        print("\n--- Zamykanie serwera ---")
        server_process.terminate()

if __name__ == '__main__':
    run_game()