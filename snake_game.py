import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH, GRID_HEIGHT = SCREEN_WIDTH // GRID_SIZE, SCREEN_HEIGHT // GRID_SIZE
SNAKE_SPEED = 10
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
FONT = pygame.font.Font(None, 74)
SMALL_FONT = pygame.font.Font(None, 36)

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Snake Game')

# Snake class
class Snake:
    def __init__(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)])
        self.grow = False

    def move(self):
        head = self.positions[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])

        if new_head[0] < 0 or new_head[0] >= GRID_WIDTH or new_head[1] < 0 or new_head[1] >= GRID_HEIGHT:
            return False

        if new_head in self.positions[1:]:
            return False

        self.positions.insert(0, new_head)

        if not self.grow:
            self.positions.pop()
        else:
            self.grow = False
        return True

    def change_direction(self, direction):
        if direction == (0, -self.direction[1]) or direction == (-self.direction[0], 0):
            return
        self.direction = direction

    def grow_snake(self):
        self.grow = True

    def draw(self, surface):
        for pos in self.positions:
            x, y = pos[0] * GRID_SIZE, pos[1] * GRID_SIZE
            pygame.draw.rect(surface, GREEN, (x, y, GRID_SIZE, GRID_SIZE))

# Food class
class Food:
    def __init__(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

    def draw(self, surface):
        x, y = self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE
        pygame.draw.rect(surface, RED, (x, y, GRID_SIZE, GRID_SIZE))

def show_start_screen():
    screen.fill(BLACK)
    
    # Draw main title
    title = FONT.render("SNAKE GAME", True, GREEN)
    title_pos = (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT // 3)
    screen.blit(title, title_pos)
    
    # Draw controls text in top right corner
    controls = SMALL_FONT.render("Use arrow keys to move", True, WHITE)
    controls_pos = (SCREEN_WIDTH - controls.get_width() - 20, 20)  # 20px padding from edges
    screen.blit(controls, controls_pos)
    
    # Draw "Press any key to start" message
    start_message = SMALL_FONT.render("Press any key to start", True, WHITE)
    start_pos = (SCREEN_WIDTH // 2 - start_message.get_width() // 2, SCREEN_HEIGHT * 2 // 3)
    screen.blit(start_message, start_pos)
    
    # Draw quit message
    quit_message = SMALL_FONT.render("Press Q to quit", True, WHITE)
    quit_pos = (SCREEN_WIDTH // 2 - quit_message.get_width() // 2, SCREEN_HEIGHT * 2 // 3 + 40)
    screen.blit(quit_message, quit_pos)
    
    pygame.display.flip()
    
    # Wait for any key press
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                waiting = False

def game_loop():
    clock = pygame.time.Clock()
    snake = Snake()
    food = Food()
    score = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction((0, -1))
                elif event.key == pygame.K_DOWN:
                    snake.change_direction((0, 1))
                elif event.key == pygame.K_LEFT:
                    snake.change_direction((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction((1, 0))
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        if not snake.move():
            break

        if snake.positions[0] == food.position:
            snake.grow_snake()
            food.randomize_position()
            score += 1

        screen.fill(BLACK)
        snake.draw(screen)
        food.draw(screen)
        pygame.display.flip()
        clock.tick(SNAKE_SPEED)
    
    return score

def show_game_over(score):
    screen.fill(BLACK)
    lose_message = FONT.render("YOU LOSE", True, WHITE)
    score_message = FONT.render(f"Final Score: {score}", True, WHITE)
    replay_message = SMALL_FONT.render("Press R to play again", True, WHITE)
    quit_message = SMALL_FONT.render("Press Q to quit", True, WHITE)
    
    lose_message_pos = (SCREEN_WIDTH // 4.5, SCREEN_HEIGHT // 4)
    score_message_pos = (SCREEN_WIDTH // 4.5, SCREEN_HEIGHT // 2)
    replay_message_pos = (SCREEN_WIDTH // 3, SCREEN_HEIGHT * 3 // 4)
    quit_message_pos = (SCREEN_WIDTH // 3, SCREEN_HEIGHT * 3 // 4 + 40)
    
    screen.blit(lose_message, lose_message_pos)
    screen.blit(score_message, score_message_pos)
    screen.blit(replay_message, replay_message_pos)
    screen.blit(quit_message, quit_message_pos)
    pygame.display.flip()

def main():
    while True:
        show_start_screen()
        score = game_loop()
        show_game_over(score)
        
        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        waiting_for_input = False
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

if __name__ == "__main__":
    main()