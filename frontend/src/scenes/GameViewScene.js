import React, { useEffect, useCallback } from 'react';
import { useGameState } from '..\contexts\GameStateContext';
import { api } from '..\services\api';
import PlayerCharacter from '..\components\PlayerCharacter';
import NPCCharacter from '..\components\NPCCharacter';
import DialogueBox from '..\components\DialogueBox';
import DisabilityOverlay from '..\components\DisabilityOverlay';
import GameControls from '..\components\GameControls'; // Komponent z przyciskami Save/Load

function GameViewScene() {
    const { gameState, updateGameState, setIsLoading, setError } = useGameState();

    // --- Obsługa Akcji Gracza ---
    const handlePlayerAction = useCallback(async (action) => {
        if (!gameState) return; // Nie rób nic, jeśli stan gry nie jest załadowany

        // setIsLoading(true); // Opcjonalnie: pokaż ładowanie podczas akcji
        setError(null);

        try {
            const newState = await api.postAction(action);
            updateGameState(newState); // Aktualizuj stan po odpowiedzi backendu
        } catch (err) {
            console.error(`Failed to perform action ${action.action_type}:`, err);
            setError(err.message || 'Action failed.');
        } finally {
            // setIsLoading(false);
        }
    }, [gameState, updateGameState, setError]); // Dodano setError do zależności

    // --- Obsługa Ruchu Klawiaturą ---
    useEffect(() => {
        const handleKeyDown = (event) => {
            if (!gameState) return; // Nie reaguj, jeśli gra nieaktywna

            let dx = 0;
            let dy = 0;
            const moveAmount = 5; // Jak daleko postać się porusza na krok

            switch (event.key) {
                case 'ArrowUp':
                case 'w':
                    dy = -moveAmount;
                    break;
                case 'ArrowDown':
                case 's':
                    dy = moveAmount;
                    break;
                case 'ArrowLeft':
                case 'a':
                    dx = -moveAmount;
                    break;
                case 'ArrowRight':
                case 'd':
                    dx = moveAmount;
                    break;
                default:
                    return; // Ignoruj inne klawisze
            }

             if (dx !== 0 || dy !== 0) {
                handlePlayerAction({ action_type: 'move', details: { dx, dy } });
             }
        };

        window.addEventListener('keydown', handleKeyDown);

        // Cleanup listener on component unmount
        return () => {
            window.removeEventListener('keydown', handleKeyDown);
        };
    }, [gameState, handlePlayerAction]); // Uruchom ponownie, jeśli gameState lub handlePlayerAction się zmieni

    // --- Obsługa Interakcji (np. Kliknięcie na NPC) ---
    const handleNpcClick = (npcId) => {
        console.log(`Clicked on NPC: ${npcId}`);
        handlePlayerAction({ action_type: 'talk', target_id: npcId });
    };

    // --- Renderowanie ---
    if (!gameState) {
        // Jeśli stan jest null, może to oznaczać ładowanie lub błąd,
        // obsłużone już w App.js, ale można dodać tu fallback
        return <div>Loading game data...</div>;
    }

    // Znajdź aktualny dialog (pierwszy NPC, który coś mówi) - uproszczenie
    const currentDialogue = gameState.npcs.find(npc => npc.current_dialogue)?.current_dialogue;


    return (
        <div className="game-view">
            <div className="game-world" style={{ position: 'relative', width: '800px', height: '600px', border: '1px solid black', overflow: 'hidden', backgroundColor: '#eee' /* Proste tło */ }}>
                {/* Renderuj Postać Gracza */}
                <PlayerCharacter player={gameState.player} />

                {/* Renderuj NPC */}
                {gameState.npcs.map(npc => (
                    <NPCCharacter key={npc.id} npc={npc} onClick={() => handleNpcClick(npc.id)} />
                ))}

                {/* Nakładka Efektów Niepełnosprawności */}
                <DisabilityOverlay effects={gameState.world_effects} />
            </div>

            {/* Okno Dialogowe */}
            <DialogueBox text={currentDialogue} />

            {/* Kontrolki Gry (Save/Load) */}
            <GameControls />

            {/* Informacje Debugowe (opcjonalnie) */}
            {/* <pre style={{ fontSize: '10px', maxHeight: '100px', overflowY: 'auto' }}>
                {JSON.stringify(gameState, null, 2)}
            </pre> */}
        </div>
    );
}

export default GameViewScene;