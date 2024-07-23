import arcade
import random

class Firework(arcade.SpriteCircle):
    def __init__(self, x, y):
        super().__init__(radius=2, color=arcade.color.WHITE)
        self.center_x = x
        self.center_y = y
        self.change_x = random.uniform(-3, 3)
        self.change_y = random.uniform(-3, 3)
        self.alpha = 255

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
        # If alpha below 0 results in error
        # Invalid value for alpha. Must be 0 to 255, received -1
        self.alpha = max(0, self.alpha - 4)
        if self.alpha < 0:
            self.alpha = 0
        self.color = (self.color[0], self.color[1], self.color[2], self.alpha)


def create_firework(x, y):
    particles = arcade.SpriteList()
    for _ in range(100):
        particle = Firework(x, y)
        particles.append(particle)
    return particles

