import pygame
import Data.Scripts.entities.entities as entities

class SquareEffects(entities.Particle):
    def __init__(self, loc, size, start_width, decay=0.1, colour=None):
        self.size = size
        self.loc = [loc[0] - (self.size / 2), loc[1] - (self.size / 2)]
        self.decay = decay
        self.width = start_width
        self.rect = pygame.Rect(self.loc, (self.size, self.size))
        self.colour = colour

    def update(self):
        self.width -= self.decay

class PixelParticle(entities.Particle):
    def __init__(self, loc, timer, decay=0.05, speed=1, gravity=0, colour=None):
        super().__init__(loc, [3, 3], decay, speed, gravity, colour)