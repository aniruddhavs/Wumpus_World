import pygame

pygame.init()
width,height = 640,480
screen=pygame.display.set_mode((width, height))
pygame.display.set_caption("Wumpus World")
fontH = pygame.font.Font('Inter-VariableFont_slnt,wght.ttf', 32)
fontH2 = pygame.font.Font('Inter-VariableFont_slnt,wght.ttf', 26)
fontH3 = pygame.font.Font('Inter-VariableFont_slnt,wght.ttf', 16)
fontH4 = pygame.font.Font('Inter-VariableFont_slnt,wght.ttf', 14)
# stench_img = pygame.image.load("icons/Stech.PNG")
# stench_img = pygame.transform.scale(stench_img, (25,25))

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
                    self.text = event.unicode
                if self.text.isnumeric():
                    self.txt_surface = fontH3.render(self.text, True, self.color)
                self.draw(screen)

    def clear_box(self):
        clear_box_surface = pygame.Surface((self.rect.w, self.rect.h))
        clear_box_surface.fill((179, 179, 179))
        screen.blit(clear_box_surface,self.rect)

    def draw(self, screen):
        self.clear_box()
        self.txt_surface_rect = self.txt_surface.get_rect()
        self.txt_surface_rect.centerx = self.rect.centerx
        self.txt_surface_rect.top = self.rect.top
        screen.blit(self.txt_surface, self.txt_surface_rect)
        pygame.draw.rect(screen, self.color, self.rect, 2)

class Button:
    def __init__(self,x,y,w,h,text):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = (255,255,255)
        self.Start_surf = fontH2.render(text, True, (25,25,25))
        self.Start_surf_rect = self.Start_surf.get_rect()
        self.Start_surf_rect.center = self.rect.center
    def draw(self,screen):
        self.surf = pygame.Surface((self.rect.w,self.rect.h),pygame.SRCALPHA)
        self.surf.fill((127,127,127,0))
        new_rect = pygame.Rect.copy(self.rect)
        new_rect.x,new_rect.y = 0,0
        pygame.draw.rect(self.surf, (127,127,127), new_rect,0,10)
        screen.blit(self.surf, self.rect)
        screen.blit(self.Start_surf, self.Start_surf_rect)
    def when_clicked(self,event,a,b):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                try:
                    clear_surf = pygame.Surface((self.error_surf_rect.w,self.error_surf_rect.h))
                    clear_surf.fill((195,195,195))
                    screen.blit(clear_surf, self.error_surf_rect)
                except:
                    pass
                if a == '' or b == '':
                    self.error_surf = fontH4.render("Enter the grid size", True, (0,0,0))
                    self.error_surf_rect = self.error_surf.get_rect()
                    self.error_surf_rect.centerx = self.rect.centerx
                    self.error_surf_rect.bottom = self.rect.top-10
                    screen.blit(self.error_surf, self.error_surf_rect)
                    return True
                elif a > '8' or b > '8' or a < '2' or b < '2':
                    self.error_surf = fontH4.render("Invalid grid size (Lower Limit=2,Upper Limit=8)", True, (0,0,0))
                    self.error_surf_rect = self.error_surf.get_rect()
                    self.error_surf_rect.centerx = self.rect.centerx
                    self.error_surf_rect.bottom = self.rect.top-10
                    screen.blit(self.error_surf, self.error_surf_rect)
                    return True
                else:
                    return False
            else:
                return True
        else:
            return True

class Grid_comp:
    def __init__(self,count_x,count_y,size_x,size_y,left,top):
        self.sizex = size_x
        self.sizey = size_y
        self.rect = pygame.Rect(left,top,size_x,size_y)
        self.position = [count_x,count_y]

    def draw(self,screen,x = None,y = None):
        self.surface = pygame.Surface((self.sizex,self.sizey))
        self.surface.fill((255,255,255))
        if x and y:
            new_rect = pygame.Rect.copy(self.rect)
            new_rect.left = x
            new_rect.top = y
            screen.blit(self.surface, new_rect)
        else:
            screen.blit(self.surface,self.rect)

    def is_selected(self,event):
        if self.rect.collidepoint(event):
            return True
        else:
            return False

class setup_component:
    pass

class Grid:
    def __init__(self,x,y):
        self.x = y
        self.y = x
        self.rect = pygame.Rect(0,0,400,400)
        self.size_x,self.size_y = 380//int(self.x),380//int(self.y)

    def draw(self,screen,x,y):
        self.rect.center = (x,y)
        clear_grid_surface = pygame.Surface((400,400))
        clear_grid_surface.fill((0,0,0))
        screen.blit(clear_grid_surface, self.rect)
        count_x = 0
        self.grid_comp_list = []
        for i in range(self.rect.left+2,self.rect.left+380,self.size_x+2):
            count_y = 0
            for j in range(self.rect.top+2,self.rect.top+380,self.size_y+2):
                square = Grid_comp(count_x,count_y,self.size_x,self.size_y,i,j)
                self.grid_comp_list.append(square)
                square.draw(screen)
                count_y += 1
            count_x += 1
        for i in self.grid_comp_list:
            print(i.position)

    def setup(self,screen,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                screen.fill((255,255,255))
                grid.draw(screen, 210, 225)
                mask_surface = pygame.Surface((640,480))
                mask_surface.fill((0,0,0))
                mask_surface.set_alpha(50)
                screen.blit(mask_surface, (0,0))
                for i in self.grid_comp_list:
                    if i.is_selected(event.pos):
                        count_x,count_y = i.position
                        x = count_x*(self.size_x+2)+12
                        y = count_y*(self.size_y+2)+27
                        i.draw(screen,x=x,y=y)

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
start_button = Button(WelcomeRect.centerx-75, height-150,150, 50,"Start")
flag = True
grid_setup_flag = True
screen.fill((255,255,255))
newsurf = pygame.Surface((640,480))
newsurf.fill((195,195,195))
while grid_setup_flag:
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
        grid_setup_flag = start_button.when_clicked(event,x_grid_in.text,y_grid_in.text)
        if event.type==pygame.QUIT:
            pygame.quit() 
            exit(0) 
grid = Grid(x_grid_in.text,y_grid_in.text)
screen.fill((255,255,255))
grid.draw(screen,width//2,height//2)
pygame.display.flip()
while True:
    for event in pygame.event.get(): 
        if event.type == pygame.MOUSEBUTTONDOWN:
            grid.setup(screen, event)
            pygame.display.flip()
        if event.type==pygame.QUIT:
            pygame.quit() 
            exit(0)