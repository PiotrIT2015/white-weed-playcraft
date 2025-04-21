import React from 'react';
import ReactDOM from 'react-dom/client';
import './styles/global.css'; // Import global styles
import App from './App.jsx'; // Zmieniono import na .jsx
// import reportWebVitals from './reportWebVitals'; // Opcjonalnie

const rootElement = document.getElementById('root'); // Usunięto 'as HTMLElement'

if (rootElement) { // Dobrą praktyką jest sprawdzenie, czy element istnieje
    const root = ReactDOM.createRoot(rootElement);
    root.render(
      <React.StrictMode>
        <App />
      </React.StrictMode>
    );
} else {
    console.error("Nie znaleziono elementu 'root'. Aplikacja React nie może zostać załadowana.");
}


// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
// reportWebVitals();
