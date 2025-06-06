#!/usr/bin/env python3
"""
Manual Snake Game - Traditional WASD Controls
A classic Snake game implementation with manual controls for comparison with the A* version.
Features: WASD movement, pause functionality, game menu, and score tracking.
"""

import pygame
import sys
import random
from enum import Enum

# Initialize pygame
pygame.init()

# Game configuration
GAME_CONFIG = {
    'cols': 25,
    'rows': 25,
    'width': 600,
    'height': 600,
    'fps': 8,  # Slower for manual control
    'obstacle_probability': 2  # Fewer obstacles for manual play
}

# Game states
class GameState(Enum):
    MENU = 1
    PLAYING = 2
    PAUSED = 3
    GAME_OVER = 4

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (128, 128, 128)
YELLOW = (255, 255, 0)
DARK_GREEN = (0, 128, 0)

# Game dimensions
cols = GAME_CONFIG['cols']
rows = GAME_CONFIG['rows']
width = GAME_CONFIG['width']
height = GAME_CONFIG['height']
cell_width = width // cols
cell_height = height // rows

# Initialize screen
screen = pygame.display.set_mode([width, height])
pygame.display.set_caption("Snake Game - Manual Control (WASD)")
clock = pygame.time.Clock()

# Direction constants
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Snake:
    """Snake class for managing snake body and movement"""
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        """Reset snake to initial state"""
        start_x = cols // 2
        start_y = rows // 2
        self.body = [(start_x, start_y)]
        self.direction = RIGHT
        self.grow_pending = False
    
    def move(self):
        """Move snake in current direction"""
        head_x, head_y = self.body[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        
        self.body.insert(0, new_head)
        
        if not self.grow_pending:
            self.body.pop()
        else:
            self.grow_pending = False
    
    def grow(self):
        """Mark snake to grow on next move"""
        self.grow_pending = True
    
    def get_head(self):
        """Get snake head position"""
        return self.body[0]
    
    def check_collision(self):
        """Check if snake collided with walls or itself"""
        head_x, head_y = self.get_head()
        
        # Check wall collision
        if head_x < 0 or head_x >= cols or head_y < 0 or head_y >= rows:
            return True
        
        # Check self collision
        if self.get_head() in self.body[1:]:
            return True
        
        return False
    
    def draw(self, surface):
        """Draw snake on the surface"""
        for i, (x, y) in enumerate(self.body):
            color = BLUE if i == 0 else WHITE  # Head is blue, body is white
            rect = pygame.Rect(x * cell_width, y * cell_height, cell_width, cell_height)
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, BLACK, rect, 1)  # Border

class Food:
    """Food class for managing food placement and rendering"""
    
    def __init__(self):
        self.position = self.generate_position()
    
    def generate_position(self):
        """Generate random food position"""
        return (random.randint(0, cols - 1), random.randint(0, rows - 1))
    
    def respawn(self, snake_body):
        """Respawn food at new location avoiding snake"""
        while True:
            new_pos = self.generate_position()
            if new_pos not in snake_body:
                self.position = new_pos
                break
    
    def draw(self, surface):
        """Draw food on the surface"""
        x, y = self.position
        rect = pygame.Rect(x * cell_width, y * cell_height, cell_width, cell_height)
        pygame.draw.rect(surface, GREEN, rect)
        pygame.draw.rect(surface, DARK_GREEN, rect, 2)

