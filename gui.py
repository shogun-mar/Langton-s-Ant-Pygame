import pygame
from collections import deque
from random import randrange

class Ant:
    def __init__(self, app, pos, color):
        self.app = app
        self.sprite = None
        self.color = color
        self.x, self.y = pos
        self.increments = deque([(1, 0), (0, 1), (-1, 0), (0, -1)])

    def run(self):
        if 0 <= self.x < self.app.COLS and 0 <= self.y < self.app.ROWS:
            value = self.app.grid[self.y][self.x]
            self.app.grid[self.y][self.x] = not value

            SIZE = self.app.self.CELL_SIZE
            rect = self.x * SIZE, self.y * SIZE, max(SIZE - 1, 1), max(SIZE - 1, 1)
            
            if value:
                pygame.draw.rect(self.app.screen, 'white', rect)
            else:
                pygame.draw.rect(self.app.screen, self.color, rect)

            self.increments.rotate(1) if value else self.increments.rotate(-1)
            dx, dy = self.increments[0]
            self.x = (self.x + dx) % self.app.COLS
            self.y = (self.y + dy) % self.app.ROWS

class App:
    def __init__(self, CELL_SIZE = 16):
        pygame.init()
        self.CELL_SIZE = CELL_SIZE
        self.ROWS = self.COLS = 16
        self.WIDTH, self.HEIGTH = 1200, 900
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGTH))
        pygame.display.set_icon(pygame.image.load('ant_window_icon.png'))
        self.clock = pygame.time.Clock()
        self.grid = [[0 for col in range(self.COLS)] for row in range(self.COLS)]

        self.colors = set('greenyellow goldenrod2 fuchsia deeppink4 cornflowerblue darkred darkslategrey blueviolet mediumpurple3 indigo crimson seagreen1 salmon1 purple2 plum3 palevioletred violetred springgreen4 \
                          steelblue4 steelblue slateblue4 slateblue sienna2 cyan skyblue purple magenta red green blue yellow \
                          white'.split())
        
        self.ants = []
        self.ant_base_sprite = pygame.image.load('ant_sprite.png').convert_alpha()

        self.is_placement_phase: bool = True
        self.placement_phase_grid = pygame.image.load('selection_phase_grid.png')
        self.placement_phase_grid_rect = self.placement_phase_grid.get_rect(center = (self.WIDTH // 2, self.HEIGTH // 2))
        self.placement_grid_offset = self.placement_phase_grid_rect.topleft

        self.title_font = pygame.font.Font('mexcellent/mexcellent 3d.otf', 64)
        self.title_text = self.title_font.render('Langton\'s Ant Simulation', True, 'white')
        self.title_rect = self.title_text.get_rect(center = (self.WIDTH // 2, 150))
        self.screen.blit(self.title_text, self.title_rect)

        self.counter_font = pygame.font.Font('mexcellent/mexcellent 3d.otf', 48)
        self.ant_counter_text = self.counter_font.render('Ants: 0', True, 'white')
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
                    if self.start_button_rect.collidepoint(event.pos) and self.is_simulation_ready():
                        self.is_placement_phase = False
                        self.start_button_text = self.button_font.render('Start', True, 'white')
                        self.screen.blit(self.start_button_text, self.start_button_rect)

                    elif self.placement_phase_grid_rect.collidepoint(event.pos):
                        self.update_placement_grid(event.pos)
            
            pygame.display.set_caption(f'Langton\'s Ant Simulation - FPS: {int(self.clock.get_fps())}')

            if self.is_placement_phase: 
                self.screen.blit(self.placement_phase_grid, self.placement_phase_grid_rect)

                coverup_surf = pygame.Surface(self.ant_counter_text.get_size())
                self.screen.blit(coverup_surf, self.ant_counter_rect)
                num_ants = len(self.ants)
                self.ant_counter_text = self.counter_font.render(f'Ants: {num_ants}', True, 'white')
                self.ant_counter_rect.center = (225 - 15 * len(str(num_ants)), 300)
                self.screen.blit(self.ant_counter_text, self.ant_counter_rect)

            else:
                coverup_surf = pygame.Surface(self.white_cell_counter_text.get_size())
                self.screen.blit(coverup_surf, self.white_cell_counter_rect)
                white_cells_num = self.get_white_cells()
                self.white_cell_counter_text = self.counter_font.render(f'White Cells: {white_cells_num}', True, 'white')
                self.white_cell_counter_rect.center = (self.WIDTH - 225 - 15 * len(str(white_cells_num)), 300)
                self.screen.blit(self.white_cell_counter_text, self.white_cell_counter_rect)

                coverup_surf = pygame.Surface(self.grey_cell_counter_text.get_size())
                self.screen.blit(coverup_surf, self.grey_cell_counter_rect)
                grey_cells_num = self.ROWS * self.COLS - white_cells_num
                self.grey_cell_counter_text = self.counter_font.render(f'Grey Cells: {grey_cells_num}', True, 'white')
                self.grey_cell_counter_rect.center = (self.WIDTH - 225 - 15 * len(str(grey_cells_num)), 550)
                self.screen.blit(self.grey_cell_counter_text, self.grey_cell_counter_rect)

                #[ant.run() for ant in self.ants]

            pygame.display.flip()
            self.clock.tick(60)

    def get_white_cells(self):
        return sum(cell for row in self.grid for cell in row)
    
    def is_simulation_ready(self):
        return len(self.ants) > 0
    
    def update_placement_grid(self, pos):
        relative_mouse_pos = pos[0] - self.placement_grid_offset[0], pos[1] - self.placement_grid_offset[1]
        x, y = relative_mouse_pos
        column, row = x // self.CELL_SIZE, y // self.CELL_SIZE
        ant = Ant(self, (column, row), 'white')
        self.ants.append(ant)
        self.grid[column][row] = 1

        grid_origin_x, grid_origin_y = self.placement_grid_offset
        color_int = pygame.Color(ant.color)  # Convert named color to integer color
        sprite_pixel_array = pygame.PixelArray(self.ant_base_sprite)
        for i in range(sprite_pixel_array.shape[0]):
            for j in range(sprite_pixel_array.shape[1]):
                pixel_color = self.ant_base_sprite.unmap_rgb(sprite_pixel_array[i, j])  # Get the color of the pixel
                if pygame.Color(pixel_color).a != 0:  # Check if the pixel is not fully transparent
                    sprite_pixel_array[i, j] = (color_int.r, color_int.g, color_int.b)
        
        ant.sprite = sprite_pixel_array.make_surface()  # Creates a new surface with the new pixel array.
        del sprite_pixel_array  # Delete the pixel array to unlock the surface
        self.screen.blit(ant.sprite, (grid_origin_x + column * self.CELL_SIZE, grid_origin_y + row * self.CELL_SIZE))
    
if __name__ == "__main__":
    app = App()
    app.run()