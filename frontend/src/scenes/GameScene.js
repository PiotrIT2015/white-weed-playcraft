// Plik: src/components/GameScene.js
import React from 'react';
import { useGameState } from '../contexts/GameStateContext';

function GameScene() {
    // Możesz pobrać stan gry, aby wyświetlić np. imię postaci
    const { gameState } = useGameState();

    return (
        <div>
            <h2>Gra w toku!</h2>
            {gameState && (
                <p>Witaj w grze, {gameState.character.name}!</p>
            )}
            <p>Tutaj będzie się toczyć główna rozgrywka.</p>
        </div>
    );
}

export default GameScene;