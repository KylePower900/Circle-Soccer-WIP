import pygame
from Configuration import *
from Entities import * 
from Methods import *  

running = True
while running:
    pygame.time.Clock().tick(240)
    
    SCREEN.fill((255,255,255))

    mouseUP = False
    mouseDOWN = False

    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            running = False
        if i.type == pygame.MOUSEBUTTONDOWN:
            mouseDOWN = True
        if i.type == pygame.MOUSEBUTTONUP:
            mouseUP = True
            
        
    MatchRunning(list_of_circles, mouseUP, mouseDOWN)
    pygame.display.update() 