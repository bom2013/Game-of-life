import random
import pygame


class GameOfLife:
    def __init__(self, height=400, weight=400, cell_size=5, dead_color=(0, 0, 0), live_color=(255, 255, 255), fps=30):
        self.height = height
        self.weight = weight
        self.dead_color = dead_color
        self.live_color = live_color
        self.fps = fps
        self.cell_size = cell_size
        self.row_number = height//cell_size
        self.column_number = weight//cell_size
        self.map = self.get_blank_map()

    def get_random_map(self):
        res = []
        for i in range(self.row_number):
            row = []
            for j in range(self.column_number):
                row.append(random.uniform(0, 1))
            res.append(row)
        return res

    def get_blank_map(self):
        return self.row_number*[[0]*self.column_number]

    def get_next_generation_map(self):
        new_map = self.get_blank_map()
        for row in range(self.row_number):
            for col in range(self.column_number):
                try:
                    new_map[row][col] = self.get_next_generation_cell(row, col)
                except:
                    pass
        return new_map

    def refresh(self):
        new_map = self.get_next_generation_map()
        self.map = new_map
        self.draw_map()

    def get_next_generation_cell(self, row, col):
        number_of_living_neighbors = 0
        number_of_living_neighbors = self.get_cell_status(row-1, col-1)
        number_of_living_neighbors = self.get_cell_status(row-1, col)
        number_of_living_neighbors = self.get_cell_status(row, col-1)
        number_of_living_neighbors = self.get_cell_status(row+1, col+1)
        number_of_living_neighbors = self.get_cell_status(row, col+1)
        number_of_living_neighbors = self.get_cell_status(row+1, col)
        number_of_living_neighbors = self.get_cell_status(row-1, col+1)
        number_of_living_neighbors = self.get_cell_status(row+1, col-1)
        old_cell = self.map[row][col]
        if old_cell == 1:
            # Death due to loneliness
            if number_of_living_neighbors <= 1:
                return 0
            # Death due to overcrowding
            if number_of_living_neighbors > 3:
                return 0
        elif number_of_living_neighbors == 3:
            return 1
        return old_cell

    def get_cell_status(self, row, col):
        try:
            return self.map[row][col]
        except:
            return 0

    def draw_map(self):
        self.screen.fill(self.dead_color)
        for row in range(self.row_number):
            for col in range(self.column_number):
                cell = self.map[row][col]
                rect = pygame.Rect((row*self.cell_size, col*self.cell_size),(self.cell_size, self.cell_size))
                image = pygame.Surface((self.cell_size, self.cell_size))
                image.fill(self.live_color if cell == 1 else self.dead_color)
                self.screen.blit(image, rect)
        pygame.display.update()

    def run(self):
        self.screen = pygame.display.set_mode((self.height, self.weight))
        clock = pygame.time.Clock()
        while True:
            clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
            self.refresh()


game = GameOfLife()
game.run()
