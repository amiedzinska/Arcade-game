import sys
from time import sleep
import pygame
from pygame import mixer
from src.settings import Settings
from src.game_stats import GameStats
from src.scoreboard import Scoreboard
from src.button import Button
from character import Character
from src.bullet import Bullet
from src.monster import Monster


class GeraltofRivia:
    """Ogólna klasa przeznaczona do zarządzania zasobami i sposobem działania gry."""

    def __init__(self):
        """Inicjalizacja gry i utworzenie jej zasobów."""
        pygame.init()
        mixer.init()                        
        self.settings = Settings()          
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))        
        self.original_caption = "Geralt of Rivia"
        self.current_caption = self.original_caption       
        self.stats = GameStats(self)                        
        self.sb = Scoreboard(self)                          
        self.character = Character(self)                    
        self.bullets = pygame.sprite.Group()
        self.monsters = pygame.sprite.Group()               
        self._create_enemies()                              
        self.play_button = Button(self, self.screen, "Start", font_path='./fonts/Thewitcher-jnOj.ttf')
        self.instructions_button = Button(self, self.screen, "How to play", y_offset=80, font_path='./fonts/Thewitcher-jnOj.ttf')  
        self.about_button = Button(self, self.screen, "Author", y_offset=160, font_path='./fonts/Thewitcher-jnOj.ttf')  
        font_path = './fonts/Thewitcher-jnOj.ttf'  
        self.game_over_font = pygame.font.Font(font_path, 70) 
        self.music = "./music/witcher.mp3"
        mixer.music.load(self.music)                        
        self.bullet_sound = mixer.Sound("./music/bullet.mp3")
        self.bg_image = pygame.image.load('./images/background.jpg')       

    def play_music(self):
        mixer.music.play(-1)

    def run_game(self):
        """Rozpoczęcie pętli głównej gry."""
        self.play_music()                   
        while True:
            self._check_events()            
            if self.stats.game_active:
                self.character.update()     
                self._update_bullets()
                self._update_monsters()
            self._update_screen()

    def _check_events(self):
        """Reakcja na zdarzenia generowane przez klawiaturę i mysz."""
        for event in pygame.event.get():                    
            if event.type == pygame.QUIT:                  
                sys.exit()
            elif event.type == pygame.KEYDOWN:              
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:                
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:     
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                self._check_instructions_button(mouse_pos)  
                self._check_about_button(mouse_pos) 

    def _check_play_button(self, mouse_pos):
        """Rozpoczęcie nowej gry po kliknięciu przycisku 'Play' przez użytkownika."""   
        button_clicked = self.play_button.rect.collidepoint(mouse_pos) 
        if button_clicked and not self.stats.game_active:                   
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_characters()
            self.monsters.empty()
            self.bullets.empty()
            self._create_enemies()
            self.character.center_character()
            pygame.mouse.set_visible(False) 
    
    def _check_instructions_button(self, mouse_pos):
        """Wyświetlenie instrukcji gry po kliknięciu przycisku 'How to play'."""
        if not self.stats.game_active:                                 
            button_clicked = self.instructions_button.rect.collidepoint(mouse_pos)
            if button_clicked:
                self.show_instructions()

    def show_instructions(self):
        """Wyświetlenie okna z instrukcjami gry."""
        instructions_screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))        
        pygame.display.set_caption("How to play")
        while True:                                                     
            instructions_screen.fill((230, 230, 230))
            font_path = './fonts/Thewitcher-jnOj.ttf'
            font = pygame.font.Font(font_path, 38)
            instructions = [
                "How to play:",
                "1. Push the arrow keys to move.",
                "2. Press spacebar to fire the bullets.",
                "3. Avoid collisions with the monsters.",
                "4. Shoot minotaurs to score points.",
                "5. The game ends when the monsters touch",
                "   the bottom of the screen or collide with you.",
                "6. Press Q to turn the game off.",
                "   Press Esc to go back to the main page."
            ]
            y_offset = 50
            for line in instructions:
                text_image = font.render(line, True, (0, 0, 0))
                instructions_screen.blit(text_image, (20, y_offset))
                y_offset += 50
            pygame.display.flip()
            for event in pygame.event.get():                            
                if event.type == pygame.QUIT:                           
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                    
    def _check_about_button(self, mouse_pos): 
        """Wyświetlenie informacji o autorze po kliknięciu przycisku 'Author'."""
        if not self.stats.game_active:                                 
            button_clicked = self.about_button.rect.collidepoint(mouse_pos)
            if button_clicked:
                self.current_caption = pygame.display.get_caption()[0] 
                self.show_about()
            if not self.stats.game_active:  
                pygame.mouse.set_visible(True)  
            
    def show_about(self):   
        """Wyświetlenie informacji o autorze."""
        about_screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))     
        pygame.display.set_caption("Author")
        while True:
            about_screen.fill((230, 230, 230))
            font_path = './fonts/Thewitcher-jnOj.ttf'
            font = pygame.font.Font(font_path, 38)
            about_text = [
                "Game made by: Aleksandra Miedzinska",
                "Index: ",
                "Press Esc to go back to the main page."
            ]
            y_offset = 50                           
            for line in about_text:
                text_image = font.render(line, True, (0, 0, 0))
                about_screen.blit(text_image, (20, y_offset))
                y_offset += 50
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return

    def _check_keydown_events(self, event):
        """Reakcja na naciśnięcie klawisza."""          
        if event.key == pygame.K_RIGHT:                 
            self.character.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.character.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Reakcja na zwolnienie klawisza."""
        if event.key == pygame.K_RIGHT:
            self.character.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.character.moving_left = False
            self.screen.fill(self.settings.bg_color)
            self.character.blitme()

    def _fire_bullet(self):
        """Utworzenie nowego pocisku i dodanie go do grupy pocisków."""
        if len(self.bullets) < self.settings.bullets_allowed:                   
            new_bullet = Bullet(self)                                           
            self.bullets.add(new_bullet)                                       
            self.bullet_sound.play()                                            

    def _update_bullets(self):
        """Uaktualnienie położenia pocisków i usunięcie tych niewidocznych na ekranie."""
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:        
                self.bullets.remove(bullet)
        collisions = pygame.sprite.groupcollide(self.bullets, self.monsters, False, True)       
        if collisions:
            for monsters in collisions.values():
                self.stats.score += self.settings.monster_points * len(monsters)        
            self.sb.prep_score()                                                        
            self.sb.check_high_score()                                                  

        if not self.monsters:
            self.bullets.empty()
            self._create_enemies()
            self.settings.increase_speed()
            self.stats.level += 1
            self.sb.prep_level()

    def _update_monsters(self):
        """Sprawdzenie, czy potwory znajdują się przy krawędzi, a następnie uaktualnienie ich położenia."""
        self._check_enemies_edges()         
        self.monsters.update()              
        if pygame.sprite.spritecollideany(self.character, self.monsters):               
            self._character_hit()                                                       
        self._check_monsters_bottom()                                                   

    def _character_hit(self):
        """Reakcja na uderzenie potwora w postać."""
        if self.stats.characters_left > 0:      
            self.stats.characters_left -= 1     
            self.sb.prep_characters()
            self.monsters.empty()
            self.bullets.empty()
            self._create_enemies()
            self.character.center_character()  
            sleep(0.5)                         
        else:
            self.stats.game_active = False      
            pygame.mouse.set_visible(True)      

    def _create_enemies(self):
        """Utworzenie wszystkich potworów."""
        monster = Monster(self)                
        monster_width, monster_height = monster.rect.size       
        available_space_x = self.settings.screen_width - (2 * monster_width)        
        number_monsters_x = available_space_x // (2 * monster_width)              
        character_height = self.character.rect.height                               
        available_space_y = (self.settings.screen_height - (3 * monster_height) - character_height)         
        number_rows = available_space_y // (2 * monster_height)                                             
        for row_number in range(number_rows):                                                              
            for monster_number in range(number_monsters_x):                                                
                self._create_monster(monster_number, row_number)                                       

    def _create_monster(self, monster_number, row_number):
        """Utworzenie potwora i umieszczenie go w rzędzie."""
        monster = Monster(self)
        monster_width, monster_height = monster.rect.size                   
        monster.x = monster_width + 2 * monster_width * monster_number      
        monster.rect.x = monster.x                                          
        monster.rect.y = monster.rect.height + 2 * monster.rect.height * row_number
        self.monsters.add(monster)                                         

    def _check_monsters_bottom(self):
        """Sprawdzenie, czy którykolwiek potwór dotarł do dolnej krawędzi ekranu."""
        screen_rect = self.screen.get_rect()                               
        for monster in self.monsters.sprites():
            if monster.rect.bottom >= screen_rect.bottom:                   
                self._character_hit()                                       
                break   

    def _check_enemies_edges(self):
        """Odpowiednia reakcja, gdy potwór dotrze do krawędzi ekranu."""
        for monster in self.monsters.sprites():             
            if monster.check_edges():                                       
                self._change_enemies_direction()                            
                break

    def _change_enemies_direction(self):
        """Przesunięcie wszystkich potworów w dół i zmiana kierunku, w którym się poruszają."""
        for monster in self.monsters.sprites():                             
            monster.rect.y += self.settings.enemies_drop_speed             
        self.settings.enemies_direction *= -1                               

    def _show_game_over(self): 
            """Wyświetlenie napisu "YOU LOST"."""
            game_over_text = self.game_over_font.render("YOU LOST", True, (253, 245, 230))
            game_over_rect = game_over_text.get_rect()                      
            game_over_rect.center = (self.settings.screen_width // 2, self.settings.screen_height // 4)
            self.screen.blit(game_over_text, game_over_rect)                

    def _update_screen(self):
        """Uaktualnienie obrazów na ekranie i przejście do nowego ekranu."""
        self.screen.blit(self.bg_image, (0, 0))  
        self.character.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.monsters.draw(self.screen)
        self.sb.show_score()

        if not self.stats.game_active:
            pygame.display.set_caption(self.current_caption)        
            self.play_button.draw_button()                          
            self.instructions_button.draw_button() 
            self.about_button.draw_button() 
            if self.stats.characters_left == 0: 
                self._show_game_over()                             
        pygame.display.flip()                                       

if __name__ == '__main__':
    ai = GeraltofRivia()
    ai.run_game()