import React from 'react';
// Importujemy plik CSS tutaj. WAŻNE: to jest linia JavaScript, która informuje Webpacka o CSS.
import './BudynekAplikacjiScene.css'; // <--- Poprawiona linia

const BudynekAplikacjiScene = () => {
  const myAppUrl = 'https://pcamobileapp.azurewebsites.net/';

  return (
    <div className="scene-container">
      <h1>Witaj w Centrum Aktywności!</h1>
      <p>Wybierz aplikację, z której chcesz skorzystać.</p>

      <div className="applications-grid">
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