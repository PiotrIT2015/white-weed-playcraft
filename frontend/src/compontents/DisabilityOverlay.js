import React from 'react';

function DisabilityOverlay({ effects = [] }) {
    if (!effects || effects.length === 0) {
        return null;
    }

    const overlayStyles = {
        position: 'absolute',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        pointerEvents: 'none', // Aby nie blokować kliknięć na elementy pod spodem
        zIndex: 10, // Aby była na wierzchu
    };

    // Zastosuj style na podstawie efektów z backendu
    effects.forEach(effect => {
        if (effect === 'visual_blur_mild') {
            overlayStyles.backdropFilter = (overlayStyles.backdropFilter || '') + ' blur(1px)';
        } else if (effect === 'visual_blur_moderate') {
             overlayStyles.backdropFilter = (overlayStyles.backdropFilter || '') + ' blur(3px)';
        } else if (effect === 'visual_grayscale') {
            overlayStyles.backdropFilter = (overlayStyles.backdropFilter || '') + ' grayscale(100%)';
        } else if (effect === 'tunnel_vision_severe') {
            // Prosta symulacja przez gradient - wymaga dopracowania
             overlayStyles.background = 'radial-gradient(circle, transparent 30%, black 80%)';
        }
        // Można dodać obsługę efektów dźwiękowych (np. przez Web Audio API) lub innych
         if (effect.includes('audio_muffled')) {
             console.warn("Audio effect simulation not implemented in this example:", effect);
         }
    });

    return <div className="disability-overlay" style={overlayStyles}></div>;
}

export default DisabilityOverlay;