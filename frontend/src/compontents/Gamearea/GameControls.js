import React, { useState } from 'react';
import { useGameState } from '../contexts/GameStateContext';
import { api } from '../services/api';

// Importy komponentów i ikon z Material-UI
import { Box, Button, Stack, Paper, Typography, List, ListItem, ListItemButton, ListItemText, IconButton, CircularProgress, Alert } from '@mui/material';
import { ArrowUpward, ArrowDownward, ArrowLeft, ArrowRight, Save, FolderOpen, Close } from '@mui/icons-material';

/**
 * Komponent kontrolek gry.
 * @param {object} props
 * @param {function} props.handlePlayerAction - Funkcja z GameViewScene do wysyłania akcji (np. ruchu).
 * @param {function} props.onGameLoad - Funkcja z komponentu nadrzędnego do obsłużenia wczytanego stanu gry.
 */
const GameControls = ({ handlePlayerAction, onGameLoad }) => {
    const { gameState } = useGameState();
    const [saves, setSaves] = useState([]);
    const [showLoadMenu, setShowLoadMenu] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const [message, setMessage] = useState({ type: '', text: '' }); // type: 'success' | 'error'

    const moveAmount = 5; // Dystans ruchu postaci

    // Funkcje do obsługi ruchu
    const handleMove = (dx, dy) => {
        if (!gameState || !handlePlayerAction) return;
        handlePlayerAction({ action_type: 'move', details: { dx, dy } });
    };

    // Zapisywanie gry
    const handleSave = async () => {
        if (!gameState) return;
        setIsLoading(true);
        setMessage({ type: '', text: '' });
        try {
            const result = await api.saveGame(`Zapis - ${new Date().toLocaleTimeString()}`);
            setMessage({ type: 'success', text: result.message });
        } catch (error) {
            setMessage({ type: 'error', text: `Błąd zapisu: ${error.message}` });
        } finally {
            setIsLoading(false);
            setTimeout(() => setMessage({ type: '', text: '' }), 5000);
        }
    };

    // Pobieranie listy zapisów i pokazywanie menu
    const fetchSavesAndShowMenu = async () => {
        setIsLoading(true);
        setMessage({ type: '', text: '' });
        try {
            const savesData = await api.getAllSaves();
            setSaves(savesData);
            setShowLoadMenu(true);
        } catch (error) {
            setMessage({ type: 'error', text: `Nie udało się pobrać zapisów: ${error.message}` });
        } finally {
            setIsLoading(false);
        }
    };

    // Wczytywanie wybranego zapisu
    const handleLoad = async (saveId) => {
        setIsLoading(true);
        setMessage({ type: '', text: '' });
        try {
            const loadedGameState = await api.loadGame(saveId);
            onGameLoad(loadedGameState); // Przekaż załadowany stan do rodzica!
            setShowLoadMenu(false);
        } catch (error) {
            setMessage({ type: 'error', text: `Błąd wczytywania: ${error.message}` });
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <Paper elevation={3} sx={{ padding: '16px', marginTop: '16px', backgroundColor: 'rgba(255, 255, 255, 0.9)' }}>
            <Stack spacing={2} direction="row" alignItems="center">
                
                {/* --- SEKCJA RUCHU --- */}
                <Box>
                    <Stack direction="row" justifyContent="center">
                        <IconButton onClick={() => handleMove(0, -moveAmount)} disabled={!gameState || isLoading}><ArrowUpward /></IconButton>
                    </Stack>
                    <Stack direction="row" justifyContent="center" spacing={1}>
                        <IconButton onClick={() => handleMove(-moveAmount, 0)} disabled={!gameState || isLoading}><ArrowLeft /></IconButton>
                        <IconButton onClick={() => handleMove(0, moveAmount)} disabled={!gameState || isLoading}><ArrowDownward /></IconButton>
                        <IconButton onClick={() => handleMove(moveAmount, 0)} disabled={!gameState || isLoading}><ArrowRight /></IconButton>
                    </Stack>
                </Box>
                
                {/* --- SEKCJA ZAPISU I WCZYTYWANIA --- */}
                <Stack spacing={1}>
                    <Button
                        variant="contained"
                        startIcon={<Save />}
                        onClick={handleSave}
                        disabled={!gameState || isLoading}
                    >
                        Zapisz Grę
                    </Button>
                    <Button
                        variant="outlined"
                        startIcon={<FolderOpen />}
                        onClick={fetchSavesAndShowMenu}
                        disabled={isLoading}
                    >
                        Wczytaj Grę
                    </Button>
                </Stack>

                {/* --- Wyświetlanie komunikatu o stanie operacji --- */}
                <Box sx={{ flexGrow: 1 }}>
                    {isLoading && <CircularProgress size={24} />}
                    {message.text && (
                        <Alert severity={message.type || 'info'} sx={{ marginTop: '10px' }}>{message.text}</Alert>
                    )}
                </Box>
            </Stack>

            {/* --- MODALNE OKNO WCZYTYWANIA --- */}
            {showLoadMenu && (
                <Paper elevation={2} sx={{ marginTop: '16px', padding: '16px', border: '1px solid #ddd' }}>
                    <Stack direction="row" justifyContent="space-between" alignItems="center">
                        <Typography variant="h6">Wybierz zapis do wczytania:</Typography>
                        <IconButton onClick={() => setShowLoadMenu(false)}><Close /></IconButton>
                    </Stack>
                    
                    {saves.length > 0 ? (
                        <List>
                            {saves.map(save => (
                                <ListItem key={save.id} disablePadding>
                                    <ListItemButton onClick={() => handleLoad(save.id)} disabled={isLoading}>
                                        <ListItemText 
                                            primary={save.saveName || `Zapis ${save.id}`} 
                                            secondary={`${save.characterName} - ${new Date(save.savedAt).toLocaleString()}`} 
                                        />
                                    </ListItemButton>
                                </ListItem>
                            ))}
                        </List>
                    ) : (
                        <Typography sx={{ mt: 2 }}>Nie znaleziono zapisów.</Typography>
                    )}
                </Paper>
            )}
        </Paper>
    );
};

export default GameControls;