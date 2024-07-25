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
            if not value:
                pygame.draw.rect(self.app.screen, 'black', rect)

            self.increments.rotate(1) if value else self.increments.rotate(-1)
            dx, dy = self.increments[0]
            self.x = (self.x + dx) % self.app.COLS
            self.y = (self.y + dy) % self.app.ROWS

class App:
    def __init__(self, WIDTH = 1600, HEIGHT = 900, CELL_SIZE = 8, NUM_ANTS = 400):
        pygame.init()
        self.screen = pygame.display.set_mode([WIDTH, HEIGHT])
        self.clock = pygame.time.Clock()

        self.CELL_SIZE = CELL_SIZE
        self.ROWS, self.COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE
        self.grid = [[0 for col in range(self.COLS)] for row in range(self.ROWS)]

        colors1 = [(50, 30, i) for i in range(256)]
        self.ants = [Ant(self, pos=[randrange(self.COLS), randrange(self.ROWS)], color=choice(colors1)) for _ in range(NUM_ANTS)]

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            pygame.display.set_caption(f'Langton\'s Ant Simulation - FPS: {int(self.clock.get_fps())}')
            self.screen.fill('white')  # Clear the screen with a white background

            [ant.run() for ant in self.ants]

            pygame.display.flip()
            self.clock.tick()

if __name__ == "__main__":
    app = App()
    app.run()