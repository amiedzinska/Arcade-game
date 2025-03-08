import pygame.font


class Button():
    def __init__(self, ai_game, screen, msg, y_offset=0, font_path=None):
        """Inicjalizacja atrybutów przycisku."""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        self.width, self.height = 250, 40      
        self.button_color = (255, 228, 225)     
        self.text_color = (47, 79, 79)
        self.font = pygame.font.Font(font_path, 35)             
        self.rect = pygame.Rect(0, 0, self.width, self.height) 
        self.rect.center = self.screen_rect.center
        self.rect.y += y_offset 
        self.shadow_color = (100, 100, 100)                     
        self._prep_msg(msg)                                    
    
    def _prep_msg(self, msg):
        """Umieszczenie komunikatu w wygenerowanym obrazie i wyśrodkowanie tekstu na przycisku."""
        self.msg_image = self.font.render(msg, True, self.text_color)       
        self.msg_image_rect = self.msg_image.get_rect()                   
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        shadow_rect = self.rect.copy()             
        shadow_rect.x += 5                         
        shadow_rect.y += 5                          
        pygame.draw.rect(self.screen, self.shadow_color, shadow_rect)      
        pygame.draw.rect(self.screen, self.button_color, self.rect)      
        self.screen.blit(self.msg_image, self.msg_image_rect)              
