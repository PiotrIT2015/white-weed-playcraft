from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union
import enum
from datetime import datetime

# --- Enumy dla API ---
class DisabilityType(str, enum.Enum):
    VISION = "vision"
    HEARING = "hearing"
    MOBILITY = "mobility"
    NEUROLOGICAL = "neurological"
    EPILEPSY = "epilepsy"

class DisabilitySeverity(str, enum.Enum):
    MILD = "mild"
    MODERATE = "moderate"
    SEVERE = "severe"

# --- Podstawowe struktury danych ---
class Position(BaseModel):
    x: float = 0.0
    y: float = 0.0

# --- Stan postaci ---
class PlayerState(BaseModel):
    name: str
    position: Position
    disability_type: DisabilityType
    disability_severity: DisabilitySeverity
    # Modyfikatory wynikające bezpośrednio z aktualnego stanu i niepełnosprawności
    current_speed_modifier: float = 1.0
    perception_modifier: Dict[str, Any] = {} # Np. {'visual_acuity': 0.8, 'hearing_range': 0.7}
    stamina: float = 100.0 # Przykładowy dodatkowy atrybut

class NPCState(BaseModel):
    id: str # Unikalny identyfikator NPC w scenie
    name: str
    position: Position
    current_dialogue: Optional[str] = None
    current_action: str = "idle" # np. "walking", "talking", "idle", "interacting"
    # Można dodać nastawienie do gracza, cel itp.
    attitude_towards_player: float = 0.0 # np. od -1 (wrogi) do 1 (przyjazny)

# --- Ogólny stan gry ---
class GameState(BaseModel):
    current_scene: str # np. "home", "school_hallway", "office"
    game_time: str = "08:00" # Czas w grze
    player: PlayerState
    npcs: List[NPCState] = []
    # Efekty środowiskowe lub wynikające z niepełnosprawności, które frontend może interpretować
    world_effects: List[str] = [] # Np. ["visual_blur_mild", "background_noise_moderate", "trigger_epilepsy_warning"]
    interactive_objects: List[Dict[str, Any]] = [] # Np. [{'id': 'door1', 'position': {'x': 10, 'y': 20}, 'state': 'closed'}]

# --- Modele dla żądań API ---
class PlayerAction(BaseModel):
    action_type: str = Field(..., description="Typ akcji, np. 'move', 'interact', 'talk', 'wait'")
    target_id: Optional[str] = Field(None, description="ID obiektu lub NPC docelowego dla akcji")
    details: Optional[Dict[str, Any]] = Field(None, description="Dodatkowe szczegóły akcji, np. {'dx': 1, 'dy': 0} dla ruchu")

class CreateCharacterRequest(BaseModel):
    character_name: str = Field(..., min_length=1, max_length=100)
    disability_type: DisabilityType
    disability_severity: DisabilitySeverity

class SaveGameRequest(BaseModel):
    save_name: str = Field(default="ManualSave", max_length=100)

# --- Modele dla odpowiedzi API ---
class GameSaveInfo(BaseModel):
    id: int
    save_name: str
    character_name: str
    disability_type: DisabilityType # Zwracamy enumy API, nie DB
    disability_severity: DisabilitySeverity
    saved_at: datetime

    class Config:
        orm_mode = True # Pozwala Pydantic na odczyt danych z modeli SQLAlchemy

class ActionResponse(BaseModel):
    """Standardowa odpowiedź po wykonaniu akcji."""
    success: bool
    message: str
    new_game_state: Optional[GameState] = None # Zwracamy nowy stan gry po udanej akcji