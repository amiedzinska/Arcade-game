import pygame
from pygame.sprite import Sprite 


class Monster(Sprite):
    """Klasa przedstawiająca pojedynczego potwora."""

    def __init__(self, ai_game):
        """Inicjalizacja potwora i zdefiniowanie jego położenia początkowego."""
        super().__init__()
        self.screen = ai_game.screen               
        self.settings = ai_game.settings            
        self.image = pygame.image.load('./images/monster.bmp')      
        self.rect = self.image.get_rect()           
        self.rect.x = self.rect.width              
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)                

    def check_edges(self):
        """Zwraca wartość True, jeśli potwór znajduje się przy krawędzi ekranu."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:     
            return True                                                     


    def update(self):
        """Przesunięcie potwora w prawo lub w lewo."""
        self.x += (self.settings.monster_speed * self.settings.enemies_direction)       
        self.rect.x = self.x                                                           

        