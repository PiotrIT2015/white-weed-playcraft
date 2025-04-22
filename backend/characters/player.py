from api.schemas import PlayerState, Position, DisabilityType, DisabilitySeverity
from disabilities import create_disability_handler, BaseDisability # Importuj fabrykę

class Player:
    """Reprezentuje postać gracza w grze."""

    def __init__(self, name: str, disability_type: DisabilityType, disability_severity: DisabilitySeverity):
        self.name = name
        # Inicjalizacja stanu początkowego - można by to ładować z konfiguracji sceny
        self._state = PlayerState(
            name=name,
            position=Position(x=50.0, y=50.0), # Przykładowa pozycja startowa
            disability_type=disability_type,
            disability_severity=disability_severity,
            stamina=100.0,
            perception_modifier={} # Pusty słownik na start
        )
        self.disability_handler: BaseDisability = create_disability_handler(disability_type, disability_severity)
        self._update_state_from_disability() # Zastosuj modyfikatory od razu

    def _update_state_from_disability(self):
        """Wewnętrzna metoda do aktualizacji stanu gracza przez handler niepełnosprawności."""
        self._state = self.disability_handler.apply_player_modifiers(self._state)

    def get_state(self) -> PlayerState:
        """Zwraca aktualny stan gracza jako obiekt Pydantic."""
        # Upewnij się, że stan jest aktualny przed zwróceniem
        self._update_state_from_disability()
        # Zwróć kopię, aby zapobiec modyfikacjom z zewnątrz
        return self._state.copy(deep=True)

    def apply_action_effects(self, action_cost: float = 1.0):
         """Redukuje staminę po wykonaniu akcji."""
         # Koszt może zależeć od akcji i modyfikatorów
         self._state.stamina -= action_cost
         self._state.stamina = max(0, self._state.stamina)

    def move(self, dx: float, dy: float, world_bounds: tuple = (0, 0, 800, 600)):
        """Przesuwa gracza, uwzględniając modyfikator prędkości i granice świata."""
        # Pobierz aktualny stan (w tym modyfikator prędkości)
        current_state = self.get_state()
        speed = current_state.current_speed_modifier

        # Oblicz nowy potencjalny x i y
        new_x = self._state.position.x + dx * speed
        new_y = self._state.position.y + dy * speed

        # Sprawdź granice świata (proste prostokątne ograniczenie)
        min_x, min_y, max_x, max_y = world_bounds
        self._state.position.x = max(min_x, min(new_x, max_x))
        self._state.position.y = max(min_y, min(new_y, max_y))

        # Akcja ruchu kosztuje staminę
        move_cost = (abs(dx) + abs(dy)) * 0.1 # Przykładowy koszt bazowy
        self.apply_action_effects(move_cost)

        print(f"Player {self.name} moved to ({self._state.position.x:.1f}, {self._state.position.y:.1f}) with speed mod {speed:.2f}. Stamina: {self._state.stamina:.1f}")

    def rest(self, duration: float = 1.0):
        """Odpoczynek regeneruje staminę."""
        regen_rate = 5.0 # Punktów staminy na jednostkę czasu
        self._state.stamina += regen_rate * duration
        self._state.stamina = min(100, self._state.stamina) # Stamina max 100
        print(f"Player {self.name} rested. Stamina: {self._state.stamina:.1f}")

    # Można dodać metody interact(), talk() itp. jeśli logika interakcji gracza ma być tutaj