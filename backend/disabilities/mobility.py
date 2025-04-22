from .base_disability import BaseDisability
from api.schemas import GameState, PlayerState, DisabilitySeverity

class MobilityDisability(BaseDisability):
    """Logika dla niepełnosprawności ruchowej."""

    def apply_player_modifiers(self, player_state: PlayerState) -> PlayerState:
        """Zmniejsza prędkość i potencjalnie staminę."""
        if self.severity == DisabilitySeverity.MILD:
            player_state.current_speed_modifier = 0.85
            player_state.stamina -= 0.1 # Bardzo lekkie zmęczenie przy ruchu
        elif self.severity == DisabilitySeverity.MODERATE:
            player_state.current_speed_modifier = 0.65
            player_state.stamina -= 0.3
        elif self.severity == DisabilitySeverity.SEVERE:
            player_state.current_speed_modifier = 0.40
            player_state.stamina -= 0.6

        player_state.stamina = max(0, player_state.stamina) # Stamina nie może być ujemna
        return player_state

    def apply_world_effects(self, game_state: GameState) -> GameState:
        """Może dodać informację o potrzebie dostępności."""
        if self.severity_level >= 2: # Umiarkowany lub znaczny
            game_state.world_effects.append("accessibility_needed_moderate")
        # Nie dodaje efektów wizualnych/dźwiękowych bezpośrednio
        return game_state

    def get_interaction_modifier(self, interaction_type: str) -> float:
        """Niektóre interakcje mogą być trudniejsze/wolniejsze."""
        if interaction_type in ["climb_stairs", "reach_high_shelf"]:
            return 1.5 + (self.severity_level * 0.5) # Znacząco trudniejsze
        return 1.0