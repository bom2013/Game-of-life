# Creadit to Noam Ben Shlomo(bom2013)

import random
import pygame

LIVE = 1
DEAD = 0

class GameOfLife:
    """
    This class operate an entire game of life game
    """

    def __init__(self, height=500, weight=500, cell_size=10, dead_color=(0, 0, 0), live_color=(255, 255, 255), fps=10):
        """
        Constructor of the class

        Create GameOfLife object

        Parameters: 
        height (int): height of the pygame windows in pixels, default value = 500
        weight (int): weight of the pygame windows in pixels, default value = 500
        cell_size (int): Cell size in pixels, default value = 10
        dead_color (rgb tuple): height of the pygame windows, default value = Black (0, 0, 0)
        live_color (rgb tuple): height of the pygame windows, default value = White (255, 255, 255) 
        fps (int>0): fps of the pygame windows,it's determines the "speed" of the game, default value = 10
        
        """

        self.height = height
        self.weight = weight
        self.dead_color = dead_color
        self.live_color = live_color
        self.fps = fps
        self.cell_size = cell_size
        self.row_number = height//cell_size
        self.column_number = weight//cell_size
        self.map = self.get_blank_map()
        self.status = False  # paused

    def reset(self, height=500, weight=500, cell_size=10, dead_color=(0, 0, 0), live_color=(255, 255, 255), fps=10):
        """ 
        Reset game 
    
        Reset game windows and map 
    
        Parameters: 
        height (int): height of the pygame windows in pixels, default value = 500
        weight (int): weight of the pygame windows in pixels, default value = 500
        cell_size (int): Cell size in pixels, default value = 10
        dead_color (rgb tuple): height of the pygame windows, default value = Black (0, 0, 0)
        live_color (rgb tuple): height of the pygame windows, default value = White (255, 255, 255) 
        fps (int>0): fps of the pygame windows,it's determines the "speed" of the game, default value = 10
        
        """
        self.height = height
        self.weight = weight
        self.dead_color = dead_color
        self.live_color = live_color
        self.fps = fps
        self.cell_size = cell_size
        self.row_number = height//cell_size
        self.column_number = weight//cell_size
        self.map = self.get_blank_map()
        self.status = False  # paused

    def get_random_map(self):
        """ 
        Create random map 
    
        Create and return random game of life map 
    
        Returns: 
        int[][]: Random map 
        
        """
        res = []
        for i in range(self.row_number):
            row = []
            for j in range(self.column_number):
                row.append(random.uniform(0, 1))
            res.append(row)
        return res

    def get_blank_map(self):
        """ 
        Create blank map
    
        Returns: 
        int[][]: Blank map
    
        """
        return list(map(lambda x: list(map(lambda x: 0, range(self.column_number))), range(self.row_number)))

    def get_next_generation_map(self):
        """ 
        Return next generation of the map 
    
        Calculate next generation of the map according to game of life rules
    
        Returns: 
        int[][]: Next generation of the map 
    
        """
        new_map = self.get_blank_map()
        for row in range(self.row_number):
            for col in range(self.column_number):
                new_map[row][col] = self.get_next_generation_cell(row, col)
        return new_map

    def refresh(self):
        """ 
        Refresh map 

        Refresh game map(get next generation and draw the new map)

        """
        new_map = self.get_next_generation_map()
        self.map = new_map
        self.draw_map()

    def get_next_generation_cell(self, row, col):
        """ 
        Get the next generation of specific cell 
    
        Parameters: 
        row (int): Cell row
        col (int): Cell column 
    
        Returns: 
        int: Next generation of the cell(LIVE\DEAD) 
    
        """
        number_of_living_neighbors = 0
        # Get all neighbors status
        number_of_living_neighbors += self.get_cell_status(row-1, col-1)
        number_of_living_neighbors += self.get_cell_status(row-1, col)
        number_of_living_neighbors += self.get_cell_status(row, col-1)
        number_of_living_neighbors += self.get_cell_status(row+1, col+1)
        number_of_living_neighbors += self.get_cell_status(row, col+1)
        number_of_living_neighbors += self.get_cell_status(row+1, col)
        number_of_living_neighbors += self.get_cell_status(row-1, col+1)
        number_of_living_neighbors += self.get_cell_status(row+1, col-1)
        old_cell = self.map[row][col]
        if old_cell == LIVE:
            # Death due to loneliness
            if number_of_living_neighbors <= 1:
                return DEAD
            # Death due to overcrowding
            if number_of_living_neighbors > 3:
                return DEAD
        elif number_of_living_neighbors == 3:
            return LIVE
        return old_cell

    def get_cell_status(self, row, col):
        """ 
        Get cell status 
    
        Get cell status(LIVE\DEAD) 
    
        Parameters: 
        row (int): Cell row
        col (int): Cell column 
    
        Returns: 
        int: LIVE\DEAD, if row or col out of range - DEAD 
    
        """
        try:
            return self.map[row][col]
        except:
            return DEAD  # cell not exist

    def get_containing_cell(self, position):
        """ 
        Get containing cell 
    
        Get the containing cell of mouse position 
    
        Parameters: 
        position (int): Mouse position 
    
        Returns: 
        (int, int) : Cell tuple position 
    
        """
        return (position[0] // self.cell_size, position[1] // self.cell_size)

    def draw_map(self):
        """ 
        Draw the map
    
        Draw the game map on the pygame window 
    
        """
        self.screen.fill(self.dead_color)
        for row in range(self.row_number):
            for col in range(self.column_number):
                cell = self.map[row][col]
                rect = pygame.Rect(
                    (row*self.cell_size, col*self.cell_size), (self.cell_size, self.cell_size))
                image = pygame.Surface((self.cell_size, self.cell_size))
                image.fill(self.live_color if cell ==
                           LIVE else self.dead_color)
                self.screen.blit(image, rect)
        pygame.display.update()

    def run(self):
        """ 
        Run the game 

        """
        self.screen = pygame.display.set_mode((self.height, self.weight))
        clock = pygame.time.Clock()
        while True:
            clock.tick(self.fps)
            for event in pygame.event.get():
                # Quit event
                if event.type == pygame.QUIT:
                    quit()
                # Key click events
                if event.type == pygame.KEYDOWN:
                    # Pause\Resume
                    if event.unicode == " ":
                        self.status = not self.status
                    # Reset
                    if event.unicode == "r":
                        self.reset()
                        self.draw_map()
                    # Increase speed
                    if event.unicode == "+":
                        self.fps += 2
                    # Decrease speed
                    if event.unicode == "-":
                        if self.fps>2:
                            self.fps -= 2
                # Check click event
                if event.type == pygame.MOUSEBUTTONUP:
                    cont_cell = self.get_containing_cell(pygame.mouse.get_pos())
                    # Swap between LIVE(1) and DEAD(0)
                    self.map[cont_cell[0]][cont_cell[1]] = not self.map[cont_cell[0]][cont_cell[1]]
                    self.draw_map()
            if self.status:
                self.refresh()


game = GameOfLife()
game.run()
