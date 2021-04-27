import pygame

pygame.init()
width,height = 640,480
screen=pygame.display.set_mode((width, height))
pygame.display.set_caption("Wumpus World")
flag = True
while True:
    screen.fill((255,255,255))
    newsurf = pygame.Surface((640,480))
    newsurf.fill((0,0,0))
    newsurf.set_alpha(50)
    if flag:
        screen.blit(newsurf,(0,0))
    pygame.display.flip()
    for event in pygame.event.get(): 
        if event.type == pygame.MOUSEBUTTONUP:
            print(event.pos)
            flag = False
        if event.type==pygame.QUIT:
            pygame.quit() 
            exit(0) 
