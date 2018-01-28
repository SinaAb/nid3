import pygame
import copy

class Hitbox:
    x : float
    y : float
    dx : float
    dy : float
    color : tuple
    dimensions : tuple

    def __init__(self, x : float, y : float, color : tuple, dimensions: tuple):
        self.x = x
        self.y = y
        self.color = color
        self.dimensions = dimensions
        self.dx , self.dy = 0 , 0

    def move(self, hit_boxes : list):
        pass

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, [self.x, self.y, self.dimensions[0], self.dimensions[1]])

    def collide(self, hit_boxes : list):
        pass

    def _overlap1D(self, l1: tuple, l2: tuple):
        # tuple in form (xmin , xmax)
        return l1[1] >= l2[0] and l2[1] >= l1[0]

    def _overlap2D(self, b1: tuple, b2: tuple):
        # tuple in form (xmin, xmax, ymin, ymax)
        return self._overlap1D((b1[0], b1[1]), (b2[0], b2[1])) and self._overlap1D((b1[2], b1[3]), (b2[2], b2[3]))

    def _getSelfBound(self):
        return (self.x , self.x + self.dimensions[0], self.y, self.y + self.dimensions[1])

    def _future_y(self):
        return (self.x, self.x + self.dimensions[0], self.y + self.dy, self.y + self.dimensions[1] + self.dy)

    def _future_x(self):
        return (self.x + self.dx, self.x + self.dimensions[0] + self.dx, self.y, self.y + self.dimensions[1])

    def _future_xy(self):
        return (self.x + self.dx, self.x + self.dimensions[0] + self.dx, self.y + self.dy, self.y + self.dimensions[1] + self.dy)
