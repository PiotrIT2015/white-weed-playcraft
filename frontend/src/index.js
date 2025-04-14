import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import axios from 'axios';

const runEngine = () => {
  axios.post('http://localhost:8000/run-engine')
    .then(response => {
      console.log(response.data);
    })
    .catch(error => {
      console.error("Błąd uruchamiania silnika:", error);
    });
};

function App2() {
  return (
    <div>
      <h1>Start Game Engine</h1>
      <button onClick={runEngine}>Uruchom silnik</button>
    </div>
  );
}

export default App2;


const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App2 />
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
