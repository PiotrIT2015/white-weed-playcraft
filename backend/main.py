# main.py
import pygame # Importuj pygame tutaj, aby upewnić się, że jest dostępne globalnie
from game.game_logic import Game

if __name__ == '__main__':
    print("Uruchamianie silnika gry...")
    try:
        game = Game()
        game.run()
    except Exception as e:
        print(f"\nWystąpił nieoczekiwany błąd: {e}")
        # W środowisku produkcyjnym można zapisać błąd do pliku logu
        import traceback
        traceback.print_exc() # Wydrukuj pełny ślad stosu
    finally:
        # Upewnij się, że pygame zostanie zamknięte nawet po błędzie
        if pygame.get_init():
            pygame.quit()
        print("Aplikacja zakończona.")