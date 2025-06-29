import React from 'react';
import './App.css'; 

// Importowanie komponentów - upewnij się, że ścieżki są poprawne!
import GameView from './compontents/Gamearea/GameView';
import StatusPanel from './compontents/Sidebar/StatusPanel';
import GameControls from './compontents/Gamearea/GameControls';

// ===== POPRAWKA BŁĘDU NR 2 =====
// Zamiast importować GameStateContext, importujemy hook useGameState
import { useGameState } from './contexts/GameStateContext';
import LoadingIndicator from './compontents/shared/LoadingIndicator'; // Zakładam, że masz ten komponent
import ErrorDisplay from './compontents/shared/ErrorDisplay';       // i ten też

function App() {
  // Używamy hooka, aby uzyskać dostęp do wszystkiego z kontekstu
  const { gameState, isLoading, error, setError } = useGameState();

  // Jeśli aplikacja się ładuje, pokaż tylko wskaźnik
  if (isLoading) {
    return <LoadingIndicator />;
  }

  // Jeśli wystąpił błąd, pokaż go
  // (Zakładam, że ErrorDisplay ma przycisk do zamykania, który wywołuje setError(null))
  if (error) {
    return <ErrorDisplay message={error} onDismiss={() => setError(null)} />;
  }

  // Jeśli nie ma stanu gry, pokaż ekran tworzenia postaci lub menu
  // (Na razie prosty tekst)
  if (!gameState) {
    return <div>Gra nie została jeszcze rozpoczęta. (Tu będzie CharacterCreationScene)</div>;
  }
  
  // Główny widok gry
  return (
    <div className="game-container">
      <header className="header-area">
        <h1>Witaj w mieście!</h1>
      </header>

      <main className="game-view-area">
        <GameView />
      </main>

      <aside className="sidebar-area">
        <StatusPanel />
      </aside>

      <footer className="controls-area">
        <GameControls />
        <div className="message-log">
          <h3>Wiadomości:</h3>
          {/* Zakładam, że wiadomość jest teraz częścią gameState */}
          <p>{gameState.message || 'Brak nowych wiadomości.'}</p>
        </div>
      </footer>
    </div>
  );
}

export default App;