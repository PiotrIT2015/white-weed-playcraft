// Definiujemy bazowy adres URL naszego API w jednym miejscu.
// Jeśli kiedykolwiek zmienisz port lub domenę, wystarczy zmienić to tutaj.
const API_BASE_URL = 'http://localhost:5000/api';

/**
 * Pomocnicza funkcja do obsługi odpowiedzi z API.
 * Sprawdza, czy odpowiedź jest poprawna, a jeśli nie, rzuca błędem
 * z komunikatem od serwera.
 * @param {Response} response - Obiekt odpowiedzi z fetch.
 * @returns {Promise<any>} - Dane JSON z odpowiedzi.
 */
const handleResponse = async (response) => {
  if (!response.ok) {
    // Próbujemy odczytać treść błędu z odpowiedzi serwera
    const errorData = await response.json().catch(() => ({})); // .catch na wypadek, gdyby treść nie była JSON-em
    const errorMessage = errorData.error || `Request failed with status ${response.status}`;
    throw new Error(errorMessage);
  }
  return response.json();
};

/**
 * Rozpoczyna nową grę.
 * @param {{characterName: string, disabilityType: string, disabilitySeverity: string}} characterData 
 * @returns {Promise<object>} - Stan nowej gry.
 */
const createNewGame = async (characterData) => {
  const response = await fetch(`${API_BASE_URL}/new-game`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(characterData),
  });
  return handleResponse(response);
};

/**
 * Zapisuje aktualny stan gry.
 * @param {string} saveName - Opcjonalna nazwa dla zapisu.
 * @returns {Promise<object>} - Potwierdzenie zapisu z serwera.
 */
const saveGame = async (saveName) => {
  const response = await fetch(`${API_BASE_URL}/saves`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ save_name: saveName }),
  });
  return handleResponse(response);
};

/**
 * Pobiera listę wszystkich dostępnych zapisów.
 * @returns {Promise<Array>} - Lista obiektów reprezentujących zapisy.
 */
const getAllSaves = async () => {
  const response = await fetch(`${API_BASE_URL}/saves`, {
    method: 'GET',
  });
  return handleResponse(response);
};

/**
 * Wczytuje grę z podanego zapisu.
 * UWAGA: Ten endpoint musi zostać zaimplementowany w backendzie!
 * Przykładowo: @app.route('/api/saves/<int:save_id>/load', methods=['POST'])
 * @param {number} saveId - ID zapisu do wczytania.
 * @returns {Promise<object>} - Stan gry z wczytanego zapisu.
 */
const loadGame = async (saveId) => {
  // UWAGA: Dostosuj ten endpoint do swojej implementacji w backendzie!
  const response = await fetch(`${API_BASE_URL}/saves/${saveId}/load`, { 
    method: 'POST',
  });
  return handleResponse(response);
};

/**
 * Wysyła akcję gracza (ruch, rozmowa itp.) do serwera.
 * @param {object} action - Obiekt akcji.
 * @returns {Promise<object>} - Zaktualizowany stan gry.
 */
const postAction = async (action) => {
    const response = await fetch(`${API_BASE_URL}/action`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(action)
    });
    return handleResponse(response);
};


// Eksportujemy wszystkie funkcje w jednym obiekcie `api` dla łatwego importu.
export const api = {
  createNewGame,
  saveGame,
  getAllSaves,
  loadGame,
  postAction,
};