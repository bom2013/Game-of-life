import random
import pygame


class GameOfLife:
    def __init__(self, height=400, weight=400, dead_color=(0, 0, 0), live_color=(255, 255, 255), fps=30):
        self.height = height
        self.weight = weight
        self.dead_color = dead_color
        self.live_color = live_color
        self.fps = fps

    def run(self):
        screen = pygame.display.set_mode((self.height, self.weight))
        clock = pygame.time.Clock()
        while True:
            clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()


game = GameOfLife()
game.run()
