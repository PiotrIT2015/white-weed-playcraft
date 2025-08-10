import React, { useState, useEffect } from 'react';
// Upewnij się, że ścieżka do api.js jest poprawna
import { api } from '../services/api'; 
import './CharacterCreationScene.css';

// Komponent przyjmuje funkcje onGameStart i onGameLoad do komunikacji z rodzicem
const CharacterCreationScene = ({ onGameStart, onGameLoad }) => { 
  // --- Stan dla formularza ---
  const [characterName, setCharacterName] = useState('');
  const [disabilityType, setDisabilityType] = useState('Vision');
  const [disabilitySeverity, setDisabilitySeverity] = useState('Mild');
  
  // --- Stan dla logiki komponentu ---
  const [view, setView] = useState('menu'); // 'menu' lub 'create_character'
  const [saves, setSaves] =useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  // Pobieranie listy zapisów, gdy komponent jest montowany
  useEffect(() => {
    // Nie pobieraj zapisów, jeśli nie jesteśmy w menu
    if (view !== 'menu') return;

    const fetchSaves = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const savesData = await api.getAllSaves();
        setSaves(savesData);
      } catch (err) {
        setError("Nie udało się pobrać listy zapisów.");
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    };
    fetchSaves();
  }, [view]); // Uruchom ponownie, gdy wrócimy do widoku 'menu'

  // --- Handlery (funkcje obsługi zdarzeń) ---

  const handleStartNewGame = async (event) => {
    event.preventDefault();
    setIsLoading(true);
    setError(null);
    try {
      const result = await api.createNewGame({ characterName, disabilityType, disabilitySeverity });
      // Przekaż pełny stan gry do komponentu nadrzędnego
      onGameStart(result.gameState); 
    } catch (err) {
      setError(err.message);
      setIsLoading(false); 
    }
  };

  const handleLoadGameClick = async (saveId) => {
    setIsLoading(true);
    setError(null);
    try {
      const loadedGameState = await api.loadGame(saveId);
      onGameLoad(loadedGameState); // Przekaż załadowany stan do rodzica
    } catch (err) {
      setError(`Błąd wczytywania gry: ${err.message}`);
      setIsLoading(false);
    }
  };

  // --- Funkcje renderujące poszczególne widoki ---

  const renderMenu = () => (
    <>
      <h1 className="main-title">Gra RPG</h1>
      <h2 className="sub-title">Stwórz nową postać</h2>

      <button className="submit-button" onClick={() => setView('create_character')}>
        Rozpocznij nową grę
      </button>

      <div className="divider"></div>

      <h2 className="sub-title-secondary">Wczytaj grę</h2>
      {isLoading && <p>Wczytywanie zapisów...</p>}
      <ul className="saves-list">
        {!isLoading && saves.length > 0 ? (
          saves.map(save => (
            <li key={save.id} className="save-item" onClick={() => handleLoadGameClick(save.id)}>
              Początek gry - {save.characterName} - Zapisano: {new Date(save.savedAt).toLocaleString('pl-PL')}
            </li>
          ))
        ) : (
          !isLoading && <p>Brak zapisanych gier.</p>
        )}
      </ul>
    </>
  );

  const renderCreateCharacter = () => (
    <>
      <button className="back-button" onClick={() => setView('menu')}>&larr; Powrót</button>
      <h1 className="main-title">Gra RPG</h1>
      <h2 className="sub-title">Create Your Character</h2>

      <form onSubmit={handleStartNewGame}>
        {/* Tu wklejamy cały formularz, który mieliśmy wcześniej */}
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
            <select id="disabilityType" className="form-select" value={disabilityType} onChange={(e) => setDisabilityType(e.target.value)} disabled={isLoading}>
              <option value="Vision">Vision</option>
              <option value="Neurological">Neurological</option>
              <option value="Mobility">Mobility</option>
              <option value="Hearing">Hearing</option>
            </select>
          </div>
          <div className="form-group">
            <label htmlFor="disabilitySeverity">Severity:</label>
            <select id="disabilitySeverity" className="form-select" value={disabilitySeverity} onChange={(e) => setDisabilitySeverity(e.target.value)} disabled={isLoading}>
              <option value="Mild">Mild</option>
              <option value="Moderate">Moderate</option>
              <option value="Severe">Severe</option>
            </select>
          </div>
          <button type="submit" className="submit-button" disabled={isLoading}>
            {isLoading ? 'Tworzenie...' : 'Rozpocznij Grę'}
          </button>
      </form>
    </>
  );

  return (
    <div className="creation-background">
      <div className="form-container">
        {/* Renderowanie warunkowe w zależności od stanu 'view' */}
        {view === 'menu' ? renderMenu() : renderCreateCharacter()}
        
        {/* Komunikat o błędzie, wspólny dla obu widoków */}
        {error && <p className="error-message">{error}</p>}
      </div>
    </div>
  );
};

export default CharacterCreationScene;