import pygame
import random

class Entity:
    def __init__(self, rect):
       self.rect = pygame.Rect(rect)
    
    def move(self, movement, colliders):
        pass

class Player(Entity):
    pass

class Particle:
    def __init__(self, loc, size_range=[5, 10], decay=0.1, speed=1, gravity=0, colour=None):
        self.velocity = [(random.randint(-10,10) / 5) * speed, (random.randint(-20, 30) / 3) * speed]
        self.size = random.randint(size_range[0], size_range[1])
        loc = [loc[0] - (self.size / 2), loc[1] - (self.size / 2)]
        self.decay = decay
        self.gravity = gravity
        self.rect = pygame.Rect(loc, (self.size, self.size))
        self.colour = colour
    
    def update(self):
        self.velocity[1] += self.gravity
        self.velocity[1] = min(self.velocity[1], 3)
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        self.size -= self.decay
        self.rect.width = self.size
        self.rect.height = self.size