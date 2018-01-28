import pygame
from NId3 import Hitbox, Player

class platform(Hitbox.Hitbox):
    movement_bound : tuple

    def __init__(self, x : float, y : float, color : tuple, dimensions : tuple, dx : float, dy : float, max_displace : tuple):
        super(platform, self).__init__(x, y, color, dimensions)
        self.dx = dx
        self.dy = dy
        self.movement_bound = (min(self.x, self.x + max_displace[0]),
                               max(self.x, self.x + max_displace[0]),
                               min(self.y, self.y + max_displace[1]),
                               max(self.y, self.y + max_displace[1]))

    def move(self, hit_boxes : list):
        if self.x + self.dx < self.movement_bound[0] or self.x + self.dx > self.movement_bound[1]:
            self.dx *= -1
        if self.y + self.dy < self.movement_bound[2] or self.y + self.dy > self.movement_bound[3]:
            self.dy *= -1

        self.collide(hit_boxes)

        self.x += self.dx
        self.y += self.dy

    def collide(self, hit_boxes : list):
        for hitbox in hit_boxes:

            #move the player with the platform if the player is on the platform
            if hitbox is not self and isinstance(hitbox, Player.Player):
                if self.x <= hitbox.x <= self.x + self.dimensions[0] and self.y - 1 <= hitbox.y + hitbox.dimensions[1] <= self.y:
                    hitbox.x += self.dx
                    hitbox.y += self.dy


