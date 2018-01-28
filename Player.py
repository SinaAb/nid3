import pygame
from NId3 import Hitbox
from NId3 import Projectile
from NId3 import Platform
from random import randint


class Player(Hitbox.Hitbox):
    x : float
    y : float
    dx = 0
    dy = 0
    color : tuple #last element of color being even implies player 1, otherwise player 2
    bound : tuple
    dimensions : tuple
    deaths = 0
    jumps = 2

    def __init__(self, x : float, y : float, color : tuple, dimensions : tuple, bound : tuple):
        super(Player, self).__init__(x, y, color, dimensions)
        self.bound = bound


    def move(self, hit_boxes):
        if self._grounded():
            self.jumps = 2

        #physical movements
        self._slide()
        self._fall()

        self.collide(hit_boxes)

        self.x += self.dx
        self.y += self.dy


    def collide(self, hit_boxes : list):
        #Screen as bound
        if not (self.bound[0] <= self.x + self.dx <= self.bound[2] - self.dimensions[0]):
            self.dx = 0
        if not (self.bound[1] <= self.y + self.dy <= self.bound[3] - self.dimensions[1]):
            self.dy = 0


        for hitbox in hit_boxes:
            if hitbox is not self and isinstance(hitbox, Hitbox.Hitbox):
                if type(hitbox) == Projectile.projectile and hitbox.owner == self:
                    continue

                if self._overlap2D(self._future_x(), hitbox._getSelfBound()):
                    self.dx = 0

                    #hit from left
                    if self.x <= hitbox.x:
                        self.x = hitbox.x - self.dimensions[0] - 1
                    #hit from right
                    elif self.x >= hitbox.x:
                        self.x = hitbox.x + hitbox.dimensions[0] + 1

                if self._overlap2D(self._future_y(), hitbox._getSelfBound()):
                    if self.y >= hitbox.y:
                        self.dy = 0.01
                    elif self.y <= hitbox.y:
                        self.dy = 0
                        self.y = hitbox.y - self.dimensions[1] - 1 #not sure how this will work in future


    def _projectile_collision(self, hitbox : Hitbox.Hitbox, hit_boxes : list):
        self.die()
        hit_boxes.remove(hitbox)

    def die(self):
        if self.color[2] % 2 == 0:
            self.x, self.y = 0, randint(0, self.bound[3] - self.dimensions[1])
        else:
            self.x, self.y = 1200 - self.dimensions[0], randint(0, self.bound[3] - self.dimensions[1])

        self.deaths += 1

    def move_in_x(self, cause):
        if cause == 0:
            self.dx = 6
        if cause == 1:
            self.dx = -6

    def move_in_y(self, cause):
        if cause == 0:
            if self.jumps == 2 or self.jumps == 1:
                self.jumps -= 1
                self.dy = -6
            else:
                pass

    def _slide(self):
        if not (self.dx == 0):
            self.dx -= (3/4) * abs(self.dx)/self.dx

    def _fall(self):
        self.dy += 0.2

    def _grounded(self):
        return self.dy == 0




    #SETTERS GETTERS AND SUCH
    def setBound(self, lx, ly, ux, uy):
        self.bound = (lx, ly, ux, uy)

    def setDimensions(self, dim : tuple):
        self.dimensions = dim

    def getPos(self):
        return (self.x, self.y)

    def setPos(self, x, y):
        self.x = x
        self.y = y


