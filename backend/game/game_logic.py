# game/game_logic.py
import pygame
from engine.graphics import GraphicsEngine
from engine.physics import PhysicsEngine
from engine.sound import SoundEngine
from engine.ai import AIEngine
from engine.resource_manager import ResourceManager
# Importuj obiekty gry
from game.player import Player
# from game.enemy import Enemy # Przykład
try:
    import config
except ImportError:
     class config:
        SCREEN_WIDTH = 800
        SCREEN_HEIGHT = 600
        FPS = 60
        TITLE = "Gra Pygame"
        FONT_DIR = "assets/fonts" # Potrzebne dla czcionki

class Game:
    """Główna klasa zarządzająca logiką gry i pętlą główną."""
    def __init__(self):
        pygame.init() # Inicjalizacja wszystkich modułów Pygame

        # Inicjalizacja modułów silnika
        self.resource_manager = ResourceManager()
        self.graphics = GraphicsEngine()
        self.physics = PhysicsEngine(gravity=800) # Dodajmy trochę grawitacji
        self.sound = SoundEngine()
        self.ai = AIEngine()

        # Stan gry
        self.is_running = False
        self.game_objects = pygame.sprite.Group() # Grupa dla łatwiejszego zarządzania
        self.player = None
        self.enemies = pygame.sprite.Group()

        # Załaduj podstawowe zasoby
        self.font = self.resource_manager.get_font("basic_font.ttf", 24) # Przykładowa czcionka

    def initialize_level(self):
        """Konfiguruje początkowy stan gry/poziomu."""
        self.game_objects.empty() # Wyczyść poprzednie obiekty
        self.enemies.empty()

        # Stwórz gracza
        self.player = Player(100, config.SCREEN_HEIGHT - 100, self.resource_manager)
        self.game_objects.add(self.player)

        # Stwórz przeciwników (przykład)
        # enemy = Enemy(500, config.SCREEN_HEIGHT - 100, self.resource_manager)
        # self.game_objects.add(enemy)
        # self.enemies.add(enemy)

        print("Poziom zainicjalizowany.")
        # Załaduj i odtwórz muzykę tła
        # music_path = os.path.join(config.SOUND_DIR, "background_music.ogg") # Przykład
        # self.sound.load_music(music_path)
        # self.sound.play_music()


    def run(self):
        """Główna pętla gry."""
        self.initialize_level()
        self.is_running = True
        delta_time = 0 # Czas od ostatniej klatki (w sekundach)

        while self.is_running:
            # 1. Obsługa zdarzeń (Input)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                # Można dodać obsługę innych zdarzeń (np. kliknięcia myszą)
                # if event.type == pygame.KEYDOWN:
                #    if event.key == pygame.K_SPACE:
                #        # Obsługa skoku - lepiej w handle_input gracza
                #        pass

            # Pobierz stan klawiszy (dla ciągłego ruchu)
            pressed_keys = pygame.key.get_pressed()
            if self.player:
                self.player.handle_input(pressed_keys) # Przekaż stan klawiszy do gracza

            # 2. Aktualizacja logiki (Update)
            # Aktualizuj wszystkie obiekty gry (w tym gracza)
            self.game_objects.update(delta_time)

            # Aktualizuj AI (przekazując pozycję gracza)
            player_pos = self.player.position if self.player else pygame.Vector2(0,0)
            self.ai.update_agents(self.enemies, player_pos, None, delta_time) # World data na razie None

            # Aktualizuj fizykę (ruch i grawitacja)
            self.physics.update(self.game_objects, delta_time)

            # Sprawdź kolizje (przykład: gracz vs przeciwnicy)
            # collisions = self.physics.check_collisions([self.player], self.enemies)
            # for player, enemy in collisions:
            #    print("Kolizja gracza z przeciwnikiem!")
               # Tutaj logika obrażeń, itp.

            # Proste ograniczenie ekranu dla gracza
            if self.player:
                 if self.player.rect.left < 0:
                     self.player.rect.left = 0
                     self.player.position.x = 0
                     self.player.velocity.x = 0
                 if self.player.rect.right > config.SCREEN_WIDTH:
                     self.player.rect.right = config.SCREEN_WIDTH
                     self.player.position.x = config.SCREEN_WIDTH - self.player.rect.width
                     self.player.velocity.x = 0
                 # Proste "podłoże"
                 if self.player.rect.bottom > config.SCREEN_HEIGHT - 20: # 20px marginesu od dołu
                     self.player.rect.bottom = config.SCREEN_HEIGHT - 20
                     self.player.position.y = self.player.rect.top
                     self.player.velocity.y = 0
                     self.player.on_ground = True # Jest na ziemi (uproszczenie)
                 else:
                     self.player.on_ground = False


            # 3. Rysowanie (Render)
            self.graphics.clear_screen((20, 20, 80)) # Ciemnoniebieskie tło

            # Rysuj wszystkie obiekty gry
            self.graphics.render_game_objects(self.game_objects)

            # Rysuj dodatkowe elementy UI (np. FPS)
            fps_text = f"FPS: {self.graphics.clock.get_fps():.1f}"
            self.graphics.render_text(fps_text, self.font, (10, 10), (255, 255, 0))

            # Aktualizuj wyświetlacz
            self.graphics.update_display()

            # 4. Ograniczenie FPS i pobranie delta_time
            delta_time = self.graphics.tick(config.FPS)

        self.quit()

    def quit(self):
        """Zamyka Pygame i kończy działanie."""
        print("Zamykanie gry...")
        pygame.quit()