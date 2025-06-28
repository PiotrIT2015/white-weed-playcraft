# disabilities/__init__.py
from .base_disability import BaseDisability
from .mobility import MobilityDisability
from .vision import VisionDisability
# Importuj inne klasy niepełnosprawności w miarę ich tworzenia
# from .hearing import HearingDisability
# from .neurological import NeurologicalDisability
# from .epilepsy import EpilepsyDisability
from api.schemas import PlayerState
from api.schemas import GameState

from api.schemas import DisabilityType, DisabilitySeverity

# Prosta fabryka do tworzenia instancji handlerów
def create_disability_handler(disability_type: DisabilityType, severity: DisabilitySeverity) -> BaseDisability:
    """Tworzy odpowiedni obiekt obsługujący logikę niepełnosprawności."""
    handler_map = {
        DisabilityType.MOBILITY: MobilityDisability,
        DisabilityType.VISION: VisionDisability,
        # Dodaj mapowania dla innych typów
        # DisabilityType.HEARING: HearingDisability,
        # DisabilityType.NEUROLOGICAL: NeurologicalDisability,
        # DisabilityType.EPILEPSY: EpilepsyDisability,
    }

    handler_class = handler_map.get(disability_type)

    if handler_class:
        return handler_class(severity)
    else:
        # Fallback dla nieimplementowanych typów - handler, który nic nie robi
        print(f"Warning: Disability type '{disability_type}' handler not implemented. Using default.")
        class NoOpDisability(BaseDisability):
            def apply_player_modifiers(self, player_state: PlayerState) -> PlayerState: return player_state
            def apply_world_effects(self, game_state: GameState) -> GameState: return game_state
        return NoOpDisability(severity)