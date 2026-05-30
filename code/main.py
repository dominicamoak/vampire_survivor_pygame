from settings import *

# General Setup
pygame.init()
pygame.display.set_caption('VAMPIRE SURVIVOR')

class Game():
    def __init__(self):
        self.running = True
        self.clock = pygame.time.Clock()
        
        # Surfaces / Imports
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        
        # Sprites
        self.all_sprites = pygame.sprite.Group()
        self.player = Player(self.all_sprites)
    
    def run(self):
        while self.running:
            self.game_events = pygame.event.get()
            self.dt = self.clock.tick(60) / 1000
            self.events()
            self.update()
            self.draw()
        
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




class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('images', 'player', 'down', f'{0}.png')).convert_alpha()
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.direction = pygame.Vector2()
        self.speed = 300
            
    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt

game = Game()
game.run()


pygame.quit()

