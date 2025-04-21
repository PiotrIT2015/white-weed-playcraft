import React from 'react';
import Character from '../Character/Character'; // Upewnij się, że ścieżka jest poprawna
import styles from './GameArea.module.css';

/**
 * Główny obszar gry, renderujący elementy statyczne i postać.
 * @param {object} props - Właściwości komponentu.
 * @param {{x: number, y: number}} props.characterPosition - Aktualna pozycja postaci.
 * @param {Array<object>} props.elements - Tablica obiektów danych elementów statycznych.
 * @param {number} props.width - Szerokość obszaru gry.
 * @param {number} props.height - Wysokość obszaru gry.
 */
const GameArea = ({ characterPosition, elements, width, height }) => {

    // Pomocnik do pobierania klasy CSS na podstawie typu elementu
    const getElementClassName = (type) => { // Usunięto typy parametrów/zwracane
        switch (type) {
            case 'building': return styles.building;
            case 'road': return styles.road;
            case 'kerb': return styles.kerb;
            case 'ramp': return styles.ramp;
            case 'obstacle': return styles.obstacle;
            default: return '';
        }
    }

    return (
        <div className={styles.gameArea} style={{ width: `${width}px`, height: `${height}px` }}>
            {/* Renderuj Elementy Statyczne */}
            {elements.map(el => (
                <div
                    key={el.id}
                    className={`${styles.staticElement} ${getElementClassName(el.type)}`}
                    style={{
                        left: `${el.x}px`,
                        top: `${el.y}px`,
                        width: `${el.width}px`,
                        height: `${el.height}px`,
                    }}
                    title={el.label || el.type} // Tooltip
                >
                    {el.label}
                </div>
            ))}

            {/* Renderuj Postać */}
            <Character x={characterPosition.x} y={characterPosition.y} />
        </div>
    );
};

export default GameArea;