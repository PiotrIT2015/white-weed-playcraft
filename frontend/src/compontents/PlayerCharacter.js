import React from 'react';

function PlayerCharacter({ player }) {
    if (!player) return null;

    // Prosta wizualizacja - kwadrat
    const style = {
        position: 'absolute',
        left: `${player.position.x}px`,
        top: `${player.position.y}px`,
        width: '20px',
        height: '20px',
        backgroundColor: 'blue', // Gracz jest niebieski
        border: '1px solid darkblue',
        transition: 'left 0.1s linear, top 0.1s linear' // Płynniejszy ruch
    };

    // Zmiana wyglądu w zależności od niepełnosprawności (bardzo prosty przykład)
    if (player.disability_type === 'mobility') {
        style.backgroundColor = 'lightblue'; // Jaśniejszy kolor dla problemów z ruchem
    }
    // Można dodać inne modyfikacje stylu

    return <div className="player-character" style={style} title={player.name}></div>;
}

export default PlayerCharacter;