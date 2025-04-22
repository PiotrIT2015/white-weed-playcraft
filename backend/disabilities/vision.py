from .base_disability import BaseDisability
from api.schemas import GameState, PlayerState, DisabilitySeverity

class VisionDisability(BaseDisability):
    """Logika dla niepełnosprawności wzrokowej."""

    def apply_player_modifiers(self, player_state: PlayerState) -> PlayerState:
        """Modyfikuje percepcję wizualną."""
        acuity_modifier = 1.0
        range_modifier = 1.0

        if self.severity == DisabilitySeverity.MILD:
            acuity_modifier = 0.8
            range_modifier = 0.9
        elif self.severity == DisabilitySeverity.MODERATE:
            acuity_modifier = 0.5
            range_modifier = 0.6
        elif self.severity == DisabilitySeverity.SEVERE:
            acuity_modifier = 0.2
            range_modifier = 0.3

        player_state.perception_modifier['visual_acuity'] = acuity_modifier
        player_state.perception_modifier['visual_range'] = range_modifier
        # Można dodać inne aspekty, np. wrażliwość na światło, widzenie barw
        return player_state

    def apply_world_effects(self, game_state: GameState) -> GameState:
        """Dodaje efekty wizualne interpretowane przez frontend."""
        if self.severity == DisabilitySeverity.MILD:
            game_state.world_effects.append("visual_blur_mild")
        elif self.severity == DisabilitySeverity.MODERATE:
            game_state.world_effects.append("visual_blur_moderate")
            game_state.world_effects.append("visual_contrast_reduced")
        elif self.severity == DisabilitySeverity.SEVERE:
            game_state.world_effects.append("visual_blur_severe")
            game_state.world_effects.append("visual_tunnel_vision_moderate") # Przykład tunelowego widzenia
            # game_state.world_effects.append("visual_grayscale_partial") # Problemy z kolorami

        # Potencjalnie modyfikuje widoczność NPC/obiektów dla logiki gry (nie tylko wizualnie)
        # (To wymagałoby bardziej złożonej symulacji percepcji w engine)

        return game_state

    def get_interaction_modifier(self, interaction_type: str) -> float:
        """Interakcje wymagające dobrego wzroku są trudniejsze."""
        if interaction_type in ["read_text", "find_small_object", "recognize_face_distance"]:
            return 1.0 / player_state.perception_modifier.get('visual_acuity', 1.0) # Odwrotność ostrości
        return 1.0