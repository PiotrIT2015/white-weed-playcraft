import React, { useState } from 'react';
import { useGameState } from '../../contexts/GameStateContext';
import { api } from '../../services/api';

import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import ArrowUpwardIcon from '@mui/icons-material/ArrowUpward'; // npm install @mui/icons-material


function GameControls() {
    const { updateGameState, setIsLoading, setError } = useGameState();
    const [saves, setSaves] = useState([]);
    const [showLoadMenu, setShowLoadMenu] = useState(false);

    const handleSave = async () => {
        setIsLoading(true);
        setError(null);
        try {
            const saveInfo = await api.saveGame(); // Używa domyślnej nazwy
            alert(`Game saved successfully! ID: ${saveInfo.id}`);
        } catch (err) {
            console.error("Failed to save game:", err);
            setError(err.message || 'Failed to save game.');
        } finally {
            setIsLoading(false);
        }
    };

    const fetchSaves = async () => {
         setIsLoading(true);
         setError(null);
         try {
             const saveList = await api.listSaves();
             setSaves(saveList);
             setShowLoadMenu(true); // Pokaż menu po pobraniu
         } catch (err) {
             console.error("Failed to list saves:", err);
             setError(err.message || 'Failed to load save list.');
             setShowLoadMenu(false);
         } finally {
             setIsLoading(false);
         }
     };


    const handleLoad = async (saveId) => {
        setIsLoading(true);
        setError(null);
        setShowLoadMenu(false); // Ukryj menu ładowania
        try {
            const loadedState = await api.loadGame(saveId);
            updateGameState(loadedState);
            alert(`Game loaded successfully from save ID: ${saveId}`);
        } catch (err) {
            console.error("Failed to load game:", err);
            setError(err.message || 'Failed to load game.');
            // Można przywrócić poprzedni stan gry lub pokazać błąd w inny sposób
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="game-controls" style={{ marginTop: '10px', padding: '10px', borderTop: '1px solid #ccc' }}>

        <Box>

            <Button variant="contained" startIcon={<ArrowUpwardIcon />}>Góra</Button>
            {/* ... inne przyciski */}
  

            <Button onClick={handleSave}>Save Game</Button>
            <Button onClick={fetchSaves} style={{ marginLeft: '10px' }}>Load Game</Button>

            {showLoadMenu && (
                <div className="load-menu" style={{ marginTop: '10px', border: '1px solid #eee', padding: '10px' }}>
                    <h4>Select Save to Load:</h4>
                    {saves.length > 0 ? (
                        <ul>
                            {saves.map(save => (
                                <li key={save.id} style={{ cursor: 'pointer', marginBottom: '5px' }} onClick={() => handleLoad(save.id)}>
                                    {save.save_name} ({save.character_name} - {new Date(save.saved_at).toLocaleString()})
                                </li>
                            ))}
                        </ul>
                    ) : (
                        <p>No saves found.</p>
                    )}
                    <Button onClick={() => setShowLoadMenu(false)}>Cancel</Button>
                </div>
            )}

            </Box>

        </div>
    );
}

export default GameControls;