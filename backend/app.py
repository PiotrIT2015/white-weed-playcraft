#
# ... (wszystkie Twoje importy pozostają bez zmian)
#
from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
from sqlalchemy.orm import Session
import os # Upewnij się, że 'os' jest zaimportowany
import json

from engine.game_state_manager import game_manager
from api.schemas import PlayerAction, DisabilityType, DisabilitySeverity, GameState
from database.database import SessionLocal, engine, Base
import database.crud
import database.models

### ZMIANA 1: Poprawiamy konfigurację serwowania plików statycznych ###
# Wskazujemy Flaskowi, gdzie znajdują się pliki JS/CSS, a nie cała aplikacja.
# URL '/static' będzie teraz mapowany na folder 'frontend/build/static'.
# To standardowa i bardziej niezawodna konfiguracja.
BUILD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend', 'build'))
app = Flask(__name__, static_folder=os.path.join(BUILD_FOLDER, 'static'), static_url_path='/static')

CORS(app)

# --- Funkcja pomocnicza do pobierania sesji DB ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Twoje funkcje inicjalizacyjne (pozostają bez zmian, są bardzo dobre!) ---
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
                game_manager.create_new_game(name="Gracz", disability_type=DisabilityType.WHEELCHAIR, disability_severity=DisabilitySeverity.MODERATE)
        except Exception as e:
            print(f"Error loading saved game from DB: {e}. Starting new game.")
            game_manager.create_new_game(name="Gracz", disability_type=DisabilityType.WHEELCHAIR, disability_severity=DisabilitySeverity.MODERATE)
    else:
        print("No existing game saves found. Starting a new game.")
        game_manager.create_new_game(name="Gracz", disability_type=DisabilityType.WHEELCHAIR, disability_severity=DisabilitySeverity.MODERATE)
    
    print("Game state initialization complete.")


#
# ==========================================================
# ===                 ENDPOINTY API (BEZ ZMIAN)          ===
# ==========================================================
# Twoje endpointy API są dobrze napisane i nie wymagają zmian.
# Wszystkie trasy zaczynające się od /api/ będą działać jak dotychczas.
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
        import traceback
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
        import traceback
        traceback.print_exc()
        db.rollback()
        return jsonify({"error": f"Failed to save game: {e}"}), 500

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
        import traceback
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

### ZMIANA 2: Dodajemy uniwersalną trasę (catch-all) dla frontendu ###
# Ta trasa musi znajdować się PO wszystkich trasach API.
# Przechwyci ona wszystkie pozostałe żądania (np. '/', '/saves', '/game')
# i zwróci główny plik `index.html`. React Router po stronie klienta
# zajmie się resztą i wyświetli odpowiedni widok.
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

# Twoja logika inicjalizacyjna jest świetna - zachowujemy ją!
def initialize_app(flask_app):
    """Scentralizowana funkcja do inicjalizacji aplikacji."""
    with flask_app.app_context():
        create_db_tables()
        initialize_game_state()

if __name__ == '__main__':
    initialize_app(app)
    
    # Uruchomienie aplikacji pozostaje bez zmian.
    # use_reloader=False jest tutaj kluczowe, aby uniknąć podwójnej inicjalizacji.
    app.run(port=5000, debug=True, use_reloader=False)