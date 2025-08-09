import React from 'react';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';

// Importujemy główne style
import './App.css';

// --- IMPORTUJEMY WSZYSTKIE SCENY ---
// Upewnij się, że te pliki istnieją w folderze 'scenes'
import CharacterCreationScene from './scenes/CharacterCreationScene';
import GameScene from './scenes/GameScene'; // Nasza nowo przeniesiona scena gry
import GameViewScene from './scenes/GameViewScene';
import BudynekAplikacjiScene from './scenes/BudynekAplikacjiScene'; 

// Komponent prostego menu głównego do nawigacji
const MainMenu = () => {
  return (
    <div className="main-menu">
      <h1>Menu Główne</h1>
      <nav>
        <ul>
          <li>
            <Link to="/tworzenie-postaci">Nowa Gra</Link>
          </li>
          <li>
            {/* Ten link prowadzi teraz do Twojej sceny gry! */}
            <Link to="/gra">Wejdź do Miasta</Link>
          </li>
          <li>
            <Link to="/aplikacje">Odwiedź Centrum Aktywności</Link>
          </li>
        </ul>
      </nav>
    </div>
  );
};


function App() {
  return (
    <BrowserRouter>
      <div className="App">
        {/* Routes działa jak przełącznik - renderuje scenę pasującą do adresu URL */}
        <Routes>
          {/* Gdy adres to "/", pokaż menu główne */}
          <Route path="/" element={<MainMenu />} />
          
          {/* Definicje pozostałych scen */}
          <Route path="/tworzenie-postaci" element={<CharacterCreationScene />} />
          <Route path="/gra" element={<GameScene />} />
          <Route path="/widok-gry" element={<GameViewScene />} />
          <Route path="/aplikacje" element={<BudynekAplikacjiScene />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
