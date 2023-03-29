
import sys, pygame
import math
import time, random

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BACKGROUND_COLOR = (46, 52, 64)

SUN_COLOR = (255, 255, 0)
PROJECTILE_COLOR = (0, 0, 255)

GRAVITATIONAL_CONSTANT = 9.81

VELOCITY_REDUCTION_FACTOR = 0.15

BLOCK_SIZE = 5
NUM_BLOCK_W = (int)(SCREEN_WIDTH/BLOCK_SIZE)
NUM_BLOCK_H = (int)(SCREEN_HEIGHT/BLOCK_SIZE)

BLOCK_COLOR = (0, 255, 0)

FPS = 10
fpsClock = pygame.time.Clock()

class Utils:

    @staticmethod
    def xComponent(component, angle):
        return math.cos(angle)*component

    @staticmethod
    def yComponent(component, angle):
        return math.sin(angle)*component

    @staticmethod
    def calculateAngle(cp1, cp2):
        a = cp1[0] - cp2[0]
        b = cp1[1] - cp2[1]
        if cp1[0] - cp2[0] < 0:
            angle = math.atan(b/a) + math.pi
        else:
            angle = math.atan(b / a)
        return angle

    @staticmethod
    def calculateRadius(cp1, cp2):
        a = abs(cp2[0] - cp1[0])
        b = abs(cp2[1] - cp1[1])
        c = math.sqrt(a**2+b**2)
        return c

    @staticmethod
    def forceOfGravity(m1, m2, r):
        fgrav = (GRAVITATIONAL_CONSTANT*m1*m2) / r**2
        return fgrav

    @staticmethod
    def countNumberAliveNeighbors(map, hi, vi):
        count = 0

        try:
            if map[hi-1][vi] == 1:
                count += 1
            if map[hi+1][vi] == 1:
                count += 1
            if map[hi][vi-1] == 1:
                count += 1
            if map[hi][vi+1] == 1:
                count += 1

            if map[hi-1][vi-1] == 1:
                count += 1
            if map[hi-1][vi+1] == 1:
                count += 1
            if map[hi+1][vi-1] == 1:
                count += 1
            if map[hi+1][vi+1] == 1:
                count += 1

        except:
            return count

        return count

class Renderer:

    @staticmethod
    def __drawBackground():
        screen.fill(BACKGROUND_COLOR)

    @staticmethod
    def __drawBlocks():
        cellsMap = GameWorld.cellsMap

        for i in range(len(cellsMap)):
            for ii in range(len(cellsMap[i])):
                value = cellsMap[i][ii]
                if value == 1:
                    blockRect = pygame.Rect((ii*BLOCK_SIZE, i*BLOCK_SIZE),
                                               (BLOCK_SIZE, BLOCK_SIZE))
                    pygame.draw.rect(screen, BLOCK_COLOR, blockRect)

    @staticmethod
    def draw():

        Renderer.__drawBackground()
        Renderer.__drawBlocks()


class GameWorld:

    @staticmethod
    def init():
        cellsHMap = []
        cellsMap = []

        for i in range(NUM_BLOCK_H):
            cellsHMap = []
            for ii in range(NUM_BLOCK_W):
                cellsHMap.append(random.randint(0,1))
            cellsMap.append(cellsHMap)



        GameWorld.cellsMap = cellsMap

    @staticmethod
    def reset():
        return None


    @staticmethod
    def quit():
        return None

    @staticmethod
    def update():

        cellsMap = GameWorld.cellsMap

        newCellsMap = []
        for i in range(NUM_BLOCK_H):
            cellsHMap = []
            for ii in range(NUM_BLOCK_W):
                cellsHMap.append(0)
            newCellsMap.append(cellsHMap)

        for i in range(len(cellsMap)):
            for ii in range(len(cellsMap[i])):
                value = cellsMap[i][ii]
                numAliveNeighbors = Utils.countNumberAliveNeighbors(cellsMap, i, ii)
                if value == 1:
                    if (numAliveNeighbors == 2 or numAliveNeighbors == 3):
                        newCellsMap[i][ii] = 1
                    else:
                        newCellsMap[i][ii] = 0
                elif value == 0:
                    if numAliveNeighbors == 3:
                        newCellsMap[i][ii] = 1
                    else:
                        newCellsMap[i][ii] = 0

        GameWorld.cellsMap = newCellsMap


if __name__ == '__main__':

    size = SCREEN_WIDTH, SCREEN_HEIGHT
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Game of Life")

    prev_time = time.time()

    GameWorld.init()

    running = True

    while running:

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                running = False

        GameWorld.update()
        Renderer.draw()

        pygame.display.flip()
        fpsClock.tick(FPS)

    GameWorld.quit()
