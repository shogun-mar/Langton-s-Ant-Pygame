import pygame
from collections import deque
from random import randrange

class Ant:
    def __init__(self, simulation, pos, color):
        self.simulation = simulation
        self.x, self.y = pos
        self.color = color
        self.increments = deque([(0, -1), (1, 0), (0, 1), (-1, 0)])

    def run(self):
        value = self.simulation.grid[self.y][self.x]
        self.simulation.grid[self.y][self.x] = not value

        SIZE = self.simulation.CELL_SIZE
        rect = self.x * SIZE, self.y * SIZE, max(SIZE - 1, 1), max(SIZE - 1, 1)  # Ensure the rect size is at least 1
        if value:
            pygame.draw.rect(self.simulation.screen, 'white', rect)
        else:
            pygame.draw.rect(self.simulation.screen, self.color, rect)
        
        self.increments.rotate(1 if value else -1)
        dx, dy = self.increments[0]
        self.x = (self.x + dx) % self.simulation.COLS #Take the remainder of the division so that the ant does not go out of bounds
        self.y = (self.y + dy) % self.simulation.ROWS

    @staticmethod
    def get_color():
        channel = lambda: randrange(30, 220) #Lambda function that returns a random number between 30 and 220
        return channel(), channel(), channel()
