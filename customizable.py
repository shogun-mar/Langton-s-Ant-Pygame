import pygame
from collections import deque
from random import choice, randrange

class Ant:
    def __init__(self, app, pos, color, shape):
        self.app = app
        self.color = color
        self.x, self.y = pos
        self.shape = shape
        self.increments = deque([(1, 0), (0, 1), (-1, 0), (0, -1)])

    def run(self):
        if 0 <= self.x < self.app.COLS and 0 <= self.y < self.app.ROWS:
            value = self.app.grid[self.y][self.x]
            self.app.grid[self.y][self.x] = not value

            SIZE = self.app.CELL_SIZE
            rect = self.x * SIZE, self.y * SIZE, max(SIZE - 1, 1), max(SIZE - 1, 1)
            
            if not value:
                if self.shape == 'square': pygame.draw.rect(self.app.screen, self.color, rect)
                else: pygame.draw.circle(self.app.screen, self.color, (self.x * SIZE + SIZE // 2, self.y * SIZE + SIZE // 2), SIZE // 2)
            else:
                if self.shape == 'square': pygame.draw.rect(self.app.screen, 'white', rect)
                else: pygame.draw.circle(self.app.screen, 'white', (self.x * SIZE + SIZE // 2, self.y * SIZE + SIZE // 2), SIZE // 2)

            self.increments.rotate(1) if value else self.increments.rotate(-1)
            dx, dy = self.increments[0]
            self.x = (self.x + dx) % self.app.COLS
            self.y = (self.y + dy) % self.app.ROWS

    @staticmethod
    def get_color():
        channel = lambda: randrange(30, 220) #Lambda function that returns a random number between 30 and 220
        return channel(), channel(), channel()