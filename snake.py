import pygame
import random

pygame.init()

#screen
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

#COLOR
WHITE = (255,255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

#Snake setting
snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]
direction = "RIGHT"
change_to = direction

#food
food_pos = [random.randrange(1, (WIDTH//10)) * 10,random.randrange(1, (HEIGHT//10)) * 10]
food_spawn = True

#Speed
clock = pygame.time.Clock()
speed = 15

#Score
score = 0

def show_score():
    font = pygame.font.SysFont("Arial", 20)
    score_surface = font.render(f"Score: {score} ", True, WHITE)
    screen.blit(score_surface, (10, 10))

#game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


        #key controls
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction  != "DOWN":
                change_to = "UP"
            elif event.key == pygame.K_DOWN and direction  != "UP":
                change_to = "DOWN"
            elif event.key == pygame.K_LEFT and direction  != "RIGHT":
                change_to = "LEFT"
            elif event.key == pygame.K_RIGHT and direction  != "LEFT":
                change_to = "RIGHT"

    direction = change_to

    #MOVE snake
    if direction == "UP":
        snake_pos[1] -= 10
    if direction == "DOWN":
        snake_pos[1] += 10
    if direction == "LEFT":
        snake_pos[0] -= 10
    if direction == "RIGHT":
        snake_pos[0] += 10

    snake_body.insert(0, list(snake_pos))

    # eating food
    if snake_pos == food_pos:
        score += 1
        food_spawn = False
    else:
        snake_body.pop()

    if not food_spawn:
        food_post = [random.randrange(1, (WIDTH//10)) * 10, random.randrange(1, (HEIGHT//10)) * 10]
    food_spawn = True

    #background
    screen.fill(BLACK)
      
    #DRAWSNAKE
    for block in snake_body:
         pygame.draw.rect(screen, GREEN, pygame.Rect(block[0], block[1], 10, 20))

    # draw food
    pygame.draw.rect(screen, RED, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

     # game over condition
    if snake_pos[0] < 0 or snake_pos[0]> WIDTH-10:
         running = False
    if snake_pos[1] < 0 or snake_pos[1]> HEIGHT-10:
         running = False

      #self collision
    for block in snake_body[1:]:
        if snake_pos == block:
            running = False

    show_score()
    pygame.display.update()
    clock.tick(speed)

pygame.quit()

    
    
     
    
    
               
               






    
    
    
               
               






    