import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """Klasa przeznaczona do zarządzania pociskami wystrzeliwanymi przez postać."""
    
    def __init__(self, ai_game):
        """Utworzenie obiektu pocisku w aktualnym położeniu postaci."""
        super().__init__()                          
        self.screen = ai_game.screen              
        self.settings = ai_game.settings            
        self.color = self.settings.bullet_color     

        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)  
        self.rect.midtop = ai_game.character.rect.midtop      
        self.y = float(self.rect.y)                             

    def update(self):
        """Poruszanie pociskiem po ekranie."""
        self.y -= self.settings.bullet_speed    
        self.rect.y = self.y                    

    def draw_bullet(self):
        """Wyświetlenie pocisku na ekranie."""
        pygame.draw.rect(self.screen, self.color, self.rect)   
