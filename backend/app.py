#
# ... (wszystkie Twoje importy pozostają bez zmian)
#
from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
from sqlalchemy.orm import Session
import os 
import json
import traceback # Dodaj ten import do lepszego logowania błędów

from engine.game_state_manager import game_manager
# Upewnij się, że Enumy są poprawnie importowane, aby można było ich użyć
from api.schemas import PlayerAction, DisabilityType, DisabilitySeverity, GameState 
from database.database import SessionLocal, engine, Base
from database import crud
from database import models

# Konfiguracja serwowania plików statycznych pozostaje bez zmian
BUILD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend', 'build'))
app = Flask(__name__, static_folder=os.path.join(BUILD_FOLDER, 'static'), static_url_path='/static')

CORS(app)

# Funkcja pomocnicza do pobierania sesji DB pozostaje bez zmian
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Funkcje inicjalizacyjne pozostają bez zmian
def create_db_tables():
    print("Creating database tables if they don't exist...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created/verified.")

def initialize_game_state():
    """Wczytuje stan gry z ostatniego zapisu lub tworzy nową grę."""
    print("Initializing game state...")
    db = next(get_db())
    last_save = crud.get_all_saves(db, limit=1)

    if last_save:
        try:
            success = game_manager.load_state_from_dict(last_save[0].game_state_json)
            if success:
                print(f"Loaded game state from save ID: {last_save[0].id}, Character: {last_save[0].character_name}")
            else:
                print("Failed to load game state from database. Starting new game.")
                game_manager.create_new_game(name="Gracz", dtype=DisabilityType.NEUROLOGICAL, dseverity=DisabilitySeverity.MODERATE)
        except Exception as e:
            print(f"Error loading saved game from DB: {e}. Starting new game.")
            game_manager.create_new_game(name="Gracz", dtype=DisabilityType.NEUROLOGICAL, dseverity=DisabilitySeverity.MODERATE)
    else:
        print("No existing game saves found. Starting a new game.")
        game_manager.create_new_game(name="Gracz", dtype=DisabilityType.NEUROLOGICAL, dseverity=DisabilitySeverity.MODERATE)
    
    print("Game state initialization complete.")


# ==========================================================
# ===                 ENDPOINTY API                      ===
# ==========================================================

# ==========================================================
# ===  NOWY KOD: ENDPOINT DO TWORZENIA NOWEJ GRY         ===
# ==========================================================
@app.route('/api/new-game', methods=['POST'])
def start_new_game():
    """
    Tworzy nową grę na podstawie danych z frontendu (imię, typ i stopień niepełnosprawności).
    """
    db = next(get_db())
    data = request.get_json()

    if not data or 'characterName' not in data or 'disabilityType' not in data or 'disabilitySeverity' not in data:
        return jsonify({'error': 'Brakujące dane: characterName, disabilityType, disabilitySeverity'}), 400

    try:
        # Pobranie danych z żądania
        name = data['characterName']
        # Konwersja stringów z JSON na członków Enum z Twoich schematów
        # Zakładamy, że wartości z frontendu (np. "vision") odpowiadają nazwom w Enum (np. VISION)
        # metoda .upper() zapewni dopasowanie
        disability_type_str = data['disabilityType'].upper()
        severity_str = data['disabilitySeverity'].upper()
        
        dtype = DisabilityType[disability_type_str]
        dseverity = DisabilitySeverity[severity_str]

        # Użyj swojego menedżera gry do stworzenia nowej instancji gry
        game_manager.create_new_game(name=name, dtype=dtype, dseverity=dseverity)
        
        # Pobierz nowo utworzony stan gry
        current_state = game_manager.get_current_state()
        if not current_state:
            return jsonify({"error": "Nie udało się zainicjować stanu gry."}), 500
            
        # Opcjonalnie, ale zalecane: stwórz pierwszy zapis gry od razu
        # To sprawi, że nowa gra będzie od razu widoczna w zapisach.
        save_name = f"Początek gry - {current_state.player.name}"
        db_save = crud.create_game_save(db, current_state, save_name)

        return jsonify({
            "success": True,
            "message": f"Nowa gra rozpoczęta dla postaci {name}.",
            "gameState": current_state.dict(),
            "saveId": db_save.id # Zwróć ID zapisu, może się przydać
        }), 201

    except KeyError as e:
        # Ten błąd wystąpi, jeśli wartość z frontendu nie pasuje do żadnego członka Enum
        return jsonify({"error": f"Nieprawidłowa wartość dla niepełnosprawności lub jej stopnia: {e}"}), 400
    except Exception as e:
        traceback.print_exc()
        db.rollback()
        return jsonify({"error": f"Wewnętrzny błąd serwera podczas tworzenia gry: {e}"}), 500

