# engine/game_object.py
import pygame

class GameObject(pygame.sprite.Sprite):
    """Bazowa klasa dla wszystkich obiektów w grze."""
    def __init__(self, x=0, y=0, image_surface=None):
        super().__init__() # Ważne dla używania w grupach sprite'ów Pygame

        # Grafika
        self.image = image_surface
        if self.image:
            self.rect = self.image.get_rect(topleft=(x, y))
        else:
            # Utwórz domyślny rect, jeśli nie ma obrazka
            self.rect = pygame.Rect(x, y, 32, 32) # Przykładowy rozmiar

        # Fizyka
        self.position = pygame.Vector2(x, y) # Dokładna pozycja (float)
        self.velocity = pygame.Vector2(0, 0)
        self.apply_gravity = True # Czy grawitacja ma działać na ten obiekt

        # AI (przykładowe atrybuty)
        self.ai_state = 'idle'
        self.speed = 100 # Piksele na sekundę
        self.detection_radius = 200
        self.chase_radius = 250
        self.attack_radius = 50


    def update(self, dt):
        """Metoda aktualizacji logiki obiektu (może być nadpisana przez klasy dziedziczące)."""
        # Domyślnie nic nie robi, fizyka jest obsługiwana przez PhysicsEngine
        pass

    def draw(self, surface):
        """Rysuje obiekt na podanej powierzchni (zwykle ekranie)."""
        if self.image:
            surface.blit(self.image, self.rect.topleft)