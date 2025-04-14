# engine/physics.py
import pygame

class PhysicsEngine:
    """Prosty silnik fizyki (głównie detekcja kolizji i ruch)."""
    def __init__(self, gravity=0.0): # Można dodać grawitację
        self.gravity = pygame.Vector2(0, gravity)
        print("PhysicsEngine zainicjalizowany.")
        # W bardziej zaawansowanej wersji można tu zainicjalizować Pymunk

    def update(self, objects, dt):
        """Aktualizuje pozycje obiektów na podstawie ich prędkości i grawitacji."""
        for obj in objects:
            if hasattr(obj, 'velocity') and hasattr(obj, 'rect'):
                # Zastosuj grawitację (jeśli istnieje)
                if self.gravity.y != 0.0 and hasattr(obj, 'apply_gravity') and obj.apply_gravity:
                     obj.velocity += self.gravity * dt

                # Zaktualizuj pozycję
                # Używamy wektorów dla precyzji, ale aktualizujemy rect (int)
                # Można przechowywać pozycję jako float i aktualizować rect
                if hasattr(obj, 'position') and isinstance(obj.position, pygame.Vector2):
                    obj.position += obj.velocity * dt
                    obj.rect.topleft = (int(obj.position.x), int(obj.position.y))
                else:
                    # Prostsza wersja bez wektorów float
                    obj.rect.x += int(obj.velocity.x * dt)
                    obj.rect.y += int(obj.velocity.y * dt)


    def check_collisions(self, objects_group1, objects_group2, callback=None):
        """Sprawdza kolizje między dwiema grupami obiektów."""
        collisions = []
        # Prosta kolizja AABB (Axis-Aligned Bounding Box)
        for obj1 in objects_group1:
            for obj2 in objects_group2:
                if obj1 != obj2 and hasattr(obj1, 'rect') and hasattr(obj2, 'rect'):
                    if obj1.rect.colliderect(obj2.rect):
                        collisions.append((obj1, obj2))
                        if callback:
                            callback(obj1, obj2) # Wywołaj funkcję zwrotną przy kolizji
        return collisions

    # Można dodać bardziej zaawansowane funkcje, np. resolve_collision