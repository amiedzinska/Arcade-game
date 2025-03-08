class Settings:
    """Klasa przeznaczona do przechowywania wszystkich ustawień gry."""
    
    def __init__(self):
        """Inicjalizacja ustawień gry."""
        self.screen_width = 1000       
        self.screen_height = 530
        self.bg_color = (154, 205, 50)

        self.character_speed = 1.5
        self.character_limit = 3

        self.bullet_width = 3
        self.bullet_height = 18
        self.bullet_color = (250, 235, 215)
        self.bullets_allowed = 3

        self.enemies_drop_speed = 8
        self.speedup_scale = 1.1 
        self.score_scale = 1.5 
        self.initialize_dynamic_settings() 

    def initialize_dynamic_settings(self):
        """Inicjalizacja ustawień, które ulegają zmianie w trakcie gry."""
        self.character_speed = 1.5
        self.bullet_speed = 3.0
        self.monster_speed = 0.3
        self.enemies_direction = 1  
        self.monster_points = 50

    def increase_speed(self):
        """Zmiana ustawień dotyczących szybkości gry u liczby przyznawanych punktów."""
        self.character_speed *= self.speedup_scale      
        self.bullet_speed *= self.speedup_scale
        self.monster_speed *= self.speedup_scale
        self.monster_points = int(self.monster_points * self.score_scale)   
        
        