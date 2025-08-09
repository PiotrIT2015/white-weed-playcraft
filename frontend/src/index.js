import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';
import { GameStateProvider } from './contexts/GameStateContext';
import './index.css'; // Twój główny plik stylów

const container = document.getElementById('root');
const root = createRoot(container);

root.render(
  <React.StrictMode>
    <GameStateProvider>
      <App />
    </GameStateProvider>
  </React.StrictMode>
);
