import React, { useState, useEffect } from 'react';
import CharacterCreationScene from '.\scenes\CharacterCreationScene';
import GameViewScene from '.\scenes\GameViewScene';
import LoadingIndicator from '.\components\LoadingIndicator'; // Prosty komponent ładowania
import ErrorDisplay from '.\components\ErrorDisplay'; // Prosty komponent błędu
import { useGameState } from '.\contexts\GameStateContext';

function App() {
    const { gameState, isLoading, error } = useGameState();
    // Stan określający, czy gra została rozpoczęta (postać stworzona lub załadowana)
    const [isGameActive, setIsGameActive] = useState(false);

    // Efekt do ustawienia flagi `isGameActive` gdy `gameState` nie jest już null
    useEffect(() => {
        if (gameState) {
            setIsGameActive(true);
        }
        // Można dodać logikę resetowania `isGameActive` np. przy wylogowaniu
    }, [gameState]);

     // Funkcja wywoływana po pomyślnym stworzeniu/załadowaniu gry
     const handleGameStart = () => {
         setIsGameActive(true);
     };

    return (
        <div className="App">
            <h1>Empatia: Symulator Codzienności</h1>
            {isLoading && <LoadingIndicator />}
            {error && <ErrorDisplay message={error} />}

            {!isLoading && !error && (
                 <>
                    {!isGameActive ? (
                        <CharacterCreationScene onGameStart={handleGameStart} />
                    ) : (
                        <GameViewScene />
                    )}
                 </>
            )}
            {/* Można dodać stopkę lub inne globalne elementy UI */}
        </div>
    );
}

export default App;