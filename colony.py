import pygame
from ant import Ant
from random import randrange

class Simulation:
    def __init__(self, WIDTH = 1920, HEIGHT = 1080, CELL_SIZE = 1, NUM_ANTS = 5000):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        self.CELL_SIZE = CELL_SIZE
        self.ROWS, self.COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE
        self.grid = [[0 for _ in range(self.COLS)] for _ in range(self.ROWS)]

        self.ants = [Ant(self, (randrange(self.COLS), randrange(self.ROWS)), Ant.get_color()) for _ in range(NUM_ANTS)]

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    exit()

            pygame.display.set_caption(f'Langton\'s Ant Simulation - FPS: {int(self.clock.get_fps())}')
            [ant.run() for ant in self.ants]

            pygame.display.flip()
            self.clock.tick()

if __name__ == "__main__":
    sim = Simulation()
    sim.run()