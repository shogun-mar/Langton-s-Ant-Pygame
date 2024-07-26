import pygame
from collections import deque

class Ant:
    def __init__(self, app, pos, color):
        self.app = app
        self.sprite = None
        self.x, self.y = pos
        self.rect = pygame.Rect(self.app.placement_grid_offset[0] + self.x * self.app.CELL_SIZE, self.app.placement_grid_offset[1] + self.y * self.app.CELL_SIZE, 
                                self.app.CELL_SIZE, self.app.CELL_SIZE)
        self.color = color
        self.increments = deque([(1, 0), (0, 1), (-1, 0), (0, -1)])

    def run(self):
        SIZE = self.app.CELL_SIZE
        base_x, base_y = self.x * SIZE + 1, self.y * SIZE + 1
        offsetted_rect = (base_x + self.app.placement_grid_offset[0], base_y + self.app.placement_grid_offset[1], max(SIZE - 1, 1) + 1, max(SIZE - 1, 1) + 1)
        value = self.app.grid[self.y][self.x]
        self.app.grid[self.y][self.x] = not value
        
        if value:
            pygame.draw.rect(self.app.screen, 'white', offsetted_rect)
        else:
            pygame.draw.rect(self.app.screen, self.color, offsetted_rect)

        self.increments.rotate(1) if value else self.increments.rotate(-1)
        dx, dy = self.increments[0]
        self.x = (self.x + dx) % self.app.COLS
        self.y = (self.y + dy) % self.app.ROWS

