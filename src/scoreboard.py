import pygame.font
from pygame.sprite import Group
from character import Character 


class Scoreboard:
    """Klasa przeznaczona do przedstawiania informacji o punktacji."""

    def __init__(self, ai_game): 
        """Inicjalizacja atrybutów dotyczących punktacji."""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        self.text_color = (253, 245, 230) 
        self.font_path = './fonts/Thewitcher-jnOj.ttf' 
        self.font = pygame.font.Font(self.font_path, 40)        
        self.prep_score()                                       
        self.prep_high_score()                                 
        self.prep_level()                                     
        self.prep_characters()                                  

    def prep_score(self):
        """Przekształcenie punktacji na wygenerowany obraz."""
        rounded_score = round(self.stats.score, -1)
        score_str = "Score: {:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color)   
        self.score_rect = self.score_image.get_rect()                           
        self.score_rect.right = self.screen_rect.right - 20                     
        self.score_rect.top = 20

    def prep_high_score(self):
        """Konwersja najlepszego wyniku w grze na wygenerowany obraz."""
        high_score = round(self.stats.high_score, -1) 
        high_score_str = "Highest score: {:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx 
        self.high_score_rect.top = self.score_rect.top 

    def prep_level(self):
        """Konwersja numeru poziomu na wygenerowany obraz."""
        level_str = "Level: " + str(self.stats.level) 
        self.level_image = self.font.render(level_str, True, self.text_color) 
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right 
        self.level_rect.top = self.score_rect.bottom + 10 

    def prep_characters(self):   
        """Wyświetla liczbę żyć, jakie pozostały graczowi."""
        self.characters = Group()                                              
        for character_number in range(self.stats.characters_left):             
            character = Character(self.ai_game)                                
            character.image = pygame.image.load(self.stats.life_image)         
            character.rect.x = 10 + character_number * character.rect.width     
            character.rect.y = 10 
            self.characters.add(character)                                     

    def check_high_score(self):
        """Sprawdzenie, czy mamy nowy najlepszy wynik osiągnięty dotąd w grze."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()
            
    def show_score(self):
        """Wyświetlenie na ekranie punktacji, poziomu oraz żyć."""
        self.screen.blit(self.score_image, self.score_rect)            
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect) 
        self.characters.draw(self.screen)                              

