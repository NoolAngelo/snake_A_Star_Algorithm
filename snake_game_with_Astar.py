from pygame import display, time, draw, QUIT, init, KEYDOWN, K_a, K_s, K_d, K_w, K_ESCAPE
from random import randint
import pygame
import sys
from numpy import sqrt

# Initialize pygame
init()

# Game configuration
GAME_CONFIG = {
    'cols': 25,
    'rows': 25, 
    'width': 600,
    'height': 600,
    'fps': 12,
    'obstacle_probability': 3
}

# Game state variables
done = False
score = 0
game_over = False

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (128, 128, 128)

# Game dimensions
cols = GAME_CONFIG['cols']
rows = GAME_CONFIG['rows']
width = GAME_CONFIG['width']
height = GAME_CONFIG['height']
wr = width / cols
hr = height / rows

# Game setup
screen = display.set_mode([width, height])
display.set_caption("Snake A* Algorithm - Autonomous Pathfinding Game")
clock = time.Clock()


# Enhanced A* algorithm with error handling and optimization
def getpath(food1, snake1):
    """
    Improved A* pathfinding algorithm with better error handling
    Returns path directions or empty list if no path found
    """
    if not food1 or not snake1:
        return []
    
    # Reset previous pathfinding data
    food1.camefrom = []
    for s in snake1:
        s.camefrom = []
    
    # Initialize sets for A* algorithm
    openset = [snake1[-1]]  # Start from snake head
    closedset = []
    dir_array1 = []
    max_iterations = cols * rows  # Prevent infinite loops
    iterations = 0

    # Main A* algorithm loop
    while openset and iterations < max_iterations:
        iterations += 1
        
        # Find node with lowest f score
        current1 = min(openset, key=lambda x: x.f)

        # Move current from open to closed set
        openset = [node for node in openset if node != current1]
        closedset.append(current1)

        # Check if we reached the goal
        if current1 == food1:
            break

        # Examine each neighbor
        for neighbor in current1.neighbors:
            # Skip if neighbor is blocked
            if (neighbor in closedset or 
                neighbor.obstrucle or 
                neighbor in snake1):
                continue
                
            # Calculate tentative g score
            tentative_g = current1.g + 1
            
            # Update neighbor if better path found
            if neighbor not in openset:
                openset.append(neighbor)
                neighbor.g = tentative_g
            elif tentative_g < neighbor.g:
                neighbor.g = tentative_g
            else:
                continue  # This path is not better
                
            # Calculate heuristic and total cost
            neighbor.h = sqrt((neighbor.x - food1.x) ** 2 + (neighbor.y - food1.y) ** 2)
            neighbor.f = neighbor.g + neighbor.h
            neighbor.camefrom = current1
    
    # Reconstruct path if goal was reached
    if current1 == food1:
        while current1.camefrom:
            # Determine direction based on movement
            if current1.x == current1.camefrom.x and current1.y < current1.camefrom.y:
                dir_array1.append(2)  # up
            elif current1.x == current1.camefrom.x and current1.y > current1.camefrom.y:
                dir_array1.append(0)  # down
            elif current1.x < current1.camefrom.x and current1.y == current1.camefrom.y:
                dir_array1.append(3)  # left
            elif current1.x > current1.camefrom.x and current1.y == current1.camefrom.y:
                dir_array1.append(1)  # right
            current1 = current1.camefrom
    
    # Reset node data for next pathfinding
    for i in range(rows):
        for j in range(cols):
            grid[i][j].camefrom = []
            grid[i][j].f = 0
            grid[i][j].h = 0
            grid[i][j].g = 0
            
    return dir_array1


