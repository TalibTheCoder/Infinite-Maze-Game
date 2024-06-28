import pygame
import sys
import random
import asyncio  # 1. Import asyncio

# Constants
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20  # Size of each grid cell in pixels
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

# Classes
class Player:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = 0
        self.y = 0

    def draw(self, screen):
        pygame.draw.rect(screen, RED, (self.x * GRID_SIZE, self.y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    def move(self, dx, dy, maze):
        new_x = self.x + dx
        new_y = self.y + dy

        # Check if the new position is within bounds and not a wall
        if 0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT and maze[new_y][new_x] != 1:
            self.x = new_x
            self.y = new_y
            if maze[self.y][self.x] == 2:
                self.reset()
                return True  # Reached the green square
        return False

class Maze:
    def __init__(self):
        self.grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]

    def generate(self, difficulty):
        # Fill the maze with white (empty space)
        self.grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]

        # Create random obstacles (black squares)
        for _ in range(difficulty * 10):  # Higher initial difficulty
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            self.grid[y][x] = 1

        # Ensure start position and end position
        self.grid[0][0] = 0  # Start position
        self.grid[GRID_HEIGHT - 1][GRID_WIDTH - 1] = 2  # End position (green square)

    def draw(self, screen):
        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                if self.grid[y][x] == 1:
                    pygame.draw.rect(screen, BLACK, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
                elif self.grid[y][x] == 2:
                    pygame.draw.rect(screen, GREEN, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))


async def main():  # 3. Define main as an asynchronous function
    # Initialize Pygame
    pygame.init()

    # Initialize game objects
    player = Player()
    maze = Maze()
    difficulty = 5  # Initial difficulty level (5 times harder)
    maze.generate(difficulty)  # Generate initial maze

    # Set up the display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Maze Game")

    # Fonts
    font = pygame.font.SysFont(None, 36)

    # Main game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    if player.move(0, -1, maze.grid):  # Move up
                        difficulty += 1
                        maze.generate(difficulty)
                elif event.key == pygame.K_s:
                    if player.move(0, 1, maze.grid):  # Move down
                        difficulty += 1
                        maze.generate(difficulty)
                elif event.key == pygame.K_a:
                    if player.move(-1, 0, maze.grid):  # Move left
                        difficulty += 1
                        maze.generate(difficulty)
                elif event.key == pygame.K_d:
                    if player.move(1, 0, maze.grid):  # Move right
                        difficulty += 1
                        maze.generate(difficulty)

        # Clear screen
        screen.fill(WHITE)

        # Draw maze and player
        maze.draw(screen)
        player.draw(screen)

        # Check if it's impossible to reach the green square
        if difficulty > 20:  # Adjust this condition as needed for difficulty scaling
            text = font.render("Congratulations! You win!", True, RED)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(text, text_rect)
            pygame.display.flip()
            await asyncio.sleep(2)  # Use asyncio.sleep instead of pygame.time.wait
            difficulty = 5  # Reset initial difficulty
            maze.generate(difficulty)
            player.reset()

        # Update display
        pygame.display.flip()

        # Cap the frame rate
        await asyncio.sleep(0)  # Use asyncio.sleep(0) instead of pygame.time.Clock().tick(30)

    pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())  # Run the main function using asyncio.run()
