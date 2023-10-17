#!/usr/local/bin/python3
"""

SlangSneek

by Diamino 2021

"""
import pygame
import time
import math
import random
from collections import deque

# Constants
GRIDSIZE = GRIDWIDTH, GRIDHEIGHT = (20, 20)
SNEEKSIZE = (20, 20)
DISPLAYSIZE = (GRIDWIDTH * SNEEKSIZE[0], GRIDHEIGHT * SNEEKSIZE[1])
FGCOLOR = "blue"
BGCOLOR = "grey"
SNACKCOLOR = "green"
GOCOLOR = "red" # Game Over color
FPS = 30

DIR_DOWN = (0,1)
DIR_UP = (0,-1)
DIR_LEFT = (-1, 0)
DIR_RIGHT = (1, 0)

DIR_LEFT_RIGHT = (DIR_LEFT, DIR_RIGHT)
DIR_UP_DOWN = (DIR_UP, DIR_DOWN)

# Classes

class Slang:

    def __init__(self, surface, size=SNEEKSIZE, color=FGCOLOR, direction=DIR_DOWN, location=(GRIDWIDTH/2, GRIDHEIGHT/2), speed=1):
        self.surface = surface
        self.size = size
        self.color = color
        self.direction = direction
        self.speed  = speed
        self.tail = deque([location])
        self.counter = 0
        self.increase = 0
        self.moved = True

    def change_direction(self, direction):
        if self.moved:
            if (self.direction in DIR_UP_DOWN and direction in DIR_LEFT_RIGHT) or (self.direction in DIR_LEFT_RIGHT and direction in DIR_UP_DOWN):
                self.direction = direction
                self.moved = False

    def grow(self, size=1):
        self.increase = size

    def move(self, snacks):
        self.counter += 1
        if math.floor(self.counter % (FPS / self.speed)) == 0:
            self.moved = True
            new_x = int(self.tail[0][0] + self.direction[0]) % GRIDWIDTH
            new_y = int(self.tail[0][1] + self.direction[1]) % GRIDHEIGHT
            location = (new_x, new_y)

            if self.increase == 0:
                savetail = self.tail.pop()
            else:
                self.increase -= 1
                savetail = None

            # Collision detection
            if location in self.tail: # with tail
                self.color = GOCOLOR
                self.tail.append(savetail) # Restore tail
                return False
            elif location in snacks.snacks: # with snack
                self.grow()
                snacks.remove_snack(location)
                snacks.initiate_snack(self.tail)
            
            self.tail.appendleft(location)
        
        return True

    def draw(self):
        for part in self.tail:
            lefttop = (part[0] * SNEEKSIZE[0], part[1] * SNEEKSIZE[1])
            pygame.draw.rect(self.surface, self.color, pygame.Rect(lefttop, SNEEKSIZE))

class Snacks:

    def __init__(self, surface, color=SNACKCOLOR):
        self.surface = surface
        self.color = color
        self.snacks = []

    def initiate_snack(self, snaketail, number=1):
        for i in range(number):
            location = None
            while location is None:
                location = (random.randrange(GRIDWIDTH), random.randrange(GRIDHEIGHT))
                if location in snaketail:
                    location = None
            self.snacks.append(location) 

    def remove_snack(self, location):
        self.snacks.remove(location)

    def draw(self):
        for snack in self.snacks:
            lefttop = (snack[0] * SNEEKSIZE[0], snack[1] * SNEEKSIZE[1])
            pygame.draw.rect(self.surface, self.color, pygame.Rect(lefttop, SNEEKSIZE))

#  
pygame.init()

screen = pygame.display.set_mode(DISPLAYSIZE)
pygame.display.set_caption("Sneek de Slang")
clock = pygame.time.Clock()

sneek = Slang(screen, speed=4)
sneek.draw()
snacks = Snacks(screen)
snacks.initiate_snack(sneek.tail)
snacks.draw()

pygame.display.update()

playing = True

try:
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            # process events
            if event.type == pygame.QUIT:
                raise KeyboardInterrupt
            elif event.type == pygame.KEYDOWN and playing:
                if event.key == pygame.K_SPACE:
                    sneek.grow()
                elif event.key == pygame.K_LEFT:
                    sneek.change_direction(DIR_LEFT)
                elif event.key == pygame.K_RIGHT:
                    sneek.change_direction(DIR_RIGHT)
                elif event.key == pygame.K_DOWN:
                    sneek.change_direction(DIR_DOWN)
                elif event.key == pygame.K_UP:
                    sneek.change_direction(DIR_UP)
            

        # Update sprites
        if playing:
            playing = sneek.move(snacks)
            screen.fill(BGCOLOR)
            sneek.draw()
            snacks.draw()

            pygame.display.update()
except KeyboardInterrupt:
    pass

pygame.quit()