from fastapi import APIRouter, Depends, HTTPException, Body, Path, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
import json # Do potencjalnej obsługi błędów JSON

from database import crud, models, database
from api import schemas
from engine import game_manager # Importuj singleton game_manager

router = APIRouter(prefix="/api", tags=["Game"])

# Zależność sesji DB
DbDep = Depends(database.get_db)

@router.post("/game/new",
             response_model=schemas.GameState,
             status_code=status.HTTP_201_CREATED,
             summary="Rozpocznij nową grę")
async def start_new_game(
    character_data: schemas.CreateCharacterRequest = Body(...)
):
    """
    Tworzy nową postać i inicjalizuje stan gry, zwracając początkowy stan.
    """
    print(f"Received request to start new game for: {character_data.character_name}")
    try:
        game_manager.create_new_game(
            name=character_data.character_name,
            dtype=character_data.disability_type,
            dseverity=character_data.disability_severity
        )
    except Exception as e:
        print(f"Error during game creation: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to initialize game: {e}")

    current_state = game_manager.get_current_state()
    if not current_state:
         print("Error: Game state is null after creation.")
         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to retrieve game state after initialization")
    print("New game started, returning initial state.")
    return current_state

@router.get("/game/state",
            response_model=schemas.GameState,
            summary="Pobierz aktualny stan gry")
async def get_current_game_state():
    """
    Zwraca pełny, aktualny stan gry (pozycja gracza, NPC, scena, itp.).
    """
    state = game_manager.get_current_state()
    if not state:
        # Jeśli gra nie jest aktywna (np. przed /new lub po błędzie ładowania)
        print("Warn: Request for game state when no game is active.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No active game found. Start a new game or load a save.")
    # print("Returning current game state.") # Można odkomentować do debugowania
    return state

@router.post("/game/action",
             # Zwraca teraz ActionResponse zamiast całego stanu dla optymalizacji
             response_model=schemas.ActionResponse,
             summary="Wykonaj akcję gracza")
async def perform_player_action(action: schemas.PlayerAction = Body(...)):
    """
    Przetwarza akcję gracza (ruch, interakcja, rozmowa) i zwraca wynik oraz nowy stan gry.
    """
    print(f"Received action: {action.action_type}, Target: {action.target_id}, Details: {action.details}")
    if not game_manager.player:
         print("Error: Action received but no active player.")
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Game not active. Start or load a game first.")

    try:
        success, message = game_manager.process_action(action)
    except Exception as e:
        print(f"Error processing action {action.action_type}: {e}")
        # W środowisku produkcyjnym logować pełny traceback
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error processing action: {e}")

    print(f"Action result: Success={success}, Message='{message}'")

    if success:
        new_state = game_manager.get_current_state()
        if not new_state:
             print("Error: Failed to get game state after successful action.")
             # To nie powinno się zdarzyć, ale lepiej obsłużyć
             raise HTTPException(status_code=500, detail="Internal error retrieving state after action.")
        return schemas.ActionResponse(success=True, message=message, new_game_state=new_state)
    else:
        # Dla nieudanej akcji zwracamy tylko informację, bez stanu gry
        return schemas.ActionResponse(success=False, message=message, new_game_state=None)


@router.post("/game/save",
             response_model=schemas.GameSaveInfo,
             status_code=status.HTTP_201_CREATED,
             summary="Zapisz grę")
async def save_current_game(
    save_request: schemas.SaveGameRequest = Body(...),
    db: Session = DbDep
):
    """Zapisuje aktualny stan gry do bazy danych."""
    current_state = game_manager.get_current_state()
    if not current_state:
        print("Error: Attempt to save game when no state is active.")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No active game state to save.")

    print(f"Saving game with name: {save_request.save_name}")
    try:
        db_save = crud.create_game_save(db=db, game_state=current_state, save_name=save_request.save_name)
        # Konwertuj obiekt SQLAlchemy na schemat Pydantic przed zwróceniem
        save_info = schemas.GameSaveInfo.from_orm(db_save)
        print(f"Game saved successfully (ID: {save_info.id}).")
        return save_info
    except Exception as e:
        print(f"Error saving game to database: {e}")
        db.rollback() # Wycofaj transakcję w razie błędu
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Could not save game state: {e}")

@router.get("/game/load/{save_id}",
            response_model=schemas.GameState,
            summary="Wczytaj zapisaną grę")
async def load_saved_game(
    save_id: int = Path(..., title="ID zapisu do wczytania", ge=1),
    db: Session = DbDep
):
    """Wczytuje stan gry z podanego ID zapisu."""
    print(f"Request to load game with ID: {save_id}")
    db_save = crud.get_game_save(db=db, save_id=save_id)
    if db_save is None:
        print(f"Error: Save game ID {save_id} not found in database.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Game save with id {save_id} not found.")

    # game_state_json powinien być już słownikiem dzięki SQLAlchemy JSON type
    if not isinstance(db_save.game_state_json, dict):
         print(f"Error: Saved game state for ID {save_id} is not a valid JSON object (type: {type(db_save.game_state_json)}).")
         # Spróbujmy sparsować, jeśli to string
         try:
              game_state_data = json.loads(db_save.game_state_json)
              if not isinstance(game_state_data, dict): raise ValueError("Parsed data is not a dict")
         except (json.JSONDecodeError, TypeError, ValueError) as e:
               print(f"Error parsing saved game state data: {e}")
               raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to parse saved game state data.")
    else:
        game_state_data = db_save.game_state_json

    # Załaduj stan do managera gry
    success = game_manager.load_state_from_dict(game_state_data)
    if not success:
        print(f"Error: Game manager failed to load state from save ID {save_id}.")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to load game state into manager.")

    loaded_state = game_manager.get_current_state()
    if not loaded_state:
         print("Error: Game state is null after successful load.")
         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Game manager failed to provide state after load.")

    print(f"Game ID {save_id} loaded successfully.")
    return loaded_state

@router.get("/game/saves",
            response_model=List[schemas.GameSaveInfo],
            summary="Lista zapisanych gier")
async def list_saved_games(
    db: Session = DbDep,
    skip: int = Query(0, ge=0, title="Liczba rekordów do pominięcia"),
    limit: int = Query(10, ge=1, le=100, title="Maksymalna liczba rekordów do zwrócenia")
):
    """Zwraca listę dostępnych zapisów gry, posortowaną od najnowszych."""
    print(f"Request to list saves: skip={skip}, limit={limit}")
    saves_orm = crud.get_all_saves(db, skip=skip, limit=limit)
    # Konwertuj listę obiektów SQLAlchemy na listę schematów Pydantic
    saves_info = [schemas.GameSaveInfo.from_orm(s) for s in saves_orm]
    print(f"Returning {len(saves_info)} save game records.")
    return saves_info

@router.delete("/game/save/{save_id}",
               status_code=status.HTTP_204_NO_CONTENT,
               summary="Usuń zapis gry")
async def delete_saved_game(
    save_id: int = Path(..., title="ID zapisu do usunięcia", ge=1),
    db: Session = DbDep
):
    """Usuwa zapis gry o podanym ID."""
    print(f"Request to delete save game with ID: {save_id}")
    deleted = crud.delete_save(db=db, save_id=save_id)
    if not deleted:
        print(f"Error: Failed to delete save game ID {save_id} (not found).")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Game save with id {save_id} not found.")
    print(f"Save game ID {save_id} deleted successfully.")
    # Status 204 No Content nie powinien zwracać ciała odpowiedzi
    return None