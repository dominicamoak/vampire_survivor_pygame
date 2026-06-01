from settings import *
from player import Player
from sprites import *
from groups import AllSprites
from pytmx.util_pygame import load_pygame
from random import randint


class Game():
    def __init__(self):
        # General Setup
        pygame.init()
        pygame.display.set_caption('VAMPIRE SURVIVOR')
        
        self.running = True
        self.clock = pygame.time.Clock()
        
        # Surfaces / Imports
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        
        # Groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        
        self.setup()
    
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
    
    # Run
    def run(self):
        while self.running:
            self.game_events = pygame.event.get()
            dt = self.clock.tick() / 1000
            
            # Event Loop
            for event in self.game_events:
                if event.type == pygame.QUIT:
                    self.running = False
            
            # Updates
            self.all_sprites.update(dt)
            
            # Draw Game
            self.display_surface.fill('#276938')
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()
            
        pygame.quit()



if __name__ == '__main__':
    game = Game()
    game.run()