class Game:
    """Main game class managing game state and logic"""
    
    def __init__(self):
        self.state = GameState.MENU
        self.score = 0
        self.high_score = 0
        self.snake = Snake()
        self.food = Food()
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
    
    def reset_game(self):
        """Reset game to initial state"""
        if self.score > self.high_score:
            self.high_score = self.score
        self.score = 0
        self.snake.reset()
        self.food.respawn(self.snake.body)
        self.state = GameState.PLAYING
    
    def handle_input(self, event):
        """Handle keyboard input based on game state"""
        if event.type == pygame.KEYDOWN:
            if self.state == GameState.MENU:
                self.handle_menu_input(event.key)
            elif self.state == GameState.PLAYING:
                self.handle_game_input(event.key)
            elif self.state == GameState.PAUSED:
                self.handle_pause_input(event.key)
            elif self.state == GameState.GAME_OVER:
                self.handle_game_over_input(event.key)
    
    def handle_menu_input(self, key):
        """Handle input in menu state"""
        if key == pygame.K_SPACE:
            self.reset_game()
        elif key == pygame.K_q or key == pygame.K_ESCAPE:
            return False
        return True
    
    def handle_game_input(self, key):
        """Handle input during gameplay (WASD movement)"""
        # Movement controls (WASD)
        if key == pygame.K_w and self.snake.direction != DOWN:
            self.snake.direction = UP
        elif key == pygame.K_s and self.snake.direction != UP:
            self.snake.direction = DOWN
        elif key == pygame.K_a and self.snake.direction != RIGHT:
            self.snake.direction = LEFT
        elif key == pygame.K_d and self.snake.direction != LEFT:
            self.snake.direction = RIGHT
        
        # Game controls
        elif key == pygame.K_p or key == pygame.K_SPACE:
            self.state = GameState.PAUSED
        elif key == pygame.K_q or key == pygame.K_ESCAPE:
            self.state = GameState.MENU
        
        return True
    
    def handle_pause_input(self, key):
        """Handle input in paused state"""
        if key == pygame.K_p or key == pygame.K_SPACE:
            self.state = GameState.PLAYING
        elif key == pygame.K_q or key == pygame.K_ESCAPE:
            self.state = GameState.MENU
        return True
    
    def handle_game_over_input(self, key):
        """Handle input in game over state"""
        if key == pygame.K_r or key == pygame.K_SPACE:
            self.reset_game()
        elif key == pygame.K_q or key == pygame.K_ESCAPE:
            self.state = GameState.MENU
        return True
    
    def update(self):
        """Update game logic"""
        if self.state != GameState.PLAYING:
            return
        
        # Move snake
        self.snake.move()
        
        # Check collision
        if self.snake.check_collision():
            self.state = GameState.GAME_OVER
            return
        
        # Check food collision
        if self.snake.get_head() == self.food.position:
            self.score += 1
            self.snake.grow()
            self.food.respawn(self.snake.body)
    
    def draw_menu(self):
        """Draw main menu"""
        screen.fill(BLACK)
        
        # Title
        title_text = self.font_large.render("SNAKE GAME", True, WHITE)
        title_rect = title_text.get_rect(center=(width // 2, height // 3))
        screen.blit(title_text, title_rect)
        
        # Subtitle
        subtitle_text = self.font_medium.render("Manual Control Edition", True, GRAY)
        subtitle_rect = subtitle_text.get_rect(center=(width // 2, height // 3 + 50))
        screen.blit(subtitle_text, subtitle_rect)
        
        # Instructions
        instructions = [
            "Press SPACE to Start",
            "W/A/S/D - Move",
            "P - Pause",
            "Q/ESC - Menu/Quit",
            f"High Score: {self.high_score}"
        ]
        
        start_y = height // 2 + 20
        for i, instruction in enumerate(instructions):
            color = YELLOW if i == 0 else WHITE
            text = self.font_small.render(instruction, True, color)
            text_rect = text.get_rect(center=(width // 2, start_y + i * 30))
            screen.blit(text, text_rect)
    
    def draw_game(self):
        """Draw game elements"""
        screen.fill(BLACK)
        
        # Draw snake and food
        self.snake.draw(screen)
        self.food.draw(screen)
        
        # Draw score
        score_text = self.font_medium.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        # Draw high score
        high_score_text = self.font_small.render(f"High: {self.high_score}", True, GRAY)
        screen.blit(high_score_text, (10, 50))
        
        # Draw controls hint
        controls_text = self.font_small.render("P-Pause | Q-Menu", True, GRAY)
        screen.blit(controls_text, (width - 150, 10))
    
    def draw_pause(self):
        """Draw pause screen"""
        self.draw_game()  # Draw game in background
        
        # Semi-transparent overlay
        overlay = pygame.Surface((width, height))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        # Pause text
        pause_text = self.font_large.render("PAUSED", True, WHITE)
        pause_rect = pause_text.get_rect(center=(width // 2, height // 2))
        screen.blit(pause_text, pause_rect)
        
        # Instructions
        resume_text = self.font_medium.render("Press P to Resume", True, YELLOW)
        resume_rect = resume_text.get_rect(center=(width // 2, height // 2 + 50))
        screen.blit(resume_text, resume_rect)
        
        menu_text = self.font_small.render("Press Q for Menu", True, WHITE)
        menu_rect = menu_text.get_rect(center=(width // 2, height // 2 + 80))
        screen.blit(menu_text, menu_rect)
    
    def draw_game_over(self):
        """Draw game over screen"""
        screen.fill(BLACK)
        
        # Game Over text
        game_over_text = self.font_large.render("GAME OVER", True, RED)
        game_over_rect = game_over_text.get_rect(center=(width // 2, height // 2 - 50))
        screen.blit(game_over_text, game_over_rect)
        
        # Final score
        score_text = self.font_medium.render(f"Final Score: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(width // 2, height // 2))
        screen.blit(score_text, score_rect)
        
        # High score
        if self.score > self.high_score:
            new_high_text = self.font_medium.render("NEW HIGH SCORE!", True, YELLOW)
            new_high_rect = new_high_text.get_rect(center=(width // 2, height // 2 + 30))
            screen.blit(new_high_text, new_high_rect)
        else:
            high_text = self.font_small.render(f"High Score: {self.high_score}", True, GRAY)
            high_rect = high_text.get_rect(center=(width // 2, height // 2 + 30))
            screen.blit(high_text, high_rect)
        
        # Instructions
        restart_text = self.font_medium.render("Press R to Restart", True, YELLOW)
        restart_rect = restart_text.get_rect(center=(width // 2, height // 2 + 80))
        screen.blit(restart_text, restart_rect)
        
        menu_text = self.font_small.render("Press Q for Menu", True, WHITE)
        menu_rect = menu_text.get_rect(center=(width // 2, height // 2 + 110))
        screen.blit(menu_text, menu_rect)
    
    def draw(self):
        """Draw current game state"""
        if self.state == GameState.MENU:
            self.draw_menu()
        elif self.state == GameState.PLAYING:
            self.draw_game()
        elif self.state == GameState.PAUSED:
            self.draw_pause()
        elif self.state == GameState.GAME_OVER:
            self.draw_game_over()
        
        pygame.display.flip()

def main():
    """Main game loop"""
    game = Game()
    running = True
    
    while running:
        clock.tick(GAME_CONFIG['fps'])
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                result = game.handle_input(event)
                if result is False:
                    running = False
        
        # Update game
        game.update()
        
        # Draw everything
        game.draw()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
