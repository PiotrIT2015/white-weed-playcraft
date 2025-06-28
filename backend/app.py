#
# ... (wszystkie Twoje importy pozostają bez zmian)
#
from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
from sqlalchemy.orm import Session
import json

from engine.game_state_manager import game_manager
from api.schemas import PlayerAction, DisabilityType, DisabilitySeverity, GameState
from database.database import SessionLocal, engine, Base
import database.crud
import database.models

app = Flask(__name__, static_folder='../frontend/build', static_url_path='/')
CORS(app)


# --- Funkcja pomocnicza do pobierania sesji DB ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- ZMIANA 1: Usuwamy dekorator @app.before_first_request ---
# Ta funkcja będzie teraz wywoływana ręcznie na starcie serwera.
def create_db_tables():
    print("Creating database tables if they don't exist...")
    # Ta komenda jest idempotentna - nie zrobi nic, jeśli tabele już istnieją.
    Base.metadata.create_all(bind=engine)
    print("Database tables created/verified.")


# --- ZMIANA 2: Usuwamy dekorator @app.before_first_request ---
# Ta funkcja również będzie wywoływana ręcznie.
def initialize_game_state():
    """Wczytuje stan gry z ostatniego zapisu lub tworzy nową grę."""
    print("Initializing game state...")
    db = next(get_db())  # Pobierz sesję DB
    last_save = crud.get_all_saves(db, limit=1)  # Spróbuj pobrać ostatni zapis

    if last_save:
        try:
            success = game_manager.load_state_from_dict(last_save[0].game_state_json)
            if success:
                print(f"Loaded game state from save ID: {last_save[0].id}, Character: {last_save[0].character_name}")
            else:
                print("Failed to load game state from database. Starting new game.")
                game_manager.create_new_game(name="Gracz", disability_type=DisabilityType.WHEELCHAIR,
                                             disability_severity=DisabilitySeverity.MODERATE)
        except Exception as e:
            print(f"Error loading saved game from DB: {e}. Starting new game.")
            game_manager.create_new_game(name="Gracz", disability_type=DisabilityType.WHEELCHAIR,
                                         disability_severity=DisabilitySeverity.MODERATE)
    else:
        print("No existing game saves found. Starting a new game.")
        game_manager.create_new_game(name="Gracz", disability_type=DisabilityType.WHEELCHAIR,
                                     disability_severity=DisabilitySeverity.MODERATE)

    print("Game state initialization complete.")


#
# ... (wszystkie Twoje @app.route(...) pozostają bez zmian)
#
@app.route('/api/gamestate', methods=['GET'])
def get_gamestate():
    # ... (bez zmian)
    current_state = game_manager.get_current_state()
    if current_state:
        return jsonify(current_state.dict())
    return jsonify({"error": "Game not initialized"}), 500


@app.route('/api/action', methods=['POST'])
def process_player_action():
    # ... (bez zmian)
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
    # ... (bez zmian)
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
    # ... (bez zmian)
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
    # ... (bez zmian)
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
    # ... (bez zmian)
    db = next(get_db())
    success = crud.delete_save(db, save_id)
    if success:
        return jsonify({"success": True, "message": f"Save game with ID {save_id} deleted successfully."})
    else:
        return jsonify(
            {"success": False, "message": f"Failed to delete save game with ID {save_id}. Not found or error."}), 404


@app.route('/')
def serve():
    """Serwuje plik index.html dla frontendu."""
    return send_from_directory(app.static_folder, 'index.html')


# --- ZMIANA 3: Wywołujemy funkcje inicjalizacyjne tutaj ---
def initialize_app(flask_app):
    """Scentralizowana funkcja do inicjalizacji aplikacji."""
    with flask_app.app_context():
        create_db_tables()
        initialize_game_state()


if __name__ == '__main__':
    # Wywołaj inicjalizację PRZED uruchomieniem serwera
    initialize_app(app)

    # Uruchom aplikację Flask
    # 'use_reloader=False' jest ważne, jeśli chcesz uniknąć podwójnego wykonania
    # funkcji inicjalizacyjnych podczas pracy z `debug=True`.
    # Jeśli chcesz zachować automatyczne przeładowywanie, zostaw jak było, ale
    # miej świadomość, że kod inicjalizacyjny wykona się dwa razy.
    app.run(port=5000, debug=True, use_reloader=False)