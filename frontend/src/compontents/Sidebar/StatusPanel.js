import React from 'react';

const StatusPanel = () => {
  return (
    <div>
      <h3>Status Postaci</h3>
      <ul>
        <li>Doświadczenie życiowe: 0</li>
        <li>Energia: 100%</li>
        {/* W przyszłości: dane z GameStateContext */}
      </ul>
    </div>
  );
};

export default StatusPanel;