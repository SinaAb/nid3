import pygame
from NId3 import Hitbox, Player

class projectile(Hitbox.Hitbox):
    x: float
    y: float
    dy = 0
    color: tuple
    bound: tuple
    dimensions: tuple
    owner : Player
    curr_frame = 0
    frames : tuple
    gravitational = True

    def __init__(self, x : float, y : float, color : tuple, bound: tuple, dimensions: tuple, dx : float, owner, gravitational : bool):
        super(projectile, self).__init__(x, y, color, dimensions)
        self.gravitational = gravitational
        self.bound = bound
        self.dx = dx

        if self.gravitational:
            self.dy = -5

        self.owner = owner

        self.frames = (pygame.image.load("bullet1.bmp"), pygame.image.load("bullet2.bmp"))

    def draw(self, screen):
        if self.curr_frame <= 17:
            screen.blit(self.frames[0], (self.x, self.y))
            self.curr_frame += 1
        elif self.curr_frame <= 33:
            screen.blit(self.frames[1], (self.x, self.y))
            self.curr_frame += 1
        else:
            self.curr_frame = 0

    def move(self, hit_boxes : list):
        self.collide(hit_boxes)
        self.x += self.dx
        self.y += self.dy

        if self.gravitational:
            self._fall()

    def collide(self, hit_boxes : list):
        if not (self.bound[0] <= self.x + self.dx <= self.bound[2] - self.dimensions[0]):
            hit_boxes.remove(self)

        for hitbox in hit_boxes:
            if hitbox is not self and hitbox is not self.owner and isinstance(hitbox, Hitbox.Hitbox):

                #accounts for collision with vertical hitboxes in case this projectile has dy = 0, so that it can
                #detect future vertical collisions
                if self._overlap2D(self._future_xy(), hitbox._future_y()):
                    if type(hitbox) == Player.Player:
                        hitbox.dx = 0
                        hitbox.die()

                    try:
                        if type(hitbox) == projectile:
                            hit_boxes.remove(hitbox)

                        hit_boxes.remove(self)

                    except(ValueError):
                        pass

                    return

    def _fall(self):
        self.dy += 0.2


