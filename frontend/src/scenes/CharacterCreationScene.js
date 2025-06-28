import React, { useState } from 'react';
import { useGameState } from '../contexts/GameStateContext';
import { api } from '../services/api';

// Dostępne opcje (powinny odpowiadać enumom w backendzie/schematach Pydantic)
const disabilityTypes = ['vision', 'hearing', 'mobility', 'neurological', 'epilepsy'];
const disabilitySeverities = ['mild', 'moderate', 'severe'];

function CharacterCreationScene({ onGameStart }) {
    const [characterName, setCharacterName] = useState('');
    const [selectedType, setSelectedType] = useState(disabilityTypes[0]);
    const [selectedSeverity, setSelectedSeverity] = useState(disabilitySeverities[0]);
    const { updateGameState, setIsLoading, setError } = useGameState();
    const [isCreating, setIsCreating] = useState(false); // Lokalny stan ładowania

    const handleSubmit = async (event) => {
        event.preventDefault();
        if (!characterName.trim()) {
            setError('Character name cannot be empty.');
            return;
        }
        setIsLoading(true);
        setIsCreating(true);
        setError(null);

        const characterData = {
            character_name: characterName,
            disability_type: selectedType,
            disability_severity: selectedSeverity,
        };

        try {
            const newGameState = await api.createGame(characterData);
            updateGameState(newGameState); // Aktualizuj globalny stan gry
            onGameStart(); // Poinformuj App.js o rozpoczęciu gry
        } catch (err) {
            console.error("Failed to create game:", err);
            setError(err.message || 'Failed to create character. Please try again.');
             // Nie wywołuj onGameStart w przypadku błędu
        } finally {
            setIsLoading(false);
            setIsCreating(false);
        }
    };

    return (
        <div className="character-creation">
            <h2>Create Your Character</h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label htmlFor="charName">Character Name:</label>
                    <input
                        type="text"
                        id="charName"
                        value={characterName}
                        onChange={(e) => setCharacterName(e.target.value)}
                        required
                        disabled={isCreating}
                    />
                </div>
                <div>
                    <label htmlFor="disType">Disability Type:</label>
                    <select
                        id="disType"
                        value={selectedType}
                        onChange={(e) => setSelectedType(e.target.value)}
                        disabled={isCreating}
                    >
                        {disabilityTypes.map(type => (
                            <option key={type} value={type}>{type}</option>
                        ))}
                    </select>
                </div>
                <div>
                    <label htmlFor="disSeverity">Severity:</label>
                    <select
                        id="disSeverity"
                        value={selectedSeverity}
                        onChange={(e) => setSelectedSeverity(e.target.value)}
                        disabled={isCreating}
                    >
                        {disabilitySeverities.map(severity => (
                            <option key={severity} value={severity}>{severity}</option>
                        ))}
                    </select>
                </div>
                <button type="submit" disabled={isCreating}>
                    {isCreating ? 'Creating...' : 'Start Game'}
                </button>
            </form>
            {/* Można tu dodać opcję ładowania gry */}
        </div>
    );
}

export default CharacterCreationScene;