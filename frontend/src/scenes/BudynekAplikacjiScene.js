import React from 'react';

// Możesz dodać trochę stylów, aby "budynek" i "drzwi" wyglądały lepiej.
// Najlepiej umieścić je w osobnym pliku CSS, np. `BudynekAplikacjiScene.css`
// i zaimportować go tutaj.
import './BudynekAplikacjiScene.css'; 

const BudynekAplikacjiScene = () => {
  // URL do Twojej aplikacji na GitHub. Zmień go na właściwy link.
  // Użyj linku do GitHub Pages (jeśli masz tam wersję demonstracyjną)
  // lub po prostu do repozytorium.
  const myAppUrl = 'https://github.com/PiotrIT2015/WW-P-sounds-help';

  return (
    <div className="scene-container">
      <h1>Witaj w Centrum Aktywności!</h1>
      <p>Wybierz aplikację, z której chcesz skorzystać.</p>
      
      <div className="applications-grid">
        {/* Link do Duolingo */}
        <a 
          href="https://www.duolingo.com/" 
          target="_blank" 
          rel="noopener noreferrer" 
          className="app-link"
        >
          <div className="app-door">
            <h2>Duolingo</h2>
            <p>Nauka języków obcych</p>
          </div>
        </a>

        {/* Link do Brainia */}
        {/* Znalazłem aplikację Brainia w sklepach z aplikacjami, ale strona internetowa jest mniej oczywista. */}
        {/* Poniżej link do oficjalnej strony, z której można pobrać aplikację. */}
        <a 
          href="https://logiclike.com/pl/lamiglowki/dla-doroslych" 
          target="_blank" 
          rel="noopener noreferrer" 
          className="app-link"
        >
          <div className="app-door">
            <h2>Brainia</h2>
            <p>Zagadki i trening mózgu</p>
          </div>
        </a>

        {/* Link do Twojej aplikacji */}
        <a 
          href={myAppUrl}
          target="_blank" 
          rel="noopener noreferrer" 
          className="app-link"
        >
          <div className="app-door my-app">
            <h2>Tłumacz Migowy</h2>
            <p>Twoja aplikacja pomagająca głuchoniemym</p>
          </div>
        </a>
      </div>
    </div>
  );
};

export default BudynekAplikacjiScene;