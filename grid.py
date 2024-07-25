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

            SIZE = self.app.self.CELL_SIZE
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
        self.CELL_SIZE = CELL_SIZE
        self.WIDTH, self.HEIGTH = 1200, 900
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGTH))
        pygame.display.set_icon(pygame.image.load('ant_icon.png'))
        self.clock = pygame.time.Clock()
        self.grid = [[0 for col in range(16)] for row in range(16)]

        self.colors = set('greenyellow goldenrod2 fuchsia deeppink4 cornflowerblue darkred darkslategrey blueviolet mediumpurple3 indigo crimson seagreen1 salmon1 purple2 plum3 palevioletred violetred springgreen4 \
                          steelblue4 steelblue slateblue4 slateblue sienna2 cyan skyblue purple magenta red green blue yellow \
                          white'.split())
        
        self.is_placement_phase: bool = True
        self.placement_phase_grid = pygame.image.load('selection_phase_grid.png')
        self.placement_phase_grid_rect = self.placement_phase_grid.get_rect(center = (self.WIDTH // 2, self.HEIGTH // 2))

        self.title_font = pygame.font.Font('mexcellent/mexcellent 3d.otf', 64)
        self.title_text = self.title_font.render('Langton\'s Ant Simulation', True, 'white')
        self.title_rect = self.title_text.get_rect(center = (self.WIDTH // 2, 150))
        self.screen.blit(self.title_text, self.title_rect)

        self.counter_font = pygame.font.Font('mexcellent/mexcellent 3d.otf', 48)
        self.ant_counter_text = self.counter_font.render(f'Ants: {NUM_ANTS}', True, 'white')
        self.ant_counter_rect = self.ant_counter_text.get_rect(center = (225, 300))
        self.screen.blit(self.ant_counter_text, self.ant_counter_rect)

        self.button_font = pygame.font.Font('mexcellent/mexcellent 3d.otf', 56)
        self.start_button_text = self.button_font.render('Start', True, 'grey')
        self.start_button_rect = self.start_button_text.get_rect(center = (225, 550))
        self.screen.blit(self.start_button_text, self.start_button_rect)

        self.white_cell_counter_text = self.counter_font.render(f'White Cells:', True, 'white')
        self.white_cell_counter_rect = self.white_cell_counter_text.get_rect(center = (self.WIDTH - 225, 300))
        self.screen.blit(self.white_cell_counter_text, self.white_cell_counter_rect)

        self.grey_cell_counter_text = self.counter_font.render(f'Grey Cells:', True, 'white')
        self.grey_cell_counter_rect = self.grey_cell_counter_text.get_rect(center = (self.WIDTH - 225, 550))
        self.screen.blit(self.grey_cell_counter_text, self.grey_cell_counter_rect) 

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
                    if self.start_button_rect.collidepoint(event.pos):
                        self.is_placement_phase = False
                        self.start_button_text = self.button_font.render('Start', True, 'white')
                        self.screen.blit(self.start_button_text, self.start_button_rect)
            
            pygame.display.set_caption(f'Langton\'s Ant Simulation - FPS: {int(self.clock.get_fps())}')
        
            if self.is_placement_phase: 
                self.screen.blit(self.placement_phase_grid, self.placement_phase_grid_rect)
            else:
                self.white_cell_counter_text = self.counter_font.render(f'White Cells:', True, 'white')
                self.screen.blit(self.white_cell_counter_text, self.white_cell_counter_rect)

            #[ant.run() for ant in self.ants]

            pygame.display.flip()
            self.clock.tick()

    def get_white_cells(self):
        return sum([sum(row) for row in self.grid])

if __name__ == "__main__":
    app = App()
    app.run()