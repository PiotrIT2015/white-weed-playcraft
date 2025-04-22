import React from 'react';
import { createRoot } from 'react-dom/client';
import './styles/main.css';
import App from './App';
import { GameStateProvider } from './contexts/GameStateContext';

const root = createRoot(document.getElementById('root'));
root.render(
  <GameStateProvider>
    <App />
  </GameStateProvider>
);
