import requests
import os
import json
import random
from dotenv import load_dotenv
from typing import Optional
from api.schemas import GameState, NPCState, PlayerState # Importuj schematy dla kontekstu

load_dotenv()

GROK_API_KEY = os.getenv("GROK_API_KEY")
GROK_API_URL = os.getenv("GROK_API_URL") # Odczytaj URL z .env

# Placeholder responses jeśli API nie działa/nie jest skonfigurowane
PLACEHOLDER_RESPONSES = [
    "Hmm...",
    "Rozumiem.",
    "Daj mi chwilę pomyśleć.",
    "Ciekawe.",
    "Coś jeszcze?",
    "Naprawdę?",
]

def get_npc_dialogue(game_state: GameState, npc: NPCState, player_message: Optional[str] = None) -> str:
    """
    Pobiera odpowiedź dialogową od AI (Grok-1) dla danego NPC w kontekście stanu gry.
    """
    if not GROK_API_KEY or not GROK_API_URL:
        print("WARN: Grok API Key or URL not configured. Returning placeholder response.")
        return f"{npc.name}: {random.choice(PLACEHOLDER_RESPONSES)}"

    headers = {
        "Authorization": f"Bearer {GROK_API_KEY}",
        "Content-Type": "application/json",
    }

    # --- Budowanie Kontekstowego Promptu ---
    player = game_state.player
    disability_desc = f"{player.disability_severity.value} {player.disability_type.value}"

    # Opis sytuacji
    prompt_context = f"""Jesteś postacią niezależną (NPC) o imieniu {npc.name} w grze 'Empatia: Symulator Codzienności'.
Znajdujesz się w scenie: {game_state.current_scene}. Aktualny czas w grze: {game_state.game_time}.
Twoja aktualna akcja to: {npc.current_action}. Twoje nastawienie do gracza: {npc.attitude_towards_player:.1f} (-1 wrogi, 0 neutralny, 1 przyjazny).

Gracz, {player.name}, ma niepełnosprawność: {disability_desc}.
Oto jego stan: Szybkość: {player.current_speed_modifier*100:.0f}%, Stamina: {player.stamina:.0f}/100.
Percepcja gracza może być ograniczona: {player.perception_modifier}.

"""

    # Poprzednia linijka dialogu NPC (jeśli istnieje)
    if npc.current_dialogue:
        prompt_context += f"Twoja ostatnia wypowiedź: \"{npc.current_dialogue}\"\n"

    # Wiadomość od gracza (jeśli to kontynuacja rozmowy)
    if player_message:
         prompt_context += f"Gracz ({player.name}) mówi do Ciebie: \"{player_message}\"\n"
    else:
         # Jeśli to początek interakcji
         prompt_context += f"Gracz ({player.name}) właśnie podszedł i zainicjował rozmowę.\n"

    # Instrukcje dla AI
    prompt_instructions = f"""Twoim zadaniem jest wygenerować następną linię dialogową dla postaci {npc.name}.
Odpowiedz realistycznie, krótko (1-2 zdania) i spójnie z kontekstem, osobowością {npc.name} oraz uwzględniając sytuację gracza (jego niepełnosprawność może wpływać na interakcję).
Nie powtarzaj dokładnie tego, co powiedziałeś przed chwilą. Bądź empatyczny, neutralny lub lekko nieufny, w zależności od sytuacji i nastawienia.
Nie używaj cudzysłowów ani nazwy postaci w odpowiedzi. Podaj tylko sam tekst dialogu.

Odpowiedź {npc.name}:"""

    full_prompt = prompt_context + prompt_instructions

    # --- Zapytanie do API ---
    payload = {
        "model": "grok-1", # Sprawdź poprawną nazwę modelu
        "prompt": full_prompt,
        "max_tokens": 60,
        "temperature": 0.7, # Odrobina kreatywności
        "stop": ["\n", f"{player.name}:"] # Zatrzymaj generowanie na nowej linii lub gdy AI zacznie mówić za gracza
    }

    try:
        print(f"--- Sending prompt to Grok for {npc.name} ---")
        # print(full_prompt) # Uncomment for debugging prompts
        print("--- End of prompt ---")

        response = requests.post(GROK_API_URL, headers=headers, json=payload, timeout=20) # Zwiększony timeout
        response.raise_for_status() # Sprawdza błędy HTTP 4xx/5xx

        result = response.json()
        print(f"Grok raw response: {result}") # Debug raw response

        # Dostosuj do struktury odpowiedzi Grok-1
        # Przykład zakładający strukturę podobną do OpenAI GPT
        if "choices" in result and len(result["choices"]) > 0:
            ai_reply = result["choices"][0].get("text", "").strip()
            if ai_reply:
                print(f"Grok generated reply for {npc.name}: '{ai_reply}'")
                # Proste oczyszczenie odpowiedzi (może wymagać ulepszenia)
                ai_reply = ai_reply.replace(f"{npc.name}:", "").strip()
                return f"{npc.name}: {ai_reply}" # Dodajemy nazwę NPC dla jasności w logach/UI
            else:
                 print(f"WARN: Grok API returned empty text for {npc.name}.")
                 return f"{npc.name}: {random.choice(PLACEHOLDER_RESPONSES)}"
        else:
            print(f"Error: Unexpected response format from Grok API for {npc.name}: {result}")
            return f"{npc.name}: {random.choice(PLACEHOLDER_RESPONSES)} (API format issue)"

    except requests.exceptions.Timeout:
        print(f"Error: Timeout connecting to Grok API for {npc.name}.")
        return f"{npc.name}: Chwileczkę, zamyśliłem się... (Timeout)"
    except requests.exceptions.RequestException as e:
        print(f"Error communicating with Grok API for {npc.name}: {e}")
        # Można sprawdzić status code np. e.response.status_code
        error_msg = f"(API Error: {e.response.status_code})" if hasattr(e, 'response') and e.response else "(API Network Error)"
        return f"{npc.name}: Przepraszam, coś mnie rozproszyło... {error_msg}"
    except Exception as e:
        print(f"An unexpected error occurred during AI call for {npc.name}: {e}")
        return f"{npc.name}: Muszę zebrać myśli... (Internal Error)"