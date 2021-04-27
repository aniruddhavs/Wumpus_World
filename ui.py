import pygame

pygame.init()
width,height = 640,480
screen=pygame.display.set_mode((width, height))
pygame.display.set_caption("Wumpus World")
fontH = pygame.font.Font('Inter-VariableFont_slnt,wght.ttf', 32)
fontH2 = pygame.font.Font('Inter-VariableFont_slnt,wght.ttf', 26)
fontH.set_bold(True)
Welcome = fontH.render("Wumpus World",True,(0,0,0))
fontH.set_bold(False)
WelcomeRect = Welcome.get_rect()
WelcomeRect.center = (width//2,height//3)
Selectgrid = fontH2.render("Select A Grid:", True,(0,0,0))
SelectgridRect = Selectgrid.get_rect()
SelectgridRect.centerx = WelcomeRect.centerx
SelectgridRect.top = WelcomeRect.bottom
flag = True
while True:
    screen.fill((255,255,255))
    newsurf = pygame.Surface((640,480))
    newsurf.fill((0,0,0))
    newsurf.set_alpha(50)
    if flag:
        screen.blit(newsurf,(0,0))
        screen.blit(Welcome,WelcomeRect)
        screen.blit(Selectgrid,SelectgridRect)
    pygame.display.flip()
    for event in pygame.event.get(): 
        if event.type == pygame.MOUSEBUTTONUP:
            print(event.pos)
            flag = False
        if event.type==pygame.QUIT:
            pygame.quit() 
            exit(0) 