class Spot:
    """Enhanced Spot class with better initialization and validation"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.f = 0
        self.g = 0
        self.h = 0
        self.neighbors = []
        self.camefrom = []
        # Generate obstacles with configured probability
        self.obstrucle = randint(1, 101) < GAME_CONFIG['obstacle_probability']

    def show(self, color):
        """Draw the spot on screen with proper positioning"""
        draw.rect(screen, color, [
            self.x * hr + 2, 
            self.y * wr + 2, 
            hr - 4, 
            wr - 4
        ])

    def add_neighbors(self):
        """Add valid neighbors to this spot"""
        # Check all four directions
        if self.x > 0:
            self.neighbors.append(grid[self.x - 1][self.y])
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y - 1])
        if self.x < rows - 1:
            self.neighbors.append(grid[self.x + 1][self.y])
        if self.y < cols - 1:
            self.neighbors.append(grid[self.x][self.y + 1])


def initialize_game():
    """Initialize the game grid, snake, and food"""
    global grid, snake, food, current, dir_array
    
    # Create and setup grid
    grid = [[Spot(i, j) for j in range(cols)] for i in range(rows)]
    for i in range(rows):
        for j in range(cols):
            grid[i][j].add_neighbors()

    # Initialize snake at center
    snake = [grid[rows // 2][cols // 2]]
    
    # Place food avoiding obstacles and snake
    food = place_food()
    current = snake[-1]
    dir_array = getpath(food, snake)

def place_food():
    """Place food in a valid location"""
    attempts = 0
    max_attempts = 100
    
    while attempts < max_attempts:
        x, y = randint(0, rows - 1), randint(0, cols - 1)
        potential_food = grid[x][y]
        
        if not potential_food.obstrucle and potential_food not in snake:
            return potential_food
        attempts += 1
    
    # Fallback: find any empty spot
    for i in range(rows):
        for j in range(cols):
            if not grid[i][j].obstrucle and grid[i][j] not in snake:
                return grid[i][j]
    
    return grid[0][0]  # Last resort

def draw_ui():
    """Draw the user interface elements"""
    # Display score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    # Display game title
    title_font = pygame.font.Font(None, 24)
    title_text = title_font.render("Snake A* Algorithm", True, GRAY)
    screen.blit(title_text, (10, height - 30))

def handle_movement():
    """Handle snake movement with improved error checking"""
    global current, score, dir_array, food
    
    if not dir_array:
        # No path available, try to recalculate
        dir_array = getpath(food, snake)
        if not dir_array:
            return False  # Game over - no path possible
    
    direction = dir_array.pop(-1)
    next_x, next_y = current.x, current.y
    
    # Calculate next position
    if direction == 0:  # down
        next_y += 1
    elif direction == 1:  # right
        next_x += 1
    elif direction == 2:  # up
        next_y -= 1
    elif direction == 3:  # left
        next_x -= 1
    
    # Boundary checking
    if (next_x < 0 or next_x >= rows or 
        next_y < 0 or next_y >= cols):
        return False  # Game over - hit boundary
    
    next_spot = grid[next_x][next_y]
    
    # Collision checking
    if next_spot.obstrucle or next_spot in snake:
        return False  # Game over - collision
    
    # Move snake
    snake.append(next_spot)
    current = snake[-1]

    # Check if food was eaten
    if current == food:
        score += 1
        food = place_food()
        dir_array = getpath(food, snake)
    else:
        snake.pop(0)  # Remove tail if no food eaten
    
    return True

# Initialize game
initialize_game()

# Main game loop
while not done:
    clock.tick(GAME_CONFIG['fps'])
    screen.fill(BLACK)
    
    # Handle movement and check for game over
    if not handle_movement():
        game_over = True
    
    # Draw game elements
    for spot in snake:
        spot.show(WHITE)
    
    for i in range(rows):
        for j in range(cols):
            if grid[i][j].obstrucle:
                grid[i][j].show(RED)

    food.show(GREEN)
    snake[-1].show(BLUE)  # Highlight snake head
    
    # Draw UI
    draw_ui()
    
    # Display game over message
    if game_over:
        font = pygame.font.Font(None, 48)
        game_over_text = font.render("GAME OVER", True, RED)
        text_rect = game_over_text.get_rect(center=(width//2, height//2))
        screen.blit(game_over_text, text_rect)
        
        restart_text = font.render("Press R to restart", True, WHITE)
        restart_rect = restart_text.get_rect(center=(width//2, height//2 + 50))
        screen.blit(restart_text, restart_rect)

    display.flip()
    
    # Handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                done = True
            elif event.key == pygame.K_r and game_over:
                # Restart game
                score = 0
                game_over = False
                initialize_game()

pygame.quit()
sys.exit()
