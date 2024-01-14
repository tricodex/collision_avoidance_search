# simulation.py

import random
from math import cos, sin, pi, hypot, sqrt
from settings import *
from entities import Bot, Obstacle

class Simulation(object):
    def __init__(self, width, height, count, obstacle_count):
        self.width = width
        self.height = height
        self.bots = self.create_bots(count)
        self.obstacles = self.create_obstacles(obstacle_count)
    # Square Edge 4 Quadrant
    def select_point_bots(self):
        half_side = SIZE / 2.0
        edge = random.choice(['top', 'bottom', 'left', 'right']) # Choose side
        if edge in ['top', 'bottom']:
            x = random.uniform(-half_side, half_side) + half_side
            y = half_side if edge == 'top' else -half_side + half_side
        else:  # left or right
            y = random.uniform(-half_side, half_side) + half_side
            x = half_side if edge == 'right' else -half_side + half_side
        return (x, y)
    def create_bots(self, count):
        result = []
        # searchbot
        for i in range(3):
            position = self.select_point_bots()
            target = self.select_point_bots()
            search_bot = Bot(position, target)  
            result.append(search_bot)
        # obstaclebot
        for i in range(3, count):
            position = self.select_point_bots()
            target = self.select_point_bots()
            other_bot = Bot(position, target)
            result.append(other_bot)
        return result

    def create_obstacles(self, obstacle_count):
        return [Obstacle(self.select_point()) for _ in range(obstacle_count)]
    # Square Random Distribution
    def select_point(self):
        half_side = SIZE / 2.0  # Half the side length of the square
        cx = SIZE / 2.0
        cy = SIZE / 2.0
        x = cx + random.uniform(-half_side, half_side)
        y = cy + random.uniform(-half_side, half_side)
        return (x, y)
    def update(self, dt):
        data = [bot.update(self.bots, self.obstacles) for bot in self.bots]
        # Bot Behavior
        for bot, (angle, magnitude) in zip(self.bots, data):
            speed = min(1, 0.2 + magnitude * 0.8)
            dx = cos(angle) * dt * SPEED * bot.speed * speed
            dy = sin(angle) * dt * SPEED * bot.speed * speed
            px, py = bot.position
            tx, ty = bot.target
            bot.set_position((px + dx, py + dy))
            # SearchBot Behavior
            if hypot(px - tx, py - ty) < 10:
                bot.target = self.select_point()
        # FollowerBot Behavior
        for bot in self.bots[-FOLLOWERS:]:
            bot.target = self.bots[0].get_position(10)

    # def update(self, dt):
    #     # Step 1: Update all bots
    #     data = [bot.update(self.bots, self.obstacles) for bot in self.bots]
    #     for bot, (angle, magnitude) in zip(self.bots, data):
    #         speed = min(1, 0.2 + magnitude * 0.8)
    #         dx = cos(angle) * dt * SPEED * bot.speed * speed
    #         dy = sin(angle) * dt * SPEED * bot.speed * speed
    #         px, py = bot.position
    #         tx, ty = bot.target
    #         bot.set_position((px + dx, py + dy))
            
    #     # Step 2: Special handling for SearchBots
    #     for bot in self.bots[:3]:  # First three bots are SearchBots
    #         if hypot(bot.position[0] - bot.target[0], bot.position[1] - bot.target[1]) < 10:
    #             new_target = self.select_point()
    #             for search_bot in self.bots[:3]:
    #                 search_bot.target = new_target
    #             break  # Update target for all SearchBots and exit loop

    #     # Step 3: Handling for FollowerBots
    #     for bot in self.bots[-FOLLOWERS:]:
    #         bot.target = self.bots[0].get_position(10)  # Assuming first bot is to be followed
