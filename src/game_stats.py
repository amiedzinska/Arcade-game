class GameStats:
    """Monitorowanie danych statystycznych w grze „Geralt of Rivia”."""
    
    def __init__(self, ai_game):
        """Inicjalizacja danych statystycznych."""
        self.settings = ai_game.settings       
        self.reset_stats()                   
        self.game_active = False                
        self.high_score = 0                   
        self.life_image = './images/life.bmp'

    def reset_stats(self):
        """Inicjalizacja danych statystycznych, które mogą zmieniać się w trakcie gry."""
        self.characters_left = self.settings.character_limit       
        self.score = 0                                              
        self.level = 1                                              
