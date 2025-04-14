# game/player.py
import pygame
from engine.game_object import GameObject
from engine.resource_manager import ResourceManager # Załóżmy instancję globalną lub przekazaną

class Player(GameObject):
    def __init__(self, x, y, resource_manager):
        player_img = resource_manager.get_image("player.png")
        super().__init__(x, y, player_img)

        self.speed = 200 # Piksele na sekundę
        self.jump_strength = 400
        self.on_ground = False # Prosty wskaźnik, czy gracz jest na ziemi
        self.resource_manager = resource_manager # Przechowaj referencję
        self.jump_sound = self.resource_manager.get_sound("jump.mp3")
        # Wyłącz domyślną grawitację AI dla gracza
        # self.ai_state = None # Gracz nie potrzebuje stanu AI

    def handle_input(self, pressed_keys):
        """Obsługuje sterowanie graczem."""
        self.velocity.x = 0
        if pressed_keys[pygame.K_LEFT] or pressed_keys[pygame.K_a]:
            self.velocity.x = -self.speed
        if pressed_keys[pygame.K_RIGHT] or pressed_keys[pygame.K_d]:
            self.velocity.x = self.speed

        # Skok (prosty przykład - wymaga poprawy o sprawdzanie podłoża)
        # if pressed_keys[pygame.K_SPACE] and self.on_ground:
        #     self.velocity.y = -self.jump_strength
        #     self.on_ground = False # Zresetuj po skoku
             # sound_engine.play_sound(self.jump_sound) # Wymaga dostępu do sound_engine

    def update(self, dt):
        """Specyficzna logika aktualizacji dla gracza."""
        # Tutaj można dodać animacje, logikę strzelania itp.
        # Kolizje i ruch podstawowy są obsługiwane przez silnik fizyki
        pass

    # Można nadpisać draw, jeśli potrzebne jest specjalne rysowanie
    # def draw(self, surface):
    #     super().draw(surface)