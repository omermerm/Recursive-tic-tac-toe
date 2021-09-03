#!/usr/bin/env python3

import sys, pygame
pygame.init()

SIZE = WIDTH, HEIGHT = 600, 800
BLACK = 0, 0, 0


screen = pygame.display.set_mode(SIZE)
grid = pygame.transform.smoothscale(pygame.image.load("empty-tic-tac-toe-gray.png").convert(), [WIDTH, WIDTH])
grid_loc = 0, HEIGHT-WIDTH
X_surf = pygame.transform.smoothscale(pygame.image.load("red-splatter.png").convert(), [int(WIDTH // 3.2), int(WIDTH // 3.2)])
O_surf = pygame.transform.smoothscale(pygame.image.load("blue-splatter.png").convert(), [int(WIDTH // 3.2), int(WIDTH // 3.2)])

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    screen.fill(BLACK)
    screen.blit(grid, grid_loc)
    pygame.display.flip()