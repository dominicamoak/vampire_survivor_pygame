from settings import *
from player import *


class Game():
    def __init__(self):
        # General Setup
        pygame.init()
        pygame.display.set_caption('VAMPIRE SURVIVOR')
        
        self.running = True
        self.clock = pygame.time.Clock()
        
        # Surfaces / Imports
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        
        # Sprites
        self.all_sprites = pygame.sprite.Group()
        self.player = Player(self.all_sprites, (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
    
    def run(self):
        while self.running:
            self.game_events = pygame.event.get()
            self.dt = self.clock.tick(60) / 1000
            self.events()
            self.update()
            self.draw()
            
        pygame.quit()
        
    # Event Loop
    def events(self):
        for event in self.game_events:
            if event.type == pygame.QUIT:
                self.running = False
    
    # Updates
    def update(self):
        self.all_sprites.update(self.dt)
        
    # Draw Game
    def draw(self):
        self.display_surface.fill('#276938')
        self.all_sprites.draw(self.display_surface)

        pygame.display.update()



if __name__ == '__main__':
    game = Game()
    game.run()