#
# ... (reszta Twoich endpointów API, np. /api/gamestate, /api/action, pozostaje BEZ ZMIAN) ...
#
@app.route('/api/gamestate', methods=['GET'])
def get_gamestate():
    current_state = game_manager.get_current_state()
    if current_state:
        return jsonify(current_state.dict())
    return jsonify({"error": "Game not initialized"}), 500

@app.route('/api/action', methods=['POST'])
def process_player_action():
    if not game_manager.player:
        return jsonify({"error": "Game not initialized. Cannot process action."}), 400
    try:
        action_data = request.json
        player_action = PlayerAction(**action_data)
        success, message = game_manager.process_action(player_action)
        current_state = game_manager.get_current_state()
        if current_state:
            return jsonify({
                "success": success,
                "message": message,
                "gameState": current_state.dict()
            })
        else:
            return jsonify({"error": "Failed to retrieve updated game state."}), 500
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": f"Invalid action data or server error: {e}"}), 400

@app.route('/api/saves', methods=['POST'])
def save_game():
    db = next(get_db())
    save_name = request.json.get('save_name', f"QuickSave-{game_manager._get_formatted_game_time()}")
    current_game_state = game_manager.get_current_state()
    if not current_game_state:
        return jsonify({"error": "No game state to save."}), 400
    try:
        db_save = crud.create_game_save(db, current_game_state, save_name)
        return jsonify({
            "success": True,
            "message": f"Game saved successfully as '{db_save.save_name}' (ID: {db_save.id}).",
            "saveId": db_save.id,
            "savedAt": db_save.saved_at.isoformat()
        }), 201
    except Exception as e:
        traceback.print_exc()
        db.rollback()
        return jsonify({"error": f"Failed to save game: {e}"}), 500

# ... (wszystkie pozostałe endpointy GET i DELETE /api/saves) ...

@app.route('/api/saves', methods=['GET'])
def get_all_game_saves():
    db = next(get_db())
    saves = crud.get_all_saves(db)
    saves_list = []
    for s in saves:
        saves_list.append({
            "id": s.id,
            "saveName": s.save_name,
            "characterName": s.character_name,
            "disabilityType": s.disability_type,
            "disabilitySeverity": s.disability_severity,
            "savedAt": s.saved_at.isoformat()
        })
    return jsonify(saves_list)

@app.route('/api/saves/<int:save_id>', methods=['GET'])
def load_game_by_id(save_id: int):
    db = next(get_db())
    db_save = crud.get_game_save(db, save_id)
    if not db_save:
        return jsonify({"error": f"Save game with ID {save_id} not found."}), 404
    try:
        success = game_manager.load_state_from_dict(db_save.game_state_json)
        if success:
            current_state = game_manager.get_current_state()
            return jsonify({
                "success": True,
                "message": f"Game loaded successfully from '{db_save.save_name}' (ID: {db_save.id}).",
                "gameState": current_state.dict() if current_state else {}
            })
        else:
            return jsonify({"error": "Failed to load game state from selected save."}), 500
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": f"Error processing saved game data: {e}"}), 500

@app.route('/api/saves/<int:save_id>', methods=['DELETE'])
def delete_game_save(save_id: int):
    db = next(get_db())
    success = crud.delete_save(db, save_id)
    if success:
        return jsonify({"success": True, "message": f"Save game with ID {save_id} deleted successfully."})
    else:
        return jsonify({"success": False, "message": f"Failed to delete save game with ID {save_id}. Not found or error."}), 404

# ==========================================================
# ===      SERWOWANIE APLIKACJI FRONTENDOWEJ (REACT)     ===
# ==========================================================
# Ta sekcja pozostaje bez zmian
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react_app(path):
    if path != "" and os.path.exists(os.path.join(BUILD_FOLDER, path)):
        return send_from_directory(BUILD_FOLDER, path)
    else:
        return send_from_directory(BUILD_FOLDER, 'index.html')


# ==========================================================
# ===           URUCHOMIENIE APLIKACJI                   ===
# ==========================================================
# Ta sekcja pozostaje bez zmian
def initialize_app(flask_app):
    """Scentralizowana funkcja do inicjalizacji aplikacji."""
    with flask_app.app_context():
        create_db_tables()
        initialize_game_state()

if __name__ == '__main__':
    initialize_app(app)
    app.run(port=5000, debug=True, use_reloader=False)