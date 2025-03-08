import pygame
from pygame.sprite import Sprite 


class Character(Sprite):
    """Klasa przeznaczona do zarządzania postacią."""
    
    def __init__(self, ai_game):                
        """Inicjalizacja postaci i jego położenie początkowe."""
        super().__init__() 
        self.screen = ai_game.screen                    
        self.settings = ai_game.settings               
        self.screen_rect = ai_game.screen.get_rect()   
        self.image = pygame.image.load('./images/character.bmp')   
        self.rect = self.image.get_rect()                           
        self.rect.midbottom = self.screen_rect.midbottom           
        self.x = float(self.rect.x)                                 
        self.moving_right = False                                  
        self.moving_left = False

    def update(self): 
        """Uaktualnienie położenia postaci na podstawie opcji wskazującej na jego ruch."""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.character_speed                             
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.character_speed

        self.rect.x = self.x                                                  

    def blitme(self): 
        """Wyświetlenie postaci w jego aktualnym położeniu."""
        self.screen.blit(self.image, self.rect)


    def center_character(self):
        """Umieszczenie postaci na środku przy dolnej krawędzi ekranu."""
        self.rect.midbottom = self.screen_rect.midbottom                        
        self.x = float(self.rect.x)                                             