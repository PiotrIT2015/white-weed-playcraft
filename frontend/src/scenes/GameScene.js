import React, { useState, useEffect, useCallback } from 'react';
// ZMIANA: Ścieżka importu musi teraz wyjść o jeden folder w górę
import GameArea from '../components/GameArea/GameArea'; 
import Controls from '../components/Controls/Controls'; 
// Nie potrzebujemy tutaj App.css, style dla sceny można dodać w osobnym pliku

// --- Konfiguracja Gry ---
const GAME_WIDTH = 500;
const GAME_HEIGHT = 400;
const CHARACTER_WIDTH = 30;
const CHARACTER_HEIGHT = 30;
const STEP_SIZE = 10;

const staticElements = [
    { id: 'b1', type: 'building', x: 50, y: 50, width: 150, height: 100, label: 'Budynek 1', isObstacle: true },
    { id: 'b2', type: 'building', x: 300, y: 150, width: 100, height: 150, label: 'Budynek 2', isObstacle: true },
    { id: 'road1', type: 'road', x: 0, y: 260, width: GAME_WIDTH, height: 80, isObstacle: false },
    { id: 'kerb1', type: 'kerb', x: 0, y: 250, width: GAME_WIDTH, height: 10, isObstacle: true, label: "Krawężnik" },
    { id: 'kerb2', type: 'kerb', x: 0, y: 340, width: GAME_WIDTH, height: 10, isObstacle: true, label: "Krawężnik" },
    { id: 'ramp1', type: 'ramp', x: 200, y: 240, width: 50, height: 30, label: 'Podjazd', isObstacle: false, isAccessible: true },
    { id: 'obs1', type: 'obstacle', x: 400, y: 300, width: 40, height: 40, label: 'Przeszkoda', isObstacle: true },
];


// ZMIANA: Zmieniono nazwę funkcji z "App" na "GameScene"
function GameScene() {
    const [characterPosition, setCharacterPosition] = useState({ x: 20, y: 350 });

    const checkCollision = useCallback((newPos) => {
        const charRect = {
            left: newPos.x,
            right: newPos.x + CHARACTER_WIDTH,
            top: newPos.y,
            bottom: newPos.y + CHARACTER_HEIGHT,
        };

        for (const el of staticElements) {
            if (!el.isObstacle) continue;

            const elRect = { left: el.x, right: el.x + el.width, top: el.y, bottom: el.y + el.height };

            if (
                charRect.left < elRect.right && charRect.right > elRect.left &&
                charRect.top < elRect.bottom && charRect.bottom > elRect.top
            ) {
                let isOverriddenByRamp = false;
                if (el.type === 'kerb') {
                    for (const ramp of staticElements) {
                         if (ramp.isAccessible && ramp.type === 'ramp') {
                             const rampRect = { left: ramp.x, right: ramp.x + ramp.width, top: ramp.y, bottom: ramp.y + ramp.height };
                             const charCenterX = newPos.x + CHARACTER_WIDTH / 2;
                             const charCenterY = newPos.y + CHARACTER_HEIGHT / 2;

                             if (charCenterX > rampRect.left && charCenterX < rampRect.right &&
                                 charCenterY > rampRect.top && charCenterY < rampRect.bottom) {
                                 isOverriddenByRamp = true;
                                 break;
                             }
                         }
                    }
                }

                if (!isOverriddenByRamp) {
                     console.log("Kolizja z:", el.id);
                     return true;
                }
            }
        }
        return false;
    }, []);

    const moveCharacter = useCallback((direction) => {
        setCharacterPosition(prevPos => {
            let newX = prevPos.x;
            let newY = prevPos.y;

            switch (direction) {
                case 'up': newY -= STEP_SIZE; break;
                case 'down': newY += STEP_SIZE; break;
                case 'left': newX -= STEP_SIZE; break;
                case 'right': newX += STEP_SIZE; break;
                default: return prevPos;
            }

            newX = Math.max(0, Math.min(newX, GAME_WIDTH - CHARACTER_WIDTH));
            newY = Math.max(0, Math.min(newY, GAME_HEIGHT - CHARACTER_HEIGHT));

            const newPos = { x: newX, y: newY };

            if (checkCollision(newPos)) {
                return prevPos;
            }
            return newPos;
        });
    }, [checkCollision]);

    useEffect(() => {
        const handleKeyDown = (event) => {
            let direction = null;
            switch (event.key) {
                case 'ArrowUp': direction = 'up'; break;
                case 'ArrowDown': direction = 'down'; break;
                case 'ArrowLeft': direction = 'left'; break;
                case 'ArrowRight': direction = 'right'; break;
                default: break;
            }

            if (direction) {
                event.preventDefault();
                moveCharacter(direction);
            }
        };

        window.addEventListener('keydown', handleKeyDown);
        return () => {
            window.removeEventListener('keydown', handleKeyDown);
        };
    }, [moveCharacter]);

    return (
        <div className="game-container"> {/* Można użyć innej klasy niż .App */}
            <h1>Witaj w mieście React (JS)!</h1>
            <GameArea
                characterPosition={characterPosition}
                elements={staticElements}
                width={GAME_WIDTH}
                height={GAME_HEIGHT}
            />
            <Controls onMove={moveCharacter} />
        </div>
    );
}

// ZMIANA: Eksportujemy GameScene
export default GameScene;