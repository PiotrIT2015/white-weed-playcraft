from sqlalchemy import Column, Integer, String, Enum as SQLEnum, JSON, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from .database import Base # Importuj Base z tego samego modułu

# Enumy dla typów używanych w bazie danych
class DisabilityTypeDB(str, enum.Enum):
    VISION = "vision"
    HEARING = "hearing"
    MOBILITY = "mobility"
    NEUROLOGICAL = "neurological"
    EPILEPSY = "epilepsy"

class DisabilitySeverityDB(str, enum.Enum):
    MILD = "mild"
    MODERATE = "moderate"
    SEVERE = "severe"

# Na razie pomijamy model Player/User, skupiamy się na zapisach
# Można go dodać później, jeśli potrzebne jest zarządzanie kontami

class GameSave(Base):
    __tablename__ = "game_saves"

    id = Column(Integer, primary_key=True, index=True)
    character_name = Column(String(100), index=True) # Uproszczenie - zakładamy imię postaci
    disability_type = Column(SQLEnum(DisabilityTypeDB), nullable=False)
    disability_severity = Column(SQLEnum(DisabilitySeverityDB), nullable=False)
    save_name = Column(String(100), default="AutoSave")
    # Przechowuje cały stan gry jako JSON - elastyczne, ale mniej wydajne dla zapytań o konkretne dane stanu
    game_state_json = Column(JSON, nullable=False)
    saved_at = Column(DateTime, default=datetime.utcnow)

    # Można dodać relację do użytkownika, jeśli będzie model User/Player
    # player_id = Column(Integer, ForeignKey("players.id"))
    # player = relationship("Player")