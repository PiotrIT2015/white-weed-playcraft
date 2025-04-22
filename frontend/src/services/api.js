// Adres URL twojego backendu FastAPI
const BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api'; // Użyj zmiennej środowiskowej lub domyślnej

// Funkcja pomocnicza do obsługi zapytań fetch
const fetchApi = async (endpoint, options = {}) => {
    const url = `${BASE_URL}${endpoint}`;
    const defaultHeaders = {
        'Content-Type': 'application/json',
        // Możesz dodać inne nagłówki, np. autoryzacji, jeśli będą potrzebne
    };

    const config = {
        ...options,
        headers: {
            ...defaultHeaders,
            ...options.headers,
        },
    };

    try {
        const response = await fetch(url, config);
        if (!response.ok) {
            // Spróbuj sparsować błąd z odpowiedzi API, jeśli istnieje
            let errorData;
            try {
                errorData = await response.json();
            } catch (e) {
                // Ignoruj błąd parsowania, jeśli odpowiedź nie jest JSONem
            }
            console.error(`API Error ${response.status}: ${response.statusText}`, errorData);
            throw new Error(`API Error: ${response.status} ${response.statusText}` + (errorData?.detail ? ` - ${errorData.detail}` : ''));
        }
        // Jeśli status to 204 No Content, zwróć null (np. dla DELETE)
        if (response.status === 204) {
            return null;
        }
        return await response.json();
    } catch (error) {
        console.error('Network or fetch error:', error);
        throw error; // Rzuć błąd dalej, aby komponent mógł go obsłużyć
    }
};

// Funkcje API odpowiadające endpointom backendu
export const api = {
    createGame: (characterData) => {
        return fetchApi('/game/new', {
            method: 'POST',
            body: JSON.stringify(characterData),
        });
    },

    getGameState: () => {
        return fetchApi('/game/state');
    },

    postAction: (actionData) => {
        return fetchApi('/game/action', {
            method: 'POST',
            body: JSON.stringify(actionData),
        });
    },

    saveGame: (saveData = { save_name: "ManualSave" }) => {
        return fetchApi('/game/save', {
            method: 'POST',
            body: JSON.stringify(saveData),
        });
    },

    loadGame: (saveId) => {
        return fetchApi(`/game/load/${saveId}`, { // Zmieniono na GET wg routingu backendu
             method: 'GET', // Poprawiono metodę na GET
        });
    },

    listSaves: (skip = 0, limit = 10) => {
        return fetchApi(`/game/saves?skip=${skip}&limit=${limit}`);
    },

    // Można dodać inne potrzebne funkcje API
};