import React, { createContext, useState, useContext, useCallback } from 'react';

// Utwórz kontekst
const GameStateContext = createContext(null);

// Utwórz dostawcę kontekstu (Provider)
export const GameStateProvider = ({ children }) => {
    const [gameState, setGameState] = useState(null); // Początkowy stan gry (null = niezaładowana)
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);

    // Funkcja do aktualizacji stanu (można dodać logikę, np. walidację)
    const updateGameState = useCallback((newState) => {
        console.log("Updating game state:", newState);
        setGameState(newState);
        setError(null); // Resetuj błąd przy udanej aktualizacji
    }, []);

    // Wartość dostarczana przez kontekst
    const value = {
        gameState,
        updateGameState,
        isLoading,
        setIsLoading,
        error,
        setError,
    };

    return (
        <GameStateContext.Provider value={value}>
            {children}
        </GameStateContext.Provider>
    );
};

// Hook do łatwego używania kontekstu w komponentach
export const useGameState = () => {
    const context = useContext(GameStateContext);
    if (!context) {
        throw new Error('useGameState must be used within a GameStateProvider');
    }
    return context;
};