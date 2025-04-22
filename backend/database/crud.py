from sqlalchemy.orm import Session
from typing import List, Optional
import json
from datetime import datetime

from . import models
from api import schemas

def create_game_save(db: Session, game_state: schemas.GameState, save_name: str) -> models.GameSave:
    """Zapisuje obiekt GameState Pydantic do bazy danych."""
    if not game_state:
        raise ValueError("Cannot save an empty game state")

    # Serializuj cały obiekt GameState do słownika JSON
    # Użyj Pydantic .dict() zamiast .json() dla kompatybilności z SQLAlchemy JSON type
    game_state_dict = game_state.dict()

    db_save = models.GameSave(
        character_name=game_state.player.name,
        # Użyj .value do zapisania wartości enumów jako stringów w bazie
        disability_type=game_state.player.disability_type.value,
        disability_severity=game_state.player.disability_severity.value,
        save_name=save_name,
        game_state_json=game_state_dict, # Zapisz słownik
        # saved_at jest zarządzane przez default/onupdate w modelu
    )
    db.add(db_save)
    db.commit()
    db.refresh(db_save)
    print(f"Game saved successfully with ID: {db_save.id} for character {db_save.character_name}")
    return db_save

def get_game_save(db: Session, save_id: int) -> Optional[models.GameSave]:
    """Pobiera zapis gry (obiekt SQLAlchemy) z bazy danych po ID."""
    print(f"Attempting to retrieve save game with ID: {save_id}")
    save = db.query(models.GameSave).filter(models.GameSave.id == save_id).first()
    if save:
        print(f"Found save game: {save.save_name}")
    else:
        print(f"Save game with ID {save_id} not found.")
    return save


def get_all_saves(db: Session, skip: int = 0, limit: int = 100) -> List[models.GameSave]:
    """Pobiera listę wszystkich zapisów (obiekty SQLAlchemy) z paginacją."""
    print(f"Retrieving all saves, skip={skip}, limit={limit}")
    saves = db.query(models.GameSave).order_by(models.GameSave.saved_at.desc()).offset(skip).limit(limit).all()
    print(f"Found {len(saves)} saves.")
    return saves

def delete_save(db: Session, save_id: int) -> bool:
    """Usuwa zapis gry po ID."""
    db_save = get_game_save(db, save_id)
    if db_save:
        print(f"Deleting save game with ID: {save_id}")
        db.delete(db_save)
        db.commit()
        print("Save game deleted successfully.")
        return True
    print(f"Could not delete: Save game with ID {save_id} not found.")
    return False