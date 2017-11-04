"""Implementation of Conway's game of life"""
import numpy as np
import pygame
import sys


class Display:

    def __init__(self, resolution: tuple = (1280, 720), update_list=(), fps=10, clock=True):
        """Initializes everything"""
        # try:
        #     sys
        # except:
        #     import sys
        # try:
        #     pygame
        # except:
        #     import pygame

        pygame.init()
        self.resolution = resolution
        self.screen = pygame.display.set_mode(resolution)
        self.screen.fill((255, 255, 255))
        self.update_list = [update_list]
        if clock:
            self.clock = pygame.time.Clock()
        self.fps = fps

    def update(self):
        """Updates display and fills it with white"""
        if self.update_list:
            for item in self.update_list:
                item(self.screen, self)
        pygame.display.flip()
        self.screen.fill((255, 255, 255))
        self.clock.tick(self.fps)


class Conway:
    """Conway's game of life"""

    def __init__(self, grid_size: tuple = (45, 80), random: bool = True):
        """Initializes the class
            The grid size is (height, width)"""
        if random:
            self.array = np.random.randint(low=0, high=2, size=grid_size)
            self.new_array = np.random.randint(low=0, high=2, size=grid_size)
        else:
            self.array = np.random.randint(low=0, high=1, size=grid_size)
            self.new_array = np.random.randint(low=0, high=2, size=grid_size)
        self.size = grid_size

    def get_array(self):
        """Returns array"""
        return self.array

    def next_gen(self):
        """Goes to next generation"""
        self.new_array = np.copy(self.array)
        for h in range(self.size[0]):
            for w in range(self.size[1]):
                neighbors = self.array[h - 1, w - 1] + self.array[h - 1, w] + self.array[h - 1, (w + 1) % self.size[1]] + self.array[h,(w + 1) % self.size[1]] + self.array[(h + 1) % self.size[0], (w + 1) % self.size[1]] + self.array[(h + 1) % self.size[0], w] + self.array[(h + 1) % self.size[0], w - 1] + self.array[h, w - 1]
                if self.array[h, w] == 0 and neighbors == 3:
                    self.new_array[h, w] = 1
                elif self.array[h, w] == 1 and neighbors not in (2, 3):
                    self.new_array[h, w] = 0
        self.array = np.copy(self.new_array)

    def change_cell(self, cell):
        """Changes cell's state
            cell format (h, w)"""
        #moze dict?
        if self.array[cell]:
            self.array[cell] = 0
        else:
            self.array[cell] = 1

    def is_dead(self, cell):
        """Return whether or not the cell is dead
            cell format (h, w)"""
        return bool(self.array[cell])

    def update(self, screen):
        """Updates itself"""
        self.next_gen()
        self.draw(screen)

    def draw(self, screen, display):
        for h in range(self.size[0]):
            for w in range(self.size[1]):
                if self.array[h, w]:
                    pygame.draw.rect(screen, (0, 0, 0), (w * display.resolution[0]/self.size[1], h * display.resolution[1]/self.size[0], display.resolution[0]/self.size[1], display.resolution[1]/self.size[0]))


def main():
    """Just main function"""
    auto = False
    game = Conway(random=True)
    display = Display(update_list=(game.draw))
    while(1):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game.next_gen()
                elif event.key == pygame.K_r:
                    auto = not auto
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                pos = (int(pos[1] // (display.resolution[1] / game.size[0])), int(pos[0] // (display.resolution[0] / game.size[1])))
                game.change_cell(pos)
        if auto:
            game.next_gen()
        display.update()


main()
