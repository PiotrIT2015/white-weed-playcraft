from characters.player import Player
from api.schemas import GameState, NPCState, Position, PlayerAction, DisabilityType, DisabilitySeverity
from typing import List, Optional
import json

# --- Symulacja NPC ---
# W rzeczywistości to pochodziłoby z konfiguracji sceny/poziomu
INITIAL_NPCS = [
    NPCState(id="npc_teacher_1", name="Nauczyciel", position=Position(x=10.0, y=5.0), current_action="idle"),
    NPCState(id="npc_student_1", name="Kolega z klasy", position=Position(x=2.0, y=8.0), current_action="walking"),
]

class GameStateManager:
    """
    Uproszczony manager stanu gry.
    UWAGA: Użycie globalnej instancji tego managera jest złym pomysłem w
    aplikacjach wielodostępnych. Lepszym podejściem byłoby zarządzanie
    stanem per sesja użytkownika lub gra. Dla celów demonstracyjnych jest OK.
    """
    def __init__(self):
        self.player: Optional[Player] = None
        self.npcs: List[NPCState] = []
        self.current_scene: str = "character_creation" # Początkowy stan

    def create_new_game(self, name: str, dtype: DisabilityType, dseverity: DisabilitySeverity):
        self.player = Player(name=name, disability_type=dtype, disability_severity=dseverity)
        self.current_scene = "home" # Przejście do pierwszej sceny
        self.npcs = [npc.copy(deep=True) for npc in INITIAL_NPCS] # Skopiuj początkowych NPC
        print(f"New game created for {name} with {dseverity} {dtype}")

    def process_action(self, action: PlayerAction):
        if not self.player:
            print("Error: Player not initialized.")
            return

        print(f"Processing action: {action.action_type}")
        if action.action_type == "move":
            details = action.details or {}
            dx = details.get("dx", 0.0)
            dy = details.get("dy", 0.0)
            self.player.move(dx, dy)
        elif action.action_type == "talk":
            npc_id = action.target_id
            npc = next((n for n in self.npcs if n.id == npc_id), None)
            if npc:
                print(f"Player talks to {npc.name} (ID: {npc_id})")
                # Tutaj nastąpiłaby integracja z AI (Grok-1)
                # context = f"Scena: {self.current_scene}. Gracz ({self.player.name}, {self.player.disability_severity} {self.player.disability_type}) podchodzi do {npc.name}. Co mówi {npc.name}?"
                # response_text = ai.grok_agent.get_npc_response(context, npc.id) # Wywołanie AI
                # npc.current_dialogue = response_text # Aktualizacja stanu NPC
                npc.current_dialogue = f"{npc.name}: Cześć {self.player.name}! Miło cię widzieć." # Placeholder
            else:
                print(f"Error: NPC with id {npc_id} not found.")
        # Dodaj obsługę innych akcji (interact, use_item, etc.)

        # Prosta symulacja ruchu NPC (placeholder)
        for npc in self.npcs:
             if npc.current_action == "walking":
                 npc.position.x += 0.1 # Np. prosty ruch w prawo

    def get_current_state(self) -> Optional[GameState]:
        if not self.player:
            return None

        # Zastosuj efekty niepełnosprawności do stanu gry
        # (modyfikuje stan gracza i może dodać globalne efekty)
        current_player_state = self.player.get_state()

        # Utwórz obiekt stanu gry
        gs = GameState(
            current_scene=self.current_scene,
            player=current_player_state,
            npcs=self.npcs,
            world_effects=[] # Początkowo puste
        )

        # Pozwól handlerowi niepełnosprawności zmodyfikować stan gry
        gs = self.player.disability_handler.apply_effects(gs)

        return gs

    def load_state_from_json(self, state_json: dict):
        """Ładuje stan gry z obiektu JSON (np. z bazy danych)."""
        try:
            loaded_state = GameState.parse_obj(state_json)
            # Odtwórz gracza
            self.player = Player(
                name=loaded_state.player.name,
                disability_type=loaded_state.player.disability_type,
                disability_severity=loaded_state.player.disability_severity
            )
            self.player.position = loaded_state.player.position
            # Odtwórz NPC
            self.npcs = loaded_state.npcs
            self.current_scene = loaded_state.current_scene
            print(f"Game state loaded successfully for {self.player.name}")
            return True
        except Exception as e:
            print(f"Error loading game state: {e}")
            # Przywróć stan początkowy lub obsłuż błąd inaczej
            self.__init__() # Reset do stanu początkowego
            return False

# --- Globalna instancja managera stanu ---
# UWAGA: To jest uproszczenie na potrzeby przykładu.
# W rzeczywistej aplikacji stan powinien być zarządzany inaczej
# (np. per request, per user session).
game_manager = GameStateManager()