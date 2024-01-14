# enitites.py

from math import sin, cos, atan2, hypot
import random 
from collections import deque

class Bot(object):
    def __init__(self, position, target):
        self.position = position
        self.target = target
        self.speed = random.random() + 0.5
        self.padding = random.random() * 8 + 16
        self.history = deque(maxlen=64)
    def get_position(self, offset):
        px, py = self.position
        tx, ty = self.target
        angle = atan2(ty - py, tx - px)
        return (px + cos(angle) * offset, py + sin(angle) * offset)
    def update(self, bots, obstacles):
        px, py = self.position
        tx, ty = self.target
        angle = atan2(ty - py, tx - px)
        dx = cos(angle)
        dy = sin(angle)
        for bot in bots:
            if bot == self:
                continue
            x, y = bot.position
            d = hypot(px - x, py - y) ** 2
            p = bot.padding ** 2
            angle = atan2(py - y, px - x)
            dx += cos(angle) / d * p
            dy += sin(angle) / d * p
        for obstacle in obstacles:
            x, y = obstacle.position
            d = hypot(px - x, py - y) ** 2
            p = obstacle.padding ** 1.5 # 2
            if d < p:
                angle = atan2(py - y, px - x)
                dx += cos(angle) / d * p
                dy += sin(angle) / d * p
        
        angle = atan2(dy, dx)
        magnitude = hypot(dx, dy)
        return angle, magnitude
    def set_position(self, position):
        self.position = position
        if not self.history:
            self.history.append(self.position)
            return
        x, y = self.position
        px, py = self.history[-1]
        d = hypot(px - x, py - y)
        if d >= 10:
            self.history.append(self.position)

class Obstacle(object):
    def __init__(self, position):
        self.position = position
        self.padding = random.random() * 8 + 16