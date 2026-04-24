import pygame
import time
import random

# Initializing pygame
pygame.init()

# Setting up colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)

# Screen dimensions
WIDTH = 600
HEIGHT = 400

# Initial game settings
BLOCK_SIZE = 10
INITIAL_SPEED = 15

# Creating the game window
dis = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game - Practice 10')

clock = pygame.time.Clock()

# Fonts for score and level display
score_font = pygame.font.SysFont("verdana", 20)

def display_status(score, level):
    """Displays current score and level on the screen"""
    value = score_font.render("Score: " + str(score) + "  Level: " + str(level), True, YELLOW)
    dis.blit(value, [10, 10])

def draw_snake(block_size, snake_list):
    """Draws each segment of the snake"""
    for x in snake_list:
        pygame.draw.rect(dis, GREEN, [x[0], x[1], block_size, block_size])

def gameLoop():
    game_over = False
    game_close = False

    # Snake starting position
    x1 = WIDTH / 2
    y1 = HEIGHT / 2

    # Movement variables
    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1
    
    score = 0
    level = 1
    current_speed = INITIAL_SPEED

    #Generate random position for food
    def get_random_food_pos():
        while True:
            foodx = round(random.randrange(0, WIDTH - BLOCK_SIZE) / 10.0) * 10.0
            foody = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / 10.0) * 10.0
            # Ensure food does not fall on the snake body
            if [foodx, foody] not in snake_List:
                return foodx, foody

    foodx, foody = get_random_food_pos()

    while not game_over:

        while game_close == True:
            dis.fill(BLUE)
            msg = score_font.render("You Lost! Press Q-Quit or C-Play Again", True, RED)
            dis.blit(msg, [WIDTH / 6, HEIGHT / 3])
            display_status(score, level)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -BLOCK_SIZE
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = BLOCK_SIZE
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -BLOCK_SIZE
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = BLOCK_SIZE
                    x1_change = 0

        #Checking for border collision (leaving the playing area)
        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            game_close = True
        
        x1 += x1_change
        y1 += y1_change
        dis.fill(BLACK)
        
        # Drawing food
        pygame.draw.rect(dis, RED, [foodx, foody, BLOCK_SIZE, BLOCK_SIZE])
        
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # Checking for self-collision
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        draw_snake(BLOCK_SIZE, snake_List)
        display_status(score, level) #Add counter to score and level

        pygame.display.update()

        # Logic for eating food
        if x1 == foodx and y1 == foody:
            foodx, foody = get_random_food_pos()
            Length_of_snake += 1
            score += 1
            
            #Add levels & 4. Increase speed
            # Level increases every 3 foods collected
            if score % 3 == 0:
                level += 1
                current_speed += 2 # Increase speed with level

        clock.tick(current_speed)

    pygame.quit()
    quit()

gameLoop()
