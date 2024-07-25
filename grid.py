import pygame
from collections import deque
from random import choice, randrange

class Ant:
    def __init__(self, app, pos, color):
        self.app = app
        self.color = color
        self.x, self.y = pos
        self.increments = deque([(1, 0), (0, 1), (-1, 0), (0, -1)])

    def run(self):
        if 0 <= self.x < self.app.COLS and 0 <= self.y < self.app.ROWS:
            value = self.app.grid[self.y][self.x]
            self.app.grid[self.y][self.x] = not value

            SIZE = self.app.CELL_SIZE
            rect = self.x * SIZE, self.y * SIZE, max(SIZE - 1, 1), max(SIZE - 1, 1)
            
            pygame.draw.rect(self.app.screen, self.color, rect)

            self.increments.rotate(1) if value else self.increments.rotate(-1)
            dx, dy = self.increments[0]
            self.x = (self.x + dx) % self.app.COLS
            self.y = (self.y + dy) % self.app.ROWS

    @staticmethod
    def get_color():
        channel = lambda: randrange(30, 220) #Lambda function that returns a random number between 30 and 220
        return channel(), channel(), channel()

class App:
    def __init__(self, CELL_SIZE = 16, NUM_ANTS = 400):
        pygame.init()
        WIDTH, HEIGHT = CELL_SIZE * 100, CELL_SIZE * 55 + (CELL_SIZE + 40) # Add 40 pixels to the height to make space for the color bar
        self.screen = pygame.display.set_mode([WIDTH, HEIGHT])
        self.clock = pygame.time.Clock()

        self.is_placement_phase = True

        self.CELL_SIZE = CELL_SIZE
        self.ROWS, self.COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE
        self.grid = [[0 for col in range(self.COLS)] for row in range(self.ROWS)]

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.is_placement_phase:
                        self.is_placement_phase = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_placement_phase:
                    x, y = event.pos
                    col, row = x // self.CELL_SIZE, y // self.CELL_SIZE
                    self.grid[row][col] = not self.grid[row][col]
            
            pygame.display.set_caption(f'Langton\'s Ant Simulation - FPS: {int(self.clock.get_fps())}')

            if self.is_placement_phase: 
                self.draw_selection_grid()

            #[ant.run() for ant in self.ants]

            pygame.display.flip()
            self.clock.tick()

    def draw_selection_grid(self):
        for row in range(self.ROWS):
            for col in range(self.COLS):
                pygame.draw.line(self.screen, 'white', (col * self.CELL_SIZE, 0), (col * self.CELL_SIZE, self.ROWS * self.CELL_SIZE))
                pygame.draw.line(self.screen, 'white', (0, row * self.CELL_SIZE), (self.COLS * self.CELL_SIZE, row * self.CELL_SIZE))
        
            # Draw the rightmost vertical line
            pygame.draw.line(self.screen, 'white', (self.COLS * self.CELL_SIZE - 1, 0), (self.COLS * self.CELL_SIZE - 1, self.ROWS * self.CELL_SIZE))
            # Draw the bottommost horizontal line
            pygame.draw.line(self.screen, 'white', (0, self.ROWS * self.CELL_SIZE - 1), (self.COLS * self.CELL_SIZE, self.ROWS * self.CELL_SIZE - 1))

if __name__ == "__main__":
    app = App()
    app.run()