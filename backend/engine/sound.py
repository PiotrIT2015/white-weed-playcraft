# engine/sound.py
import pygame

class SoundEngine:
    """Odpowiada za inicjalizację i odtwarzanie dźwięków oraz muzyki."""
    def __init__(self, frequency=44100, size=-16, channels=2, buffer=2048):
        try:
            pygame.mixer.init(frequency, size, channels, buffer)
            print("SoundEngine zainicjalizowany.")
            self._music_playing = False
        except pygame.error as e:
            print(f"Błąd inicjalizacji SoundEngine (mixer): {e}")
            print("Dźwięk będzie niedostępny.")
            pygame.mixer.quit() # Upewnij się, że mixer jest wyłączony

    def play_sound(self, sound_object, loops=0):
        """Odtwarza załadowany obiekt dźwiękowy."""
        if sound_object and pygame.mixer.get_init(): # Sprawdź, czy mixer działa
            sound_object.play(loops)

    def load_music(self, filepath):
         """Ładuje plik muzyczny do odtwarzania strumieniowego."""
         if pygame.mixer.get_init():
             try:
                 pygame.mixer.music.load(filepath)
                 print(f"Załadowano muzykę: {filepath}")
             except pygame.error as e:
                 print(f"Błąd ładowania muzyki '{filepath}': {e}")


    def play_music(self, loops=-1): # -1 oznacza pętlę nieskończoną
        """Odtwarza załadowaną muzykę."""
        if pygame.mixer.get_init() and not self._music_playing:
            try:
                pygame.mixer.music.play(loops)
                self._music_playing = True
            except pygame.error as e:
                 print(f"Błąd odtwarzania muzyki: {e}")


    def stop_music(self):
        """Zatrzymuje odtwarzanie muzyki."""
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()
            self._music_playing = False

    def set_music_volume(self, volume): # volume: 0.0 to 1.0
         """Ustawia głośność muzyki."""
         if pygame.mixer.get_init():
             pygame.mixer.music.set_volume(volume)

    def set_sound_volume(self, sound_object, volume): # volume: 0.0 to 1.0
        """Ustawia głośność konkretnego dźwięku."""
        if sound_object and pygame.mixer.get_init():
            sound_object.set_volume(volume)