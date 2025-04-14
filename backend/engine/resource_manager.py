# engine/resource_manager.py
import pygame
import os
# Można zaimportować config, jeśli istnieje
try:
    import config
except ImportError:
    # Domyślne wartości, jeśli config.py nie istnieje
    class config:
        IMAGE_DIR = "assets/images"
        SOUND_DIR = "assets/sounds"
        FONT_DIR = "assets/fonts"

class ResourceManager:
    """Zarządza ładowaniem i przechowywaniem zasobów (obrazy, dźwięki, czcionki)."""
    def __init__(self):
        self._images = {}
        self._sounds = {}
        self._fonts = {}
        print("ResourceManager zainicjalizowany.")

    def get_image(self, filename, use_alpha=True):
        """Ładuje obraz lub zwraca z pamięci podręcznej."""
        if filename not in self._images:
            path = os.path.join(config.IMAGE_DIR, filename)
            try:
                image = pygame.image.load(path)
                if use_alpha:
                    # Optymalizuje obraz do wyświetlania z przezroczystością
                    image = image.convert_alpha()
                else:
                    # Optymalizuje obraz bez przezroczystości
                    image = image.convert()
                self._images[filename] = image
                print(f"Załadowano obraz: {path}")
            except pygame.error as e:
                print(f"Błąd ładowania obrazu '{path}': {e}")
                # Można zwrócić domyślny obraz błędu lub rzucić wyjątek
                return None # Lub np. pustą powierzchnię
        return self._images[filename]

    def get_sound(self, filename):
        """Ładuje dźwięk lub zwraca z pamięci podręcznej."""
        if filename not in self._sounds:
            path = os.path.join(config.SOUND_DIR, filename)
            try:
                sound = pygame.mixer.Sound(path)
                self._sounds[filename] = sound
                print(f"Załadowano dźwięk: {path}")
            except pygame.error as e:
                print(f"Błąd ładowania dźwięku '{path}': {e}")
                return None
        return self._sounds[filename]

    def get_font(self, filename, size):
        """Ładuje czcionkę lub zwraca z pamięci podręcznej."""
        key = (filename, size)
        if key not in self._fonts:
            path = os.path.join(config.FONT_DIR, filename)
            try:
                font = pygame.font.Font(path, size)
                self._fonts[key] = font
                print(f"Załadowano czcionkę: {path} (rozmiar: {size})")
            except pygame.error as e:
                print(f"Błąd ładowania czcionki '{path}': {e}")
                return None
            except FileNotFoundError:
                 print(f"Nie znaleziono pliku czcionki '{path}', używam domyślnej.")
                 # Użyj domyślnej czcionki systemowej Pygame
                 font = pygame.font.Font(None, size)
                 self._fonts[key] = font

        return self._fonts[key]

    def clear_cache(self):
        """Czyści pamięć podręczną zasobów (przydatne przy zmianie poziomu)."""
        self._images.clear()
        self._sounds.clear()
        self._fonts.clear()
        print("Pamięć podręczna zasobów wyczyszczona.")

# Można stworzyć globalną instancję, jeśli preferujesz łatwy dostęp
# resource_manager = ResourceManager()