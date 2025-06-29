// Plik: frontend/src/App.js

import React, { useState } from 'react';

// 1. Zaimportuj obrazek - Webpack zwróci poprawną ścieżkę
import backgroundImage from './assets/background.jpeg'; 

import CharacterCreationScene from './scenes/CharacterCreationScene'; // Zaktualizuj ścieżkę, jeśli trzeba
import GameScene from './scenes/GameScene'; // Zaktualizuj ścieżkę, jeśli trzeba
import { GameStateProvider } from './contexts/GameStateContext';
import './App.css';

function App() {
    const [isGameStarted, setIsGameStarted] = useState(false);

    const handleGameStart = () => {
        setIsGameStarted(true);
    };

    // 2. Stwórz obiekt stylu, który zostanie użyty poniżej
    const appStyle = {
      backgroundImage: `url(${backgroundImage})`,
      backgroundSize: 'cover',
      backgroundRepeat: 'no-repeat',
      backgroundAttachment: 'fixed',
      backgroundPosition: 'center center',
      minHeight: '100vh',
      width: '100vw'
    };

    return (
        <GameStateProvider>
            {/* 3. Zastosuj styl do głównego kontenera aplikacji */}
            <div className="App" style={appStyle}>
                <header className="App-header">
                    <h1>Gra RPG</h1>
                </header>
                <main>
                    {isGameStarted ? (
                        <GameScene />
                    ) : (
                        <CharacterCreationScene onGameStart={handleGameStart} />
                    )}
                </main>
            </div>
        </GameStateProvider>
    );
}

export default App;