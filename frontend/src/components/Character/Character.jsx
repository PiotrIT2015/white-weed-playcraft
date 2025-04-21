import React from 'react';
import styles from './Character.module.css';

/**
 * Reprezentuje postać gracza.
 * @param {object} props - Właściwości komponentu.
 * @param {number} props.x - Pozycja pozioma (left).
 * @param {number} props.y - Pozycja pionowa (top).
 */
const Character = ({ x, y }) => {
  return (
    <div
      className={styles.character}
      style={{ left: `${x}px`, top: `${y}px` }}
      aria-label="Postać na wózku inwalidzkim"
      role="img"
    >
      ♿
    </div>
  );
};

export default Character;