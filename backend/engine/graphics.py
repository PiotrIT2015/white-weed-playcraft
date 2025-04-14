# engine/graphics.py
import pygame
try:
    import config
except ImportError:
     class config:
        SCREEN_WIDTH = 800
        SCREEN_HEIGHT = 600
        TITLE = "Gra Pygame"

class GraphicsEngine:
    """Odpowiada za inicjalizację okna i rysowanie na ekranie."""
    def __init__(self):
        pygame.display.set_caption(config.TITLE)
        # Użyj HWACCEL i DOUBLEBUF dla lepszej wydajności
        self.screen = pygame.display.set_mode(
            (config.SCREEN_WIDTH, config.SCREEN_HEIGHT),
            pygame.HWSURFACE | pygame.DOUBLEBUF
        )
        self.clock = pygame.time.Clock()
        print("GraphicsEngine zainicjalizowany.")

    def clear_screen(self, color=(0, 0, 0)):
        """Wypełnia ekran jednolitym kolorem."""
        self.screen.fill(color)

    def render_sprite(self, surface, position):
        """Rysuje daną powierzchnię (sprite) w określonej pozycji."""
        self.screen.blit(surface, position)

    def render_game_objects(self, objects):
        """Rysuje listę obiektów gry (zakładając, że mają atrybut 'image' i 'rect')."""
        for obj in objects:
            if hasattr(obj, 'image') and hasattr(obj, 'rect'):
                self.screen.blit(obj.image, obj.rect.topleft)
            # Można dodać obsługę rysowania innych kształtów itp.

    def render_text(self, text, font, position, color=(255, 255, 255)):
        """Renderuje tekst na ekranie."""
        if font:
            text_surface = font.render(text, True, color)
            self.screen.blit(text_surface, position)
        else:
            print("Błąd: Próba renderowania tekstu bez załadowanej czcionki.")


    def update_display(self):
        """Aktualizuje zawartość całego ekranu."""
        pygame.display.flip() # Użyj flip() z DOUBLEBUF

    def tick(self, fps):
        """Ogranicza liczbę klatek na sekundę i zwraca czas delta."""
        # Zwraca czas w milisekundach od ostatniego wywołania
        # Dzielimy przez 1000.0, aby uzyskać sekundy (ważne dla fizyki)
        delta_time = self.clock.tick(fps) / 1000.0
        return delta_time