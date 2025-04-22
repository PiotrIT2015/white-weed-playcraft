import React from 'react';

function DialogueBox({ text }) {
    if (!text) {
        return null; // Nie renderuj, jeśli nie ma tekstu
    }

    const style = {
        position: 'absolute', // Lub fixed, jeśli ma być zawsze na dole ekranu
        bottom: '10px',
        left: '10px',
        right: '10px',
        backgroundColor: 'rgba(0, 0, 0, 0.7)',
        color: 'white',
        padding: '15px',
        borderRadius: '5px',
        border: '1px solid #ccc',
        minHeight: '50px',
    };

    return (
        <div className="dialogue-box" style={style}>
            <p>{text}</p>
        </div>
    );
}

export default DialogueBox;