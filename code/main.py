from settings import *
from player import Player
from sprites import *
from groups import AllSprites

from pytmx.util_pygame import load_pygame
from random import randint, choice

### Still to add
# player health
# player score

class Game():
    def __init__(self):
        # General Setup
        pygame.init()
        pygame.display.set_caption('VAMPIRE SURVIVOR')
        
        self.running = True
        self.clock = pygame.time.Clock()
        self.game_state = 'start_menu'
        self.previous_state = 'none'
        self.player_score = 0
        self.final_score = 0
        self.player_life = 5
        self.menu_font = pygame.font.Font(join('data', 'Oxanium-Bold.ttf'), 75)
        self.final_score_font = pygame.font.Font(join('data', 'Oxanium-Bold.ttf'), 40)
        self.other_font = pygame.font.Font(join('data', 'Oxanium-Bold.ttf'), 30)
        
        # Surfaces / Imports
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        
        # Groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        
        # Gun Timer
        self.can_shoot = True
        self.shoot_time = 0
        self.gun_resttime = 100
        
        # Enemy Timer
        self.enemy_event = pygame.event.custom_type()
        pygame.time.set_timer(self.enemy_event, 750)
        self.appear_pos = []
        
        # Game Sounds
        self.impact_sound = pygame.mixer.Sound(join('audio', 'impact.ogg'))
        self.impact_sound.set_volume(0.5)
        self.game_music = pygame.mixer.Sound(join('audio', 'music.wav'))
        self.game_music.play(loops = -1)
        self.shoot_sound = pygame.mixer.Sound(join('audio', 'shoot.wav'))
        self.shoot_sound.set_volume(0.3)
        
        self.load_images()
        self.setup()
    
    # Load Images
    def load_images(self):
        self.bullet_surf = pygame.image.load(join('images', 'gun', 'bullet.png')).convert_alpha()
        
        folders = list(walk(join('images', 'enemies')))[0][1]
        self.enemy_frames = {}
        for folder in folders:
            for folder_path, _, file_names in walk(join('images', 'enemies', folder)):
                self.enemy_frames[folder] = []
                for file_name in sorted(file_names, key = lambda name: int(name.split('.')[0])):
                    full_path = join(folder_path, file_name)
                    surf = pygame.image.load(full_path).convert_alpha()
                    self.enemy_frames[folder].append(surf)
    
    # Inputs
    def input(self):
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            self.shoot_sound.play()
            pos = self.gun.rect.center + self.gun.player_direction * 50
            self.bullet = Bullet((self.all_sprites, self.bullet_sprites), self.bullet_surf, pos, self.gun.player_direction)
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()
    
    # Gun Timer
    def gun_timer(self):
        if not self.can_shoot:
            gun_current_time = pygame.time.get_ticks()
            if gun_current_time - self.shoot_time >= self.gun_resttime:
                self.can_shoot = True
    
    # Scene Setup
    def setup(self):
        map = load_pygame(join('data', 'maps', 'world.tmx'))
        for x, y, image in map.get_layer_by_name('Ground').tiles():
            Sprite(self.all_sprites, (x * TILE_SIZE, y * TILE_SIZE), image)
        
        for obj in map.get_layer_by_name('Objects'):
            CollisionSprite((self.all_sprites, self.collision_sprites), (obj.x, obj.y), obj.image)
        
        for block in map.get_layer_by_name('Collisions'):
            CollisionSprite((self.collision_sprites), (block.x, block.y), pygame.Surface((block.width, block.height)))
        
        for entity in map.get_layer_by_name('Entities'):
            if entity.name == 'Player':
                self.player = Player(self.all_sprites, (entity.x, entity.y), self.collision_sprites)
                self.gun = Gun(self.all_sprites, self.player)
            if entity.name == 'Enemy':
                self.appear_pos.append((entity.x, entity.y))
    
    # Start Menu Screen
    def start_menu(self): # will add event parameter soon
        mouse_pos = pygame.mouse.get_pos()
        self.text_color = '#eba038'
        start_game_surf = self.menu_font.render('Start Game', True, self.text_color)
        start_game_rect = start_game_surf.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 400))
        exit_game_surf = self.menu_font.render('Exit', True, self.text_color)
        exit_game_rect = exit_game_surf.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 300))
        
        if start_game_rect.collidepoint(mouse_pos):
            self.text_color = '#ffffff'
            start_game_surf = self.menu_font.render('Start Game', True, self.text_color)
            start_game_surf = pygame.transform.scale_by(start_game_surf, 1.2)
        if exit_game_rect.collidepoint(mouse_pos):
            self.text_color = '#ffffff'
            exit_game_surf = self.menu_font.render('Exit', True, self.text_color)
            exit_game_surf = pygame.transform.scale_by(exit_game_surf, 1.2)
        
        start_game_rect = start_game_surf.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 400))
        exit_game_rect = exit_game_surf.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 300))
        
        self.display_surface.blit(start_game_surf, start_game_rect)
        self.display_surface.blit(exit_game_surf, exit_game_rect)
        
        for event in self.game_events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_game_rect.collidepoint(mouse_pos):
                    self.init_game()
                    self.game_state = 'playing'
                if exit_game_rect.collidepoint(mouse_pos):
                    self.running = False
    
    def end_menu(self):
        mouse_pos = pygame.mouse.get_pos()
        self.text_color = '#eba038'
        start_game_surf = self.menu_font.render('Play Again', True, self.text_color)
        start_game_rect = start_game_surf.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 400))
        exit_game_surf = self.menu_font.render('Exit', True, self.text_color)
        exit_game_rect = exit_game_surf.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 300))
        
        if start_game_rect.collidepoint(mouse_pos):
            self.text_color = '#ffffff'
            start_game_surf = self.menu_font.render('Play Again', True, self.text_color)
            start_game_surf = pygame.transform.scale_by(start_game_surf, 1.2)
        if exit_game_rect.collidepoint(mouse_pos):
            self.text_color = '#ffffff'
            exit_game_surf = self.menu_font.render('Exit', True, self.text_color)
            exit_game_surf = pygame.transform.scale_by(exit_game_surf, 1.2)
        
        start_game_rect = start_game_surf.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 400))
        exit_game_rect = exit_game_surf.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 300))
        
        self.display_surface.blit(start_game_surf, start_game_rect)
        self.display_surface.blit(exit_game_surf, exit_game_rect)
        
        for event in self.game_events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_game_rect.collidepoint(mouse_pos):
                    self.init_game()
                    self.game_state = 'playing'
                if exit_game_rect.collidepoint(mouse_pos):
                    self.running = False
    
    # Initialize Game
    def init_game(self):
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.player_score = 0
        self.player_life = 5
        
        self.load_images()
        self.setup()
    
    # Game Music
    def game_sound(self, new_state):
        if new_state == 'playing' or new_state == 'start_menu':
            self.game_music.set_volume(0.2)
        elif new_state == 'game_over':
            self.game_music.set_volume(0.05)
    
    # Bullet Collisions
    def bullet_collisions(self):
        if self.bullet_sprites:
            for bullet in self.bullet_sprites:
                collision_sprites = pygame.sprite.spritecollide(bullet, self.enemy_sprites, False, pygame.sprite.collide_mask)
                if collision_sprites:
                    self.impact_sound.play()
                    for sprite in collision_sprites:
                        sprite.take_damage()
                    bullet.kill()
    
    # Player Collisions
    def player_collisions(self):
        if pygame.sprite.spritecollide(self.player, self.enemy_sprites, True, pygame.sprite.collide_mask):
            self.player_life = self.player_life - 1
        if self.player_life == 0:
            self.game_state = 'game_over'
    
    def add_score(self, amount):
        self.player_score += amount
        self.final_score = self.player_score
    
    # Score Display during Game
    def display_score(self, score):
        self.text_color = '#ffffff'
        text_surf = self.other_font.render(('Score: ' + str(score)), True, self.text_color)
        text_rect = text_surf.get_frect(topright = (WINDOW_WIDTH - 75, 75))
        self.display_surface.blit(text_surf, text_rect)
        
        pygame.draw.rect(self.display_surface, '#ffffff', text_rect.inflate(30, 30).move(0, -8), 5, 10)
    
    # Fianl Score Display
    def display_final_score(self, score):
        self.text_color = '#ffffff'
        text_surf = self.final_score_font.render(('Final Score: ' + str(score)), True, self.text_color)
        text_rect = text_surf.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 500))
        self.display_surface.blit(text_surf, text_rect)
    
    # Player Health Display during Game
    def display_life(self, life):
        self.text_color = '#ffffff'
        text_surf = self.other_font.render(('Health: ' + str(life)), True, self.text_color)
        text_rect = text_surf.get_frect(topleft = (75, 75))
        self.display_surface.blit(text_surf, text_rect)
        
        pygame.draw.rect(self.display_surface, '#ffffff', text_rect.inflate(30, 30).move(0, -8), 5, 10)
    
    # Run
    def run(self):
        while self.running:
            self.game_events = pygame.event.get()
            
            if self.game_state != self.previous_state:
                self.game_sound(self.game_state)
                self.previous_state = self.game_state
            
            elif self.game_state == 'start_menu':
                self.display_surface.fill('#276938')
                self.start_menu() # will be passing game_events
                pygame.display.update()
            
            elif self.game_state == 'playing':
                dt = self.clock.tick() / 1000
                
                # Event Loop
                for event in self.game_events:
                    if event.type == pygame.QUIT:
                        self.running = False
                    if event.type == self.enemy_event:
                        Enemy((self.all_sprites, self.enemy_sprites), choice(list(self.enemy_frames.values())), choice(self.appear_pos), self.player, self.collision_sprites, self.add_score)
                
                # Updates
                self.gun_timer()
                self.input()
                self.all_sprites.update(dt)
                self.bullet_collisions()
                self.player_collisions()
                
                # Draw Game
                self.display_surface.fill('#276938')
                self.all_sprites.draw(self.player.rect.center)
                self.display_score(self.player_score)
                self.display_life(self.player_life)
                pygame.display.update()
            
            elif self.game_state == 'game_over':
                self.display_surface.fill('#276938')
                self.display_final_score(self.final_score)
                self.end_menu()
                pygame.display.update()
            
        pygame.quit()



if __name__ == '__main__':
    game = Game()
    game.run()