class App:
    def __init__(self):
        pygame.init()
        self.CELL_SIZE = 16
        self.ROWS = self.COLS = 16
        self.WIDTH, self.HEIGTH = 1200, 900
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGTH))
        pygame.display.set_icon(pygame.image.load('ant_window_icon.png'))
        self.clock = pygame.time.Clock()
        self.MAX_FPS = 10
        self.grid = [[0 for col in range(self.COLS)] for row in range(self.COLS)]

        self.ant_colors = list(set('greenyellow goldenrod2 fuchsia deeppink4 cornflowerblue darkred darkslategrey blueviolet mediumpurple3 indigo crimson seagreen1 salmon1 purple2 plum3 palevioletred violetred springgreen4 \
                          steelblue4 steelblue slateblue4 slateblue sienna2 cyan skyblue purple magenta red green blue yellow \
                          white'.split())) #Convert to set to remove duplicates then back to list to allow indexing
        
        self.ants = []
        self.ant_base_sprite = pygame.image.load('ant_sprite.png').convert_alpha()

        self.is_placement_phase: bool = True
        self.placement_phase_grid = pygame.image.load('selection_phase_grid.png').convert_alpha()
        self.placement_phase_grid_rect = self.placement_phase_grid.get_rect(center = (self.WIDTH // 2, self.HEIGTH // 2))
        self.placement_grid_offset = self.placement_phase_grid_rect.topleft

        self.simulation_phase_grid = pygame.image.load('simulation_phase_grid.png').convert_alpha()
        self.simulation_phase_grid_rect = self.simulation_phase_grid.get_rect(center = self.placement_phase_grid_rect.center)

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

        #placement phase color grid
        self.current_selected_color_name = None
        self.colored_cell_size = 40
        self.color_grid_cell_offset = 5
        #Calculations to align the color grid to the center of the screen and move it down 200 pixels
        self.len_ant_colors = len(self.ant_colors)
        self.expected_color_grid_width =  40 * self.ROWS + 5 * (self.ROWS - 1)
        self.expected_color_grid_heigth = 40 * (self.len_ant_colors // self.ROWS) + 5 * ((self.len_ant_colors // self.ROWS) - 1)
        screen_center = self.WIDTH // 2, self.HEIGTH // 2
        self.color_grid_origin = screen_center[0] - self.expected_color_grid_width // 2, (screen_center[1] - self.expected_color_grid_heigth // 2) + 250 

        self.placement_phase_color_grid_rects = []
        x, y = self.color_grid_origin
        for i in range(self.len_ant_colors):
            if i % self.ROWS == 0 and i != 0:
                x = self.color_grid_origin[0]
                y = self.color_grid_origin[1] + (self.colored_cell_size + self.color_grid_cell_offset)
            self.placement_phase_color_grid_rects.append(pygame.Rect(x, y, self.colored_cell_size, self.colored_cell_size))
            x += (self.colored_cell_size + self.color_grid_cell_offset)

        #Initial draw calls
        self.draw_colors_grid()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.is_placement_phase:
                        self.is_placement_phase = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_placement_phase: #Start simulation event
                    if self.start_button_rect.collidepoint(event.pos) and self.is_simulation_ready():
                        self.is_placement_phase = False #Toggle to simulation phase
                        #Update start button text color
                        self.start_button_text = self.button_font.render('Start', True, 'white')
                        self.screen.blit(self.start_button_text, self.start_button_rect)

                        #Hide placement grid
                        coverup_surf = pygame.Surface(self.placement_phase_grid.get_size())
                        self.screen.blit(coverup_surf, self.placement_phase_grid_rect)

                        #Hide color grid
                        coverup_surf = pygame.Surface((self.expected_color_grid_width, self.expected_color_grid_heigth))
                        self.screen.blit(coverup_surf, (self.color_grid_origin[0], self.color_grid_origin[1]))

                        #Draw simulation grid
                        self.screen.blit(self.simulation_phase_grid, self.simulation_phase_grid_rect)

                    elif self.placement_phase_grid_rect.collidepoint(event.pos) and self.current_selected_color_name != None:
                        self.update_placement_grid(event.pos)

                    current_color = self.get_currently_selected_color(event.pos)
                    if current_color != None: self.current_selected_color_name = current_color
                        
            pygame.display.set_caption(f'Langton\'s Ant Simulation - FPS: {int(self.clock.get_fps())}')

            if self.is_placement_phase: 
                self.screen.blit(self.placement_phase_grid, self.placement_phase_grid_rect)

                coverup_surf = pygame.Surface(self.ant_counter_text.get_size())
                self.screen.blit(coverup_surf, self.ant_counter_rect)
                num_ants = len(self.ants)
                self.ant_counter_text = self.counter_font.render(f'Ants: {num_ants}', True, 'white')
                self.ant_counter_rect.center = (225 - 15 * len(str(num_ants)), 300)
                self.screen.blit(self.ant_counter_text, self.ant_counter_rect)

                self.draw_ants_placement_grid()

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

                [ant.run() for ant in self.ants]

                #Draw simulation grid again to cover up ant drawn rects (not necessary added for aesthetic reasons)
                self.screen.blit(self.simulation_phase_grid, self.simulation_phase_grid_rect)

            pygame.display.flip()
            self.clock.tick(self.MAX_FPS)

    def get_white_cells(self):
        return sum(cell for row in self.grid for cell in row)
    
    def is_simulation_ready(self):
        return len(self.ants) > 0
    
    def update_placement_grid(self, pos):
        relative_mouse_pos = pos[0] - self.placement_grid_offset[0], pos[1] - self.placement_grid_offset[1]
        x, y = relative_mouse_pos
        column, row = x // self.CELL_SIZE, y // self.CELL_SIZE
        ant = Ant(self, (column, row), self.current_selected_color_name)
        self.ants.append(ant)
        self.grid[column][row] = 1

        color_int = pygame.Color(ant.color)  # Convert named color to integer color
        sprite_pixel_array = pygame.PixelArray(self.ant_base_sprite)
        width, height = sprite_pixel_array.shape

        for i in range(width):
            for j in range(height):
                pixel_color = self.ant_base_sprite.unmap_rgb(sprite_pixel_array[i, j])  # Get the color of the pixel
                original_color = pygame.Color(pixel_color)
                if original_color.a != 0:  # Check if the pixel is not fully transparent
                    new_color = pygame.Color(color_int.r, color_int.g, color_int.b, original_color.a)
                    sprite_pixel_array[i, j] = self.ant_base_sprite.map_rgb(new_color)
                
        ant.sprite = sprite_pixel_array.make_surface()  # Creates a new surface with the new pixel array.
        del sprite_pixel_array  # Delete the pixel array to unlock the surface

    def draw_ants_placement_grid(self):
        for ant in self.ants:
            self.screen.blit(ant.sprite, ant.rect)

    def get_currently_selected_color(self, mouse_pos):
        for i in range(self.len_ant_colors):
            if self.placement_phase_color_grid_rects[i].collidepoint(mouse_pos):
                self.current_selected_color_name = self.ant_colors[i]
                return self.ant_colors[i]
        return None

    def draw_colors_grid(self):
        for i in range(self.len_ant_colors):
            pygame.draw.rect(self.screen, self.ant_colors[i], self.placement_phase_color_grid_rects[i])
    
if __name__ == "__main__":
    app = App()
    app.run()