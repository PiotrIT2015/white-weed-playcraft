import time
import random
import json
from typing import List, Optional, Dict, Any

from characters import Player
from api.schemas import GameState, NPCState, Position, PlayerAction, DisabilityType, DisabilitySeverity
from ai.grok_agent import get_npc_dialogue # Import funkcji AI

# --- Konfiguracja Początkowa Scen ---
# W realnej grze ładowane z plików konfiguracyjnych/bazy danych
SCENE_CONFIG = {
    "home": {
        "npcs": [
            {"id": "npc_family_member_1", "name": "Członek rodziny", "position": {"x": 200, "y": 100}, "action": "idle", "attitude": 0.8}
        ],
        "objects": [
            {"id": "bed", "position": {"x": 50, "y": 20}, "state": "made"},
            {"id": "door_exit", "position": {"x": 380, "y": 290}, "state": "closed", "target_scene": "street"},
        ],
        "bounds": (0, 0, 400, 300)
    },
    "street": {
         "npcs": [
            {"id": "npc_stranger_1", "name": "Przechodzień", "position": {"x": 100, "y": 500}, "action": "walking", "attitude": 0.0},
            {"id": "npc_stranger_2", "name": "Inny przechodzień", "position": {"x": 600, "y": 200}, "action": "walking", "attitude": 0.1},
         ],
         "objects": [
             {"id": "door_home", "position": {"x": 50, "y": 50}, "state": "closed", "target_scene": "home"},
             {"id": "bus_stop", "position": {"x": 700, "y": 550}, "state": "waiting"},
         ],
         "bounds": (0, 0, 800, 600)
     },
    # Dodaj inne sceny (szkoła, praca, etc.)
}

