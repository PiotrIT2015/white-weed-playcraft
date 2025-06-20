from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
from sqlalchemy.orm import Session
import json # Do ewentualnego zapisu/odczytu JSON dla debugowania

# Importujemy instancję menedżera stanu gry
from game_state_manager import game_manager
# Importujemy schematy Pydantic do walidacji danych wejściowych
from api.schemas import PlayerAction, DisabilityType, DisabilitySeverity, GameStateResponse
# Importujemy funkcje CRUD i obiekty bazy danych
from database.database import SessionLocal, engine, Base
import database.crud
import database.models # Musi być zaimportowany, aby SQLAlchemy "zobaczyło" modele i stworzyło tabele

app = Flask(__name__, static_folder='../frontend/build', static_url_path='/')
CORS(app)

# --- Funkcja pomocnicza do pobierania sesji DB ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Utwórz tabele w bazie danych przy starcie aplikacji (tylko w celach deweloperskich!) ---
# W środowisku produkcyjnym używałbyś narzędzi do migracji baz danych (np. Alembic)
@app.before_first_request
def create_db_tables():
    print("Creating database tables if they don't exist...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created.")

# --- Inicjalizacja Gry ---
# Przy starcie aplikacji, zamiast zawsze tworzyć nową grę,
# możemy spróbować załadować ostatni zapis lub domyślny
@app.before_first_request
def initialize_game_state():
    db = next(get_db()) # Pobierz sesję DB
    last_save = crud.get_all_saves(db, limit=1) # Spróbuj pobrać ostatni zapis

    if last_save:
        try:
            # game_manager.load_state_from_dict oczekuje słownika
            # game_state_json jest już słownikiem dzięki Column(JSON)
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


@app.route('/api/gamestate', methods=['GET'])
def get_gamestate():
    """Zwraca aktualny stan gry."""
    current_state = game_manager.get_current_state()
    if current_state:
        # Użyj GameStateResponse.from_orm(current_state) jeśli chcesz dodatkową walidację/filtrowanie
        # LUB po prostu current_state.dict() jeśli GameState jest już gotowe
        return jsonify(current_state.dict())
    return jsonify({"error": "Game not initialized"}), 500

@app.route('/api/action', methods=['POST'])
def process_player_action():
    """Przetwarza akcje gracza (ruch, interakcja, rozmowa itp.)."""
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
        traceback.print_exc() # Wydrukuj pełny traceback dla debugowania
        return jsonify({"error": f"Invalid action data or server error: {e}"}), 400

---
### Nowe Endpoints dla Zarządzania Zapisami Gry
---

@app.route('/api/saves', methods=['POST'])
def save_game():
    """Zapisuje aktualny stan gry do bazy danych."""
    db = next(get_db()) # Pobierz sesję DB
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
        db.rollback() # Wycofaj transakcję w przypadku błędu
        return jsonify({"error": f"Failed to save game: {e}"}), 500

@app.route('/api/saves', methods=['GET'])
def get_all_game_saves():
    """Pobiera listę wszystkich dostępnych zapisów gry."""
    db = next(get_db()) # Pobierz sesję DB
    saves = crud.get_all_saves(db)
    
    # Przekształć obiekty SQLAlchemy na słowniki dla JSON
    # Nie przesyłamy całego game_state_json w liście, by nie obciążać sieci
    # wysyłamy tylko metadata
    saves_list = []
    for s in saves:
        saves_list.append({
            "id": s.id,
            "saveName": s.save_name,
            "characterName": s.character_name,
            "disabilityType": s.disability_type,
            "disabilitySeverity": s.disability_severity,
            "savedAt": s.saved_at.isoformat() # Format daty ISO 8601
        })
    return jsonify(saves_list)

@app.route('/api/saves/<int:save_id>', methods=['GET'])
def load_game_by_id(save_id: int):
    """Ładuje konkretny zapis gry po ID i ustawia go jako bieżący stan."""
    db = next(get_db()) # Pobierz sesję DB
    db_save = crud.get_game_save(db, save_id)
    
    if not db_save:
        return jsonify({"error": f"Save game with ID {save_id} not found."}), 404

    try:
        # game_state_json jest już słownikiem
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
    """Usuwa zapis gry po ID."""
    db = next(get_db()) # Pobierz sesję DB
    success = crud.delete_save(db, save_id)
    
    if success:
        return jsonify({"success": True, "message": f"Save game with ID {save_id} deleted successfully."})
    else:
        return jsonify({"success": False, "message": f"Failed to delete save game with ID {save_id}. Not found or error."}), 404

@app.route('/')
def serve():
    """Serwuje plik index.html dla frontendu."""
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    # Uruchom aplikację Flask na porcie 5000
    # W trybie debugowania, Flask może dwukrotnie uruchomić create_db_tables
    # co jest normalnym zachowaniem, ale warto o tym wiedzieć.
    app.run(port=5000, debug=True)