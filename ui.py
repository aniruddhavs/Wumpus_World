import pygame

pygame.init()
width,height = 640,480
screen=pygame.display.set_mode((width, height))
pygame.display.set_caption("Wumpus World")
fontH = pygame.font.Font('Inter-VariableFont_slnt,wght.ttf', 32)
fontH2 = pygame.font.Font('Inter-VariableFont_slnt,wght.ttf', 26)
fontH3 = pygame.font.Font('Inter-VariableFont_slnt,wght.ttf', 16)

class text_box:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = (255,255,255)
        self.text = text
        self.txt_surface = fontH3.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = (0,0,0) if self.active else (255,255,255)
            self.draw(screen)
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    if len(self.text) <= 1:
                        self.text =''
                        self.txt_surface = fontH3.render(self.text, True, self.color)
                    else:
                        self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                if self.text.isnumeric():
                    self.txt_surface = fontH3.render(self.text, True, self.color)
                self.draw(screen)

    def clear_box(self):
        clear_box_surface = pygame.Surface((self.rect.w, self.rect.h))
        clear_box_surface.fill((179, 179, 179))
        screen.blit(clear_box_surface,self.rect)

    def update(self):
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        self.clear_box()
        self.txt_surface_rect = self.txt_surface.get_rect()
        self.txt_surface_rect.centerx = self.rect.centerx
        self.txt_surface_rect.top = self.rect.top
        screen.blit(self.txt_surface, self.txt_surface_rect)
        pygame.draw.rect(screen, self.color, self.rect, 2)

class Button:
    def __init__(self,x,y,w,h):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = (255,255,255)
        self.Start_surf = fontH2.render("Start", True, (0,0,0))
        self.Start_surf_rect = self.Start_surf.get_rect()
        self.Start_surf_rect.center = self.rect.center
    def draw(self,screen):
        pygame.draw.rect(screen, (127,127,127), self.rect,0,10)
        screen.blit(self.Start_surf, self.Start_surf_rect)

fontH.set_bold(True)
Welcome = fontH.render("Wumpus World",True,(0,0,0))
fontH.set_bold(False)
WelcomeRect = Welcome.get_rect()
WelcomeRect.center = (width//2,height//3)
Selectgrid = fontH2.render("Select A Grid:", True,(0,0,0))
SelectgridRect = Selectgrid.get_rect()
SelectgridRect.centerx = WelcomeRect.centerx
SelectgridRect.top = WelcomeRect.bottom
XSurf = fontH2.render("X", True, (0,0,0))
XSurf_Rect = XSurf.get_rect()
XSurf_Rect.centerx = WelcomeRect.centerx
XSurf_Rect.top = SelectgridRect.bottom+23
x_grid_in = text_box(WelcomeRect.left, SelectgridRect.bottom+25, 100, 25)
y_grid_in = text_box(WelcomeRect.right-100, SelectgridRect.bottom+25, 100, 25)
start_button = Button(WelcomeRect.centerx-75, height-150,150, 50)
flag = True
screen.fill((255,255,255))
newsurf = pygame.Surface((640,480))
newsurf.fill((0,0,0))
newsurf.set_alpha(50)
while True:
    if flag:
        screen.blit(newsurf,(0,0))
        screen.blit(Welcome,WelcomeRect)
        screen.blit(Selectgrid,SelectgridRect)
        screen.blit(XSurf, XSurf_Rect)
        x_grid_in.draw(screen)
        y_grid_in.draw(screen)
        start_button.draw(screen)
        flag = False
    pygame.display.flip()
    for event in pygame.event.get(): 
        x_grid_in.handle_event(event)
        y_grid_in.handle_event(event)
        if event.type==pygame.QUIT:
            pygame.quit() 
            exit(0) 
