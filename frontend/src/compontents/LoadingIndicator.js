// src/components/LoadingIndicator.js
import React from 'react';

function LoadingIndicator() {
    return <div style={{ padding: '20px', textAlign: 'center', fontWeight: 'bold' }}>Loading...</div>;
}

export default LoadingIndicator;

// src/components/ErrorDisplay.js
import React from 'react';

function ErrorDisplay({ message }) {
    if (!message) return null;
    return <div style={{ padding: '10px', margin: '10px', color: 'red', border: '1px solid red', backgroundColor: '#ffeeee' }}>Error: {message}</div>;
}

export default ErrorDisplay;