import React from 'react';
import styles from './Controls.module.css';

/**
 * Renderuje przyciski sterowania.
 * @param {object} props - Właściwości komponentu.
 * @param {(direction: 'up'|'down'|'left'|'right') => void} props.onMove - Funkcja wywoływana po kliknięciu przycisku ruchu.
 */
const Controls = ({ onMove }) => {
  return (
    <div className={styles.controls}>
      <p>Sterowanie:</p>
      <button onClick={() => onMove('up')}>Góra</button>
      <br />
      <button onClick={() => onMove('left')}>Lewo</button>
      <button onClick={() => onMove('right')}>Prawo</button>
      <br />
      <button onClick={() => onMove('down')}>Dół</button>
    </div>
  );
};

export default Controls;