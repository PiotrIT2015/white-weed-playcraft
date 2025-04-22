from abc import ABC, abstractmethod
from api.schemas import GameState, DisabilitySeverity, PlayerState # Używamy schematów Pydantic

class BaseDisability(ABC):
    """Abstrakcyjna klasa bazowa dla logiki niepełnosprawności."""

    def __init__(self, severity: DisabilitySeverity):
        if not isinstance(severity, DisabilitySeverity):
             raise TypeError(f"Severity must be an instance of DisabilitySeverity enum, got {type(severity)}")
        self.severity = severity
        self._severity_map = {
            DisabilitySeverity.MILD: 1,
            DisabilitySeverity.MODERATE: 2,
            DisabilitySeverity.SEVERE: 3
        }
        self.severity_level = self._severity_map.get(severity, 1)

    @abstractmethod
    def apply_player_modifiers(self, player_state: PlayerState) -> PlayerState:
        """Modyfikuje *bezpośrednio* atrybuty stanu gracza (prędkość, percepcja, etc.)."""
        pass

    @abstractmethod
    def apply_world_effects(self, game_state: GameState) -> GameState:
        """Dodaje/modyfikuje globalne efekty w świecie gry (np. wizualne, dźwiękowe)
           interpretowane przez frontend."""
        pass

    def get_interaction_modifier(self, interaction_type: str) -> float:
        """(Opcjonalnie) Zwraca modyfikator do trudności/czasu interakcji."""
        return 1.0 # Domyślnie brak modyfikatora