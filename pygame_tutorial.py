import pygame
import os

PATH = os.path.join(os.getcwd(), 'Project 1 - Search') 

pygame.init()

screen = pygame.display.set_mode((800, 600))

# Title and Icon
pygame.display.set_caption("Gifuto Unpansha")
icon = pygame.image.load(os.path.join(PATH, 'images/logo_rmbg.png'))
pygame.display.set_icon(icon)

playerImg = pygame.image.load(os.path.join(PATH, 'images/logo_rmbg.png'))


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 211, 0))
    pygame.display.update()