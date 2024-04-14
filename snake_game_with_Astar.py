from pygame import display, time, draw, QUIT, init, KEYDOWN, K_a, K_s, K_d, K_w
from random import randint
import pygame
from numpy import sqrt

init()

done = False
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

cols = 25
rows = 25

width = 600
height = 600
wr = width / cols
hr = height / rows
direction = 1
score = 0  # Initialize score

screen = display.set_mode([width, height])
display.set_caption("snake_self")
clock = time.Clock()


# The A* algorithm is implemented in the getpath function
def getpath(food1, snake1):
    # Initialize the open and closed sets
    food1.camefrom = []
    for s in snake1:
        s.camefrom = []
    openset = [snake1[-1]]
    closedset = []
    dir_array1 = []

    # Main loop of the A* algorithm
    while 1:
        # Find the node in the open set with the lowest f score
        current1 = min(openset, key=lambda x: x.f)

        # Remove the current node from the open set and add it to the closed set
        openset = [openset[i] for i in range(len(openset)) if not openset[i] == current1]
        closedset.append(current1)

        # For each neighbor of the current node
        for neighbor in current1.neighbors:
            # If the neighbor is not in the closed set and is not an obstacle and is not in the snake
            if neighbor not in closedset and not neighbor.obstrucle and neighbor not in snake1:
                # Calculate the tentative g score for the neighbor
                tempg = neighbor.g + 1
                # If the neighbor is in the open set and the tentative g score is less than the neighbor's current g score
                if neighbor in openset:
                    if tempg < neighbor.g:
                        # Update the neighbor's g score
                        neighbor.g = tempg
                else:
                    # If the neighbor is not in the open set, set its g score to the tentative g score and add it to the open set
                    neighbor.g = tempg
                    openset.append(neighbor)
                # Calculate the h and f scores for the neighbor
                neighbor.h = sqrt((neighbor.x - food1.x) ** 2 + (neighbor.y - food1.y) ** 2)
                neighbor.f = neighbor.g + neighbor.h
                neighbor.camefrom = current1
        # If the current node is the goal, exit the loop
        if current1 == food1:
            break
    # After the loop, construct the path from the goal to the start by following the parent pointers
    while current1.camefrom:
        if current1.x == current1.camefrom.x and current1.y < current1.camefrom.y:
            dir_array1.append(2)
        elif current1.x == current1.camefrom.x and current1.y > current1.camefrom.y:
            dir_array1.append(0)
        elif current1.x < current1.camefrom.x and current1.y == current1.camefrom.y:
            dir_array1.append(3)
        elif current1.x > current1.camefrom.x and current1.y == current1.camefrom.y:
            dir_array1.append(1)
        current1 = current1.camefrom
    # print(dir_array1)
    # Reset the f, g, and h scores and the parent pointers for all nodes
    for i in range(rows):
        for j in range(cols):
            grid[i][j].camefrom = []
            grid[i][j].f = 0
            grid[i][j].h = 0
            grid[i][j].g = 0
    return dir_array1


class Spot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.f = 0
        self.g = 0
        self.h = 0
        self.neighbors = []
        self.camefrom = []
        self.obstrucle = False
        if randint(1, 101) < 3:
            self.obstrucle = True

    def show(self, color):
        draw.rect(screen, color, [self.x * hr + 2, self.y * wr + 2, hr - 4, wr - 4])

    def add_neighbors(self):
        if self.x > 0:
            self.neighbors.append(grid[self.x - 1][self.y])
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y - 1])
        if self.x < rows - 1:
            self.neighbors.append(grid[self.x + 1][self.y])
        if self.y < cols - 1:
            self.neighbors.append(grid[self.x][self.y + 1])


grid = [[Spot(i, j) for j in range(cols)] for i in range(rows)]

for i in range(rows):
    for j in range(cols):
        grid[i][j].add_neighbors()

snake = [grid[round(rows / 2)][round(cols / 2)]]
food = grid[randint(0, rows - 1)][randint(0, cols - 1)]
current = snake[-1]
dir_array = getpath(food, snake)
food_array = [food]

while not done:
    clock.tick(12)
    screen.fill(BLACK)
    direction = dir_array.pop(-1)
    if direction == 0:  # down
        snake.append(grid[current.x][current.y + 1])
    elif direction == 1:  # right
        snake.append(grid[current.x + 1][current.y])
    elif direction == 2:  # up
        snake.append(grid[current.x][current.y - 1])
    elif direction == 3:  # left
        snake.append(grid[current.x - 1][current.y])
    current = snake[-1]

    if current.x == food.x and current.y == food.y:
        score += 1  # Increase score when snake eats food
        while 1:
            food = grid[randint(0, rows - 1)][randint(0, cols - 1)]
            if not (food.obstrucle or food in snake):
                break
        food_array.append(food)
        dir_array = getpath(food, snake)
    else:
        snake.pop(0)

    for spot in snake:
        spot.show(WHITE)
    for i in range(rows):
        for j in range(cols):
            if grid[i][j].obstrucle:
                grid[i][j].show(RED)

    food.show(GREEN)
    snake[-1].show(BLUE)
    
    # Display score
    font = pygame.font.Font(None, 36)
    text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(text, (10, 10))

    display.flip()
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True
        elif event.type == KEYDOWN:
            if event.key == K_w and not direction == 0:
                direction = 2
            elif event.key == K_a and not direction == 1:
                direction = 3
            elif event.key == K_s and not direction == 2:
                direction = 0
            elif event.key == K_d and not direction == 3:
                direction = 1
