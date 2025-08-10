// Plik: frontend/src/App.js

import React, { useState } from 'react';
import backgroundImage from './assets/background.jpeg';

// Krok 1: Zmień importy - usuń GameScene, dodaj BudynekAplikacjiScene
import CharacterCreationScene from './scenes/CharacterCreationScene';
import BudynekAplikacjiScene from './scenes/BudynekAplikacjiScene'; // Nowy import

import { GameStateProvider } from './contexts/GameStateContext';
import './App.css';

function App() {
    const [isGameStarted, setIsGameStarted] = useState(false);

    // Ta funkcja jest przekazywana do CharacterCreationScene i wywoływana,
    // gdy gra zostanie pomyślnie utworzona.
    const handleGameStart = () => {
        setIsGameStarted(true);
    };

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
        // GameStateProvider może pozostać, jeśli inne części aplikacji (np. przyszłe sceny gry)
        // będą z niego korzystać. Nie przeszkadza on w działaniu.
        <GameStateProvider>
            <div className="App" style={appStyle}>
                <main>
                    {/* 
                      Krok 2: Zaktualizuj logikę renderowania warunkowego.
                      Teraz po rozpoczęciu gry ładujemy BudynekAplikacjiScene.
                    */}
                    {isGameStarted ? (
                        // Po rozpoczęciu gry pokazujemy budynek z aplikacjami
                        <BudynekAplikacjiScene />
                    ) : (
                        // Na początku pokazujemy ekran tworzenia postaci wraz z nagłówkiem
                        <>
                            <header className="App-header">
                                <h1>Gra RPG</h1>
                            </header>
                            <CharacterCreationScene onGameStart={handleGameStart} />
                        </>
                    )}
                </main>
            </div>
        </GameStateProvider>
    );
}

export default App;