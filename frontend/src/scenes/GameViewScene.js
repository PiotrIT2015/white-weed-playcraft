import React, { useEffect, useCallback } from 'react';
import { useGameState } from '../contexts/GameStateContext';
import { api } from '../services/api';
import PlayerCharacter from '../compontents/PlayerCharacter';
import NPCCharacter from '../compontents/NPCCharacter';
import DialogueBox from '../compontents/DialogueBox';
import DisabilityOverlay from '../compontents/DisabilityOverlay';
import GameControls from '../compontents/GameControls'; // Komponent z przyciskami Save/Load

function GameViewScene() {
    // Twoje istniejące haki - wszystko tu jest w porządku
    const { gameState, updateGameState, setIsLoading, setError } = useGameState();

    // Twoja istniejąca funkcja do obsługi akcji - bez zmian
    const handlePlayerAction = useCallback(async (action) => {
        if (!gameState) return;
        setError(null);
        try {
            const newState = await api.postAction(action);
            updateGameState(newState);
        } catch (err) {
            console.error(`Failed to perform action ${action.action_type}:`, err);
            setError(err.message || 'Action failed.');
        }
    }, [gameState, updateGameState, setError]);

    // Twój istniejący useEffect do obsługi klawiatury - bez zmian
    useEffect(() => {
        const handleKeyDown = (event) => {
            if (!gameState) return;
            let dx = 0;
            let dy = 0;
            const moveAmount = 5;

            switch (event.key) {
                case 'ArrowUp': case 'w': dy = -moveAmount; break;
                case 'ArrowDown': case 's': dy = moveAmount; break;
                case 'ArrowLeft': case 'a': dx = -moveAmount; break;
                case 'ArrowRight': case 'd': dx = moveAmount; break;
                default: return;
            }

            if (dx !== 0 || dy !== 0) {
                handlePlayerAction({ action_type: 'move', details: { dx, dy } });
            }
        };
        window.addEventListener('keydown', handleKeyDown);
        return () => {
            window.removeEventListener('keydown', handleKeyDown);
        };
    }, [gameState, handlePlayerAction]);

    // Twoja istniejąca funkcja do obsługi kliknięcia na NPC - bez zmian
    const handleNpcClick = (npcId) => {
        console.log(`Clicked on NPC: ${npcId}`);
        handlePlayerAction({ action_type: 'talk', target_id: npcId });
    };

    // --- NOWA FUNKCJA ---
    // Ta funkcja zostanie przekazana do GameControls.
    // Gdy GameControls pomyślnie wczyta grę przez API, wywoła tę funkcję,
    // przekazując nowy stan gry, który zaktualizuje całą aplikację.
    const handleGameLoad = (loadedGameState) => {
        console.log("Game state loaded in GameViewScene, updating context...");
        updateGameState(loadedGameState);
    };

    // Renderowanie - bez zmian
    if (!gameState) {
        return <div>Loading game data...</div>;
    }

    const currentDialogue = gameState.npcs.find(npc => npc.current_dialogue)?.current_dialogue;

    // --- ZMIANA W SEKCJI RETURN ---
    // Zaktualizowaliśmy wywołanie komponentu <GameControls />, aby przekazać mu
    // funkcje, których potrzebuje do działania.
    return (
        <div className="game-view">
            <div className="game-world" style={{ position: 'relative', width: '800px', height: '600px', border: '1px solid black', overflow: 'hidden', backgroundColor: '#eee' }}>
                <PlayerCharacter player={gameState.player} />
                {gameState.npcs.map(npc => (
                    <NPCCharacter key={npc.id} npc={npc} onClick={() => handleNpcClick(npc.id)} />
                ))}
                <DisabilityOverlay effects={gameState.world_effects} />
            </div>

            <DialogueBox text={currentDialogue} />

            {/* --- ZMODYFIKOWANY KOMPONENT --- */}
            {/* Przekazujemy handlePlayerAction, aby przyciski ruchu w GameControls mogły wysyłać akcje. */}
            {/* Przekazujemy onGameLoad, aby GameControls mógł poinformować tę scenę o wczytaniu nowego stanu gry. */}
            <GameControls
                handlePlayerAction={handlePlayerAction}
                onGameLoad={handleGameLoad}
            />

        </div>
    );
}

export default GameViewScene;