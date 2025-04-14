# engine/ai.py
import random
import math

class AIEngine:
    """Moduł do obsługi logiki sztucznej inteligencji."""
    def __init__(self):
        print("AIEngine zainicjalizowany (szkielet).")

    def update_agents(self, agents, player_pos, world_data, dt):
        """Aktualizuje stan i zachowanie agentów AI."""
        for agent in agents:
            if hasattr(agent, 'ai_state'):
                self.run_state_machine(agent, player_pos, world_data, dt)

    def run_state_machine(self, agent, player_pos, world_data, dt):
        """Przykładowa prosta maszyna stanów dla agenta."""
        if not hasattr(agent, 'position') or not hasattr(agent, 'velocity'):
             return # Agent musi mieć pozycję i prędkość

        distance_to_player = agent.position.distance_to(player_pos)

        # Przejścia między stanami
        if agent.ai_state == 'idle':
            if distance_to_player < agent.detection_radius:
                agent.ai_state = 'chasing'
        elif agent.ai_state == 'chasing':
            if distance_to_player > agent.chase_radius:
                agent.ai_state = 'idle'
            elif distance_to_player < agent.attack_radius:
                 agent.ai_state = 'attacking' # Przykładowy stan
        elif agent.ai_state == 'attacking':
             # Logika ataku, np. odliczanie czasu do następnego ataku
             if distance_to_player > agent.attack_radius: # Gracz uciekł
                 agent.ai_state = 'chasing'


        # Akcje w zależności od stanu
        if agent.ai_state == 'idle':
            # Stój w miejscu lub patroluj losowo (prosty przykład)
            agent.velocity = pygame.Vector2(0, 0)
            if random.random() < 0.01: # Mała szansa na zmianę kierunku
                agent.velocity.x = random.uniform(-agent.speed, agent.speed) * 0.5
                agent.velocity.y = random.uniform(-agent.speed, agent.speed) * 0.5

        elif agent.ai_state == 'chasing':
            # Poruszaj się w kierunku gracza
            direction = (player_pos - agent.position).normalize()
            agent.velocity = direction * agent.speed
        elif agent.ai_state == 'attacking':
             agent.velocity = pygame.Vector2(0,0) # Zatrzymaj się by atakować
             # Tutaj logika ataku (np. strzał, uderzenie)
             print(f"Agent {id(agent)} atakuje!")


    def find_path(self, start_pos, end_pos, grid_map):
        """Prosta implementacja algorytmu A* (lub innego) do znajdowania ścieżek."""
        # To jest złożony temat, wymaga implementacji algorytmu A*
        # na podstawie mapy świata (grid_map)
        print(f"AI: Znajdowanie ścieżki od {start_pos} do {end_pos} (niezaimplementowane)")
        return [] # Zwraca listę punktów (węzłów) na ścieżce