class GameStateManager:
    """Zarządza całym stanem i logiką gry."""
    _instance = None # Dla wzorca Singleton (nadal nie idealne dla web)

    def __new__(cls, *args, **kwargs):
        # Prosty singleton, aby trzymać jeden stan gry (tylko dla demo!)
        if not cls._instance:
            cls._instance = super(GameStateManager, cls).__new__(cls)
            # Inicjalizacja tylko przy pierwszym tworzeniu
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.player: Optional[Player] = None
        self.current_scene_id: str = "limbo" # Stan przed inicjalizacją
        self.npcs: List[NPCState] = []
        self.interactive_objects: List[Dict[str, Any]] = []
        self.world_bounds: tuple = (0, 0, 100, 100) # Domyślne granice
        self.game_time_seconds: float = 8 * 3600 # Start o 8:00
        self.last_update_time: float = time.time()
        self._initialized = True
        print("GameStateManager initialized.")

    def _update_game_time(self):
        """Aktualizuje czas w grze."""
        now = time.time()
        delta_real_time = now - self.last_update_time
        # Przyspieszenie czasu gry (np. 1 sekunda rzeczywista = 1 minuta w grze)
        game_time_factor = 60
        self.game_time_seconds += delta_real_time * game_time_factor
        self.last_update_time = now

        # Ogranicz czas do 24h cyklu
        self.game_time_seconds %= (24 * 3600)

    def _get_formatted_game_time(self) -> str:
        """Zwraca czas w formacie HH:MM."""
        hours = int(self.game_time_seconds // 3600)
        minutes = int((self.game_time_seconds % 3600) // 60)
        return f"{hours:02d}:{minutes:02d}"

    def _load_scene(self, scene_id: str):
        """Ładuje konfigurację sceny."""
        if scene_id not in SCENE_CONFIG:
            print(f"Error: Scene '{scene_id}' not found in config.")
            # Można wrócić do sceny domyślnej lub rzucić błąd
            scene_id = "home" # Wróć do domu w razie problemu

        config = SCENE_CONFIG[scene_id]
        self.current_scene_id = scene_id
        self.world_bounds = config.get("bounds", (0, 0, 800, 600))

        # Załaduj NPC (twórz nowe instancje Pydantic)
        self.npcs = [NPCState(**npc_data) for npc_data in config.get("npcs", [])]

        # Załaduj obiekty interaktywne
        self.interactive_objects = config.get("objects", [])

        # Ustaw gracza na pozycji startowej dla tej sceny (jeśli zdefiniowano)
        # W tym przykładzie pozycja gracza jest trwała, ale można by to zmienić
        # np. if 'start_pos' in config and self.player: self.player._state.position = Position(**config['start_pos'])

        print(f"Loaded scene: {scene_id}")

    def create_new_game(self, name: str, dtype: DisabilityType, dseverity: DisabilitySeverity):
        """Tworzy nową grę, inicjalizuje gracza i ładuje pierwszą scenę."""
        self.player = Player(name=name, disability_type=dtype, disability_severity=dseverity)
        self.game_time_seconds = 8 * 3600 # Reset czasu
        self.last_update_time = time.time()
        self._load_scene("home") # Zacznij w domu
        print(f"New game started for {self.player.name} in scene '{self.current_scene_id}'")

    def _find_npc_by_id(self, npc_id: str) -> Optional[NPCState]:
        """Znajduje NPC w bieżącej scenie po ID."""
        return next((npc for npc in self.npcs if npc.id == npc_id), None)

    def _find_object_by_id(self, obj_id: str) -> Optional[Dict[str, Any]]:
         """Znajduje obiekt interaktywny w bieżącej scenie po ID."""
         return next((obj for obj in self.interactive_objects if obj.get("id") == obj_id), None)

    def _simulate_npcs(self, delta_time: float):
        """Prosta symulacja zachowania NPC."""
        for npc in self.npcs:
            if npc.current_action == "walking":
                # Prosty ruch w losowym kierunku (z ograniczeniem granic)
                move_speed = 30 # Pixeli na sekundę (w czasie gry)
                dx = random.uniform(-1, 1) * move_speed * delta_time
                dy = random.uniform(-1, 1) * move_speed * delta_time
                new_x = max(self.world_bounds[0], min(npc.position.x + dx, self.world_bounds[2]))
                new_y = max(self.world_bounds[1], min(npc.position.y + dy, self.world_bounds[3]))
                npc.position.x = new_x
                npc.position.y = new_y

                # Szansa na zmianę akcji
                if random.random() < 0.05:
                    npc.current_action = "idle"
            elif npc.current_action == "idle":
                 # Szansa na rozpoczęcie chodzenia
                 if random.random() < 0.1:
                     npc.current_action = "walking"
            # Resetuj dialog po pewnym czasie bez interakcji
            if npc.current_dialogue and random.random() < 0.02: # Mała szansa na reset w każdej klatce
                 npc.current_dialogue = None


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
                # Koszt ruchu jest już obliczany w player.move
                success = True
                message = "Gracz się poruszył."
            else:
                message = "Brak kierunku ruchu."
                success = False # Nie wykonano akcji

        elif action_type == "wait":
            # Czekanie regeneruje staminę
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

                # Wywołaj AI, aby uzyskać odpowiedź NPC
                # player_message w tym przypadku jest None, bo to gracz inicjuje
                ai_response = get_npc_dialogue(current_game_state, npc, player_message=None)
                npc.current_dialogue = ai_response

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
                     # Można ustawić nową pozycję gracza w nowej scenie
                     # self.player._state.position = new_start_pos
                     success = True
                     message = f"Przechodzisz do sceny: {target_scene}."
                 elif obj_id == "bed":
                      # Odpoczynek w łóżku regeneruje więcej staminy
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
        # Symuluj NPC - delta_time tutaj jest uproszczeniem, normalnie byłby to czas od ostatniej klatki
        self._simulate_npcs(delta_time=0.1) # Załóżmy stały mały krok czasowy dla symulacji NPC

        return success, message


    def get_current_state(self) -> Optional[GameState]:
        """Zbiera i zwraca aktualny stan gry."""
        if not self.player:
            return None

        # Pobierz aktualny stan gracza (uwzględniając modyfikatory)
        player_state = self.player.get_state()

        # Stwórz obiekt stanu gry
        gs = GameState(
            current_scene=self.current_scene_id,
            game_time=self._get_formatted_game_time(),
            player=player_state,
            npcs=[npc.copy(deep=True) for npc in self.npcs], # Zwróć kopie
            interactive_objects=[obj for obj in self.interactive_objects], # Zwróć listę (można by kopie)
            world_effects=[] # Zacznij z pustą listą efektów
        )

        # Zastosuj efekty niepełnosprawności do globalnego stanu gry
        gs = self.player.disability_handler.apply_world_effects(gs)

        return gs

    def load_state_from_dict(self, state_data: dict) -> bool:
        """Ładuje stan gry ze słownika (np. z JSON z bazy danych)."""
        try:
            # Użyj Pydantic do walidacji i sparsowania stanu
            loaded_state = GameState.parse_obj(state_data)

            # Odtwórz gracza
            self.player = Player(
                name=loaded_state.player.name,
                disability_type=loaded_state.player.disability_type,
                disability_severity=loaded_state.player.disability_severity
            )
            # Przywróć szczegółowy stan gracza (pozycję, staminę itp.)
            self.player._state = loaded_state.player.copy(deep=True)

            # Załaduj scenę, NPC i obiekty
            self.current_scene_id = loaded_state.current_scene
            # Uwaga: Ładowanie sceny nadpisze NPC/obiekty z konfiguracji.
            # Jeśli chcemy zachować stan NPC/obiektów z zapisu, musimy pominąć
            # ładowanie ich z SCENE_CONFIG i użyć tych z loaded_state.
            # Poniżej wersja używająca stanu z zapisu:
            scene_config = SCENE_CONFIG.get(self.current_scene_id, {})
            self.world_bounds = scene_config.get("bounds", (0, 0, 800, 600)) # Granice ze sceny
            self.npcs = loaded_state.npcs
            self.interactive_objects = loaded_state.interactive_objects

            # Przywróć czas gry
            try:
                time_parts = loaded_state.game_time.split(':')
                hours = int(time_parts[0])
                minutes = int(time_parts[1])
                self.game_time_seconds = hours * 3600 + minutes * 60
            except Exception:
                print(f"Warning: Could not parse game time '{loaded_state.game_time}'. Resetting to 8:00.")
                self.game_time_seconds = 8 * 3600

            self.last_update_time = time.time() # Zresetuj czas ostatniej aktualizacji
            self._initialized = True # Upewnij się, że jest zainicjalizowany

            print(f"Game state loaded successfully for {self.player.name} in scene '{self.current_scene_id}'.")
            return True

        except Exception as e:
            print(f"Error loading game state from dict: {e}")
            # W przypadku błędu, zresetuj stan do początkowego
            self.__init__() # Użyj __init__ do resetu (ostrożnie z singletonem)
            self._initialized = False # Reset flagi
            return False

# --- Utworzenie instancji Singletona ---
game_manager = GameStateManager()