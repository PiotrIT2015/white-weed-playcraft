import React, { useState } from 'react';
import './CharacterCreationScene.css';

// Krok 1: Zmień sygnaturę komponentu, aby przyjmował props 'onGameStart'
const CharacterCreationScene = ({ onGameStart }) => { 
  const [characterName, setCharacterName] = useState('');
  const [disabilityType, setDisabilityType] = useState('vision');
  const [disabilitySeverity, setDisabilitySeverity] = useState('mild');
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleStartGame = async (event) => {
    event.preventDefault();
    setIsLoading(true);
    setError(null);
    setSuccessMessage('');

    const characterData = {
      characterName,
      disabilityType,
      disabilitySeverity,
    };

    try {
      const response = await fetch('http://localhost:5000/api/new-game', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(characterData),
      });

      const result = await response.json();

      if (!response.ok) {
        throw new Error(result.error || 'Wystąpił nieznany błąd serwera.');
      }
      
      setSuccessMessage(`Gra dla postaci ${result.gameState.player.name} została pomyślnie utworzona! Rozpoczynamy...`);
      
      // Krok 2: Wywołaj funkcję z komponentu nadrzędnego po krótkim opóźnieniu,
      // aby użytkownik zdążył przeczytać komunikat.
      setTimeout(() => {
        onGameStart(); // <-- TO JEST KLUCZOWA ZMIANA!
      }, 2000); // 2-sekundowe opóźnienie

    } catch (err) {
      setError(err.message);
      // Musimy wyłączyć ładowanie również w przypadku błędu
      setIsLoading(false); 
    } 
    // Usunięto 'finally', aby 'isLoading' nie zostało ustawione na 'false' od razu po sukcesie,
    // co mogłoby pozwolić na ponowne kliknięcie przycisku przed zmianą sceny.
  };

  // Reszta kodu JSX pozostaje bez zmian
  return (
    <div className="creation-background">
      <div className="form-container">
        
        <h1 className="main-title">Gra RPG</h1>
        <h2 className="sub-title">Create Your Character</h2>

        <form onSubmit={handleStartGame}>
          <div className="form-group">
            <label htmlFor="characterName">Character Name:</label>
            <input
              type="text"
              id="characterName"
              className="form-input"
              value={characterName}
              onChange={(e) => setCharacterName(e.target.value)}
              required
              disabled={isLoading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="disabilityType">Disability Type:</label>
            <select 
              id="disabilityType" 
              className="form-select"
              value={disabilityType} 
              onChange={(e) => setDisabilityType(e.target.value)} 
              disabled={isLoading}
            >
              <option value="vision">Vision</option>
              <option value="neurological">Neurological</option>
              <option value="mobility">Mobility</option>
              <option value="hearing">Hearing</option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="disabilitySeverity">Severity:</label>
            <select 
              id="disabilitySeverity" 
              className="form-select"
              value={disabilitySeverity} 
              onChange={(e) => setDisabilitySeverity(e.target.value)} 
              disabled={isLoading}
            >
              <option value="mild">Mild</option>
              <option value="moderate">Moderate</option>
              <option value="severe">Severe</option>
            </select>
          </div>

          <button type="submit" className="submit-button" disabled={isLoading}>
            {isLoading ? 'Tworzenie gry...' : 'Start Game'}
          </button>

          {error && <p className="error-message">Błąd: {error}</p>}
          {successMessage && <p className="success-message">{successMessage}</p>}
        </form>
      </div>
    </div>
  );
};

export default CharacterCreationScene;