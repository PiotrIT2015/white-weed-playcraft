from characters.player import Player
from api.schemas import GameState, NPCState, Position, PlayerAction, DisabilityType, DisabilitySeverity
from typing import List, Optional
import json
from ai.grok_agent import get_npc_dialogue # <--- Kluczowy import!

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

    def process_action(self, action: PlayerAction) -> tuple[bool, str]:
        """Przetwarza akcję gracza i zwraca (success, message)."""
        if not self.player:
            return False, "Gra nie została zainicjowana."

        success = False
        message = "Nieznana akcja lub błąd."
        action_cost = 0.5 # Domyślny koszt akcji dla staminy

        action_type = action.action_type.lower()
        details = action.details or {}
        target_id = action.target_id

        # --- Obsługa Akcji ---
        if action_type == "move":
            dx = details.get("dx", 0.0)
            dy = details.get("dy", 0.0)
            if dx != 0 or dy != 0:
                self.player.move(dx, dy, self.world_bounds)
                success = True
                message = "Gracz się poruszył."
            else:
                message = "Brak kierunku ruchu."
                success = False # Nie wykonano akcji

        elif action_type == "wait":
            duration = details.get("duration", 1.0) # Domyślnie czekaj 1 jednostkę czasu
            self.player.rest(duration)
            action_cost = 0 # Odpoczynek nie kosztuje staminy
            success = True
            message = f"Gracz odpoczął przez {duration} jednostek czasu."

        elif action_type == "talk":
            if not target_id: return False, "Nie wybrano celu rozmowy."
            npc = self._find_npc_by_id(target_id)
            if npc:
                # Sprawdź dystans (prosty przykład)
                player_pos = self.player.get_state().position
                dist_sq = (player_pos.x - npc.position.x)**2 + (player_pos.y - npc.position.y)**2
                talk_range_sq = 50**2 # Zasięg rozmowy (do kwadratu)
                if dist_sq > talk_range_sq:
                    return False, f"Jesteś za daleko od {npc.name}, aby rozmawiać."

                print(f"Initiating talk with {npc.name} (ID: {target_id})")
                npc.current_action = "talking" # NPC się zatrzymuje, by rozmawiać

                # Pobierz aktualny stan gry dla kontekstu AI
                current_game_state = self.get_current_state()
                if not current_game_state: return False, "Błąd pobierania stanu gry dla AI."

                # --- TUTAJ NASTĘPUJE INTEGRACJA Z AGENTEM GROK-1 ---
                # player_message w tym przypadku jest None, bo to gracz inicjuje rozmowę
                # W przyszłości, jeśli gracz będzie mógł wpisywać tekst, przekazesz go tutaj
                ai_response = get_npc_dialogue(current_game_state, npc, player_message=None)
                npc.current_dialogue = ai_response # Aktualizuj dialog NPC

                action_cost = 0.2 # Rozmowa lekko męczy
                success = True
                message = f"Rozpoczęto rozmowę z {npc.name}. Odpowiedź: {npc.current_dialogue}"
            else:
                message = f"Nie znaleziono postaci o ID '{target_id}' w tej scenie."

        elif action_type == "interact":
            if not target_id: return False, "Nie wybrano celu interakcji."
            target_object = self._find_object_by_id(target_id)
            if target_object:
                # Sprawdź dystans
                player_pos = self.player.get_state().position
                obj_pos = Position(**target_object.get("position", {"x":0, "y":0}))
                dist_sq = (player_pos.x - obj_pos.x)**2 + (player_pos.y - obj_pos.y)**2
                interact_range_sq = 30**2
                if dist_sq > interact_range_sq:
                    return False, f"Jesteś za daleko od obiektu '{target_object.get('id', 'N/A')}'."

                # Logika interakcji (bardzo prosty przykład)
                obj_id = target_object.get("id")
                obj_state = target_object.get("state")
                target_scene = target_object.get("target_scene")

                interaction_modifier = self.player.disability_handler.get_interaction_modifier(obj_id or "generic")
                action_cost = 1.0 * interaction_modifier # Koszt zależy od trudności interakcji

                if "door" in obj_id and target_scene:
                    print(f"Player interacts with door {obj_id} leading to {target_scene}")
                    self._load_scene(target_scene)
                    success = True
                    message = f"Przechodzisz do sceny: {target_scene}."
                elif obj_id == "bed":
                    self.player.rest(duration=5.0) # Dłuższy odpoczynek
                    target_object["state"] = "used"
                    action_cost = 0 # Sam odpoczynek nie męczy
                    success = True
                    message = "Odpocząłeś w łóżku, regenerując siły."
                else:
                    message = f"Interakcja z '{obj_id}' ({obj_state}) - brak zdefiniowanej akcji."
                    action_cost = 0.1 # Mały koszt za próbę interakcji

            else:
                message = f"Nie znaleziono obiektu interaktywnego o ID '{target_id}'."

        else:
            message = f"Nieznany typ akcji: '{action_type}'"

        # Zastosuj koszt akcji, jeśli była udana
        if success:
            self.player.apply_action_effects(action_cost)

        # Po każdej akcji gracza, zaktualizuj stan świata (czas, NPC)
        self._update_game_time()
        self._simulate_npcs(delta_time=0.1) # Załóżmy stały mały krok czasowy dla symulacji NPC

        return success, message

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