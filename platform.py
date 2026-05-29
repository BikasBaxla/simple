import pygame
import sys

pygame.init()

#---settings---
WIDTH, HEIGHT = 1000 , 800
FPS = 60
GRAVITY = 0.5
JUMP_STRENGTH = -15
PLAYER_SPEED = 5

WHITE = (255, 255, 0)
BLACK = (0, 0 , 0)
BLUE = (40, 200, 50)
GREEN = (50, 200, 50)
ORANGE = (255,165, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Platformer ")
clock = pygame.time.Clock()

#---platform class---
class Platform(pygame.sprite.Sprite):
    def __init__(self, x , y, w, h):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(topleft = (x, y))
        
class MovingPlatform(Platform):
    def __init__(self, x, y, w, h, dx= 0, dy = 0, distance = 200, speed = 2):
        super().__init__(x, y, w, h)
        self.start_x = x
        self.start_y = y
        self.dx = dx #horizontal
        self.dy = dy #vertical
        self.distance = distance
        self.speed = speed
        self.travelled = 0
        
    def update(self):
        move_x = self.dx * self.speed
        move_y = self.dy * self.speed
        self.rect.x += move_x
        self.rect.y += move_y
        self.travelled += abs(move_x) + abs(move_y)
        
        #reverse direction
        if self.travelled >= self.distance:
            self.dx *= -1
            self.dy *= -1
            self.travelled = 0  
           
        
#---Player class----
class Player(pygame.sprite.Sprite):
    def __init__(self, x ,y , platforms):
        super().__init__()
        self.image = pygame.Surface((60, 60), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 0, 0),(30, 30), 30)
        self.rect = self.image.get_rect(topleft=(x, y))
        
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.platforms = platforms
        
    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.vel_x = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
             self.vel_x = PLAYER_SPEED
        if(keys[pygame.K_SPACE] or keys[pygame.K_UP]) and self.on_ground:
            self.vel_y = JUMP_STRENGTH
            self.on_ground = False
            
    def apply_gravity(self):
        self.vel_y += GRAVITY
        if self.vel_y > 20:
            self.vel_y = 20
            
    def move_and_collide(self):
        #Horizontal movement
        self.rect.x += self.vel_x
        for platform in self.platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_x > 0:
                    self.rect.right = platform.rect.left
                elif self.vel_x < 0:
                    self.rect.left = platform.rect.right
                    
        #vertical movement
        self.rect.y += self.vel_y
        self.on_ground = False
        for platform in self.platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0: #falling
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0: #jumping up
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0
                    
        #ride moving platform
        for platform in self.platforms:
            if isinstance(platform, MovingPlatform):
                if self.rect.bottom == platform.rect.top:
                    self.rect.x += platform.dx * platform.speed
                    
                
        #death?reset if falls of screen
        if self.rect.top > HEIGHT:
            self.rect.topleft = (100, 100)
            self.vel_y = 0
            
    def update(self):
        self.handle_input()
        self.apply_gravity()
        self.move_and_collide()
        
#LOad level from file
def load_level(filename, tile_size = 40):
    platforms = pygame.sprite.Group()
    with open(filename, "r")as f:
        rows = f.readlines()
        
    for row_index , row in enumerate(rows):
        for col_index, title in enumerate(row.strip()):
            x = col_index * tile_size
            y = row_index * tile_size
            
            if title == "1":
                platforms.add(Platform(x ,y, tile_size, tile_size))
            if title == "2":
                platforms.add(MovingPlatform(x, y, tile_size, tile_size, dx= 1, dy=0, distance = 200, speed = 2))
            if title == "3":
                platforms.add(MovingPlatform(x, y, tile_size, tile_size, dx = 0, dy=1, distance = 150, speed =2))
                
    return platforms    
#---create level ---
platforms = load_level("level2.txt")
player = Player(100, 100, platforms)

all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(platforms)

        

#---Game loop---
running = True 
while running:
    dt = clock.tick(FPS) / 1000 # not used  heavily but good
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #update moving platform
    for platform in platforms:
        if isinstance(platform, MovingPlatform):
            platform.update()
    
    all_sprites.update()
    
    screen.fill(BLACK)
    all_sprites.draw(screen)
    pygame.display.flip()
    
pygame.quit()
sys.exit()


                

                    
                    
                
            

            
            
        
