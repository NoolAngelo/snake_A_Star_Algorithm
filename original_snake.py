import pygame
import time
import random

pygame.init()

# Colors
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Screen dimensions
dis_width = 800
dis_height = 600

# Snake block size and speed
snake_block = 20
snake_speed = 15

# Fonts
font_style = pygame.font.SysFont(None, 50)

# Clock
clock = pygame.time.Clock()

# Initialize screen
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game')

# Score
def Your_score(score):
    value = font_style.render("Your Score: " + str(score), True, black)
    dis.blit(value, [0, 0])

# Draw snake
def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, green, [x[0], x[1], snake_block, snake_block])

# Message display
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])

# Game over message
def game_over_msg():
    message("You Lost! Press Space to Play Again or Q to Quit", red)

# Main game loop
def gameLoop():
    game_over = False
    game_close = False

    while not game_over:

        while game_close == True:
            dis.fill(blue)
            game_over_msg()
            Your_score(Length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_SPACE:
                        gameLoop()

        # Initial snake position
        x1 = dis_width / 2
        y1 = dis_height / 2

        # Initial change in position
        x1_change = snake_block
        y1_change = 0

        # Snake body
        snake_List = []
        Length_of_snake = 1

        # Randomly position food
        foodx = round(random.randrange(0, dis_width - snake_block) / snake_block) * snake_block
        foody = round(random.randrange(0, dis_height - snake_block) / snake_block) * snake_block

        game_close = False

        while not game_close:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and x1_change == 0:
                        x1_change = -snake_block
                        y1_change = 0
                    elif event.key == pygame.K_RIGHT and x1_change == 0:
                        x1_change = snake_block
                        y1_change = 0
                    elif event.key == pygame.K_UP and y1_change == 0:
                        y1_change = -snake_block
                        x1_change = 0
                    elif event.key == pygame.K_DOWN and y1_change == 0:
                        y1_change = snake_block
                        x1_change = 0

            # Teleport the snake when it hits the screen boundary
            if x1 >= dis_width:
                x1 = 0
            elif x1 < 0:
                x1 = dis_width - snake_block
            elif y1 >= dis_height:
                y1 = 0
            elif y1 < 0:
                y1 = dis_height - snake_block

            x1 += x1_change
            y1 += y1_change
            dis.fill(blue)

            # Draw snake
            snake_Head = []
            snake_Head.append(x1)
            snake_Head.append(y1)
            snake_List.append(snake_Head)
            if len(snake_List) > Length_of_snake:
                del snake_List[0]

            # Check if snake hits itself
            for x in snake_List[:-1]:
                if x == snake_Head:
                    game_close = True

            # Draw snake
            our_snake(snake_block, snake_List)

            # Draw food
            pygame.draw.rect(dis, red, [foodx, foody, snake_block, snake_block])

            # Update display
            Your_score(Length_of_snake - 1)
            pygame.display.update()

            # If snake eats food
            if x1 == foodx and y1 == foody:
                foodx = round(random.randrange(0, dis_width - snake_block
                                               ) / snake_block) * snake_block
                foody = round(random.randrange(0, dis_height - snake_block) / snake_block) * snake_block
                Length_of_snake += 1

            # FPS
            clock.tick(snake_speed)

        pygame.quit()
        quit()

gameLoop()
