<<<<<<< HEAD
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
=======
.scene-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background-color: #f0f2f5;
  font-family: 'Arial', sans-serif;
  color: #333;
  padding: 20px;
  box-sizing: border-box;
}

h1 {
  color: #2c3e50;
  margin-bottom: 10px;
  font-size: 2.5em;
  text-align: center;
}

p {
  color: #555;
  margin-bottom: 30px;
  font-size: 1.1em;
  text-align: center;
}

.applications-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 30px;
  width: 100%;
  max-width: 1200px;
  padding: 20px;
}

.app-link {
  text-decoration: none;
  color: inherit;
}

.app-door {
  background-color: #ffffff;
  border-radius: 15px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
  padding: 30px;
  text-align: center;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  height: 200px; /* Ujednolicenie wysokości drzwi */
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  border: 2px solid transparent; /* Dodajemy border dla efektu hover */
}
>>>>>>> 1b0ef463254675e538c7d51053d4d9658018e247

.app-door:hover {
  transform: translateY(-10px);
  box-shadow: 0 12px 25px rgba(0, 0, 0, 0.15);
  border-color: #3498db; /* Kolor ramki przy najechaniu */
}

.app-door h2 {
  color: #34495e;
  margin-top: 0;
  margin-bottom: 10px;
  font-size: 1.8em;
}

.app-door p {
  color: #7f8c8d;
  font-size: 1em;
  margin-bottom: 0;
}

/* Specjalne style dla Twojej aplikacji, aby się wyróżniała */
.my-app {
  background-color: #3498db;
  color: #ffffff;
}

.my-app h2,
.my-app p {
  color: #ffffff;
}

.my-app:hover {
  background-color: #2980b9;
  border-color: #2980b9;
}

/* Responsywność */
@media (max-width: 768px) {
  h1 {
    font-size: 2em;
  }

  p {
    font-size: 1em;
  }

  .applications-grid {
    grid-template-columns: 1fr;
    padding: 15px;
  }

  .app-door {
    padding: 25px;
    height: 180px;
  }

  .app-door h2 {
    font-size: 1.5em;
  }
}

@media (max-width: 480px) {
  h1 {
    font-size: 1.8em;
  }

  p {
    font-size: 0.9em;
  }

  .app-door {
    padding: 20px;
    height: 160px;
  }

  .app-door h2 {
    font-size: 1.3em;
  }
}