import React from 'react';

function NPCCharacter({ npc, onClick }) {
    if (!npc) return null;

    // Prosta wizualizacja - kółko
    const style = {
        position: 'absolute',
        left: `${npc.position.x}px`,
        top: `${npc.position.y}px`,
        width: '18px',
        height: '18px',
        backgroundColor: 'green', // NPC są zielone
        border: '1px solid darkgreen',
        borderRadius: '50%', // Kółko
        cursor: 'pointer', // Wskaźnik kliknięcia
        textAlign: 'center',
        lineHeight: '18px',
        fontSize: '10px',
        color: 'white',
        transition: 'left 0.5s linear, top 0.5s linear' // Wolniejszy, płynny ruch NPC
    };

    return (
        <div
            className="npc-character"
            style={style}
            title={npc.name}
            onClick={onClick} // Dodaj obsługę kliknięcia
        >
            {/* Można dodać inicjał np. N */}
        </div>
    );
}

export default NPCCharacter;