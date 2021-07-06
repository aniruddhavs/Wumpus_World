import pygame
from pygame.display import update

pygame.init()
width,height = 640,480
screen=pygame.display.set_mode((width, height))
pygame.display.set_caption("Wumpus World")
fontH = pygame.font.Font('Inter-VariableFont_slnt,wght.ttf', 32)
fontH2 = pygame.font.Font('Inter-VariableFont_slnt,wght.ttf', 26)
fontH3 = pygame.font.Font('Inter-VariableFont_slnt,wght.ttf', 16)
fontH4 = pygame.font.Font('Inter-VariableFont_slnt,wght.ttf', 14)
stench_img = pygame.image.load("icons/Stench.png")
gold_img = pygame.image.load("icons/Gold.png")
pit_img = pygame.image.load("icons/Pit.png")
wumpus_img = pygame.image.load("icons/Wumpus.png")
breeze_img = pygame.image.load("icons/Breeze.png")
agent_img = pygame.image.load("icons/Agent.png")

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
    def start_event(self,event,screen,a,g,w):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                try:
                    clear_surf = pygame.Surface((self.error_surf_rect.w,self.error_surf_rect.h))
                    clear_surf.fill((255,255,255))
                    screen.blit(clear_surf, self.error_surf_rect)
                except:
                    pass
                if a and g and w:
                    return False
                else:
                    self.error_surf = fontH4.render("Must contain Agent,Gold and Wumpus", True, (0,0,0))
                    self.error_surf_rect = self.error_surf.get_rect()
                    self.error_surf_rect.centerx = 320
                    self.error_surf_rect.bottom = 460
                    screen.blit(self.error_surf, self.error_surf_rect)
                    return True
            else:
                return True
        else:
            return True

class Grid_comp:
    def __init__(self,count_x,count_y,size_x,size_y,left=None,top=None):
        self.sizex = size_x
        self.sizey = size_y
        self.rect = pygame.Rect(0,0,size_x,size_y)
        self.position = (count_x,count_y)
        self.content = 0
        self.effect = 0
        global agent_img
        global pit_img
        global breeze_img
        global gold_img
        global stench_img
        global wumpus_img
        scale_factor = min(size_x,size_y)
        self.scaled_agent = pygame.transform.scale(agent_img,(scale_factor,scale_factor))
        self.scaled_pit = pygame.transform.scale(pit_img,(scale_factor,scale_factor))
        self.scaled_wumpus = pygame.transform.scale(wumpus_img,(scale_factor,scale_factor))
        self.scaled_gold = pygame.transform.scale(gold_img,(scale_factor,scale_factor))
        self.full_scale_img = {1:self.scaled_agent,
                               2:self.scaled_gold,
                               3:self.scaled_pit,
                               4:self.scaled_wumpus}
        self.half_scaled_agent = pygame.transform.scale(agent_img,(scale_factor//2,scale_factor//2))
        self.half_scaled_pit = pygame.transform.scale(pit_img,(scale_factor//2,scale_factor//2))
        self.half_scaled_wumpus = pygame.transform.scale(wumpus_img,(scale_factor//2,scale_factor//2))
        self.half_scaled_gold = pygame.transform.scale(gold_img,(scale_factor//2,scale_factor//2))
        self.half_scale_img = {1:self.half_scaled_agent,
                               2:self.half_scaled_gold,
                               3:self.half_scaled_pit,
                               4:self.half_scaled_wumpus}
        self.scaled_stench = pygame.transform.scale(stench_img,(scale_factor,scale_factor))
        self.scaled_breeze = pygame.transform.scale(breeze_img,(scale_factor,scale_factor))
        self.full_scaled_effects = {1:self.scaled_breeze,
                                    2:self.scaled_stench}
        self.half_scaled_stench = pygame.transform.scale(stench_img,(scale_factor//2,scale_factor//2))
        self.half_scaled_breeze = pygame.transform.scale(breeze_img,(scale_factor//2,scale_factor//2))
        self.half_scaled_effects = {1:self.half_scaled_breeze,
                                    2:self.half_scaled_stench}

    def update_co_ordinates(self,left,top):
        self.rect.left,self.rect.top = left,top

    def draw(self,screen,x = None,y = None,draw_agent = True,draw_effects = True):
        self.surface = pygame.Surface((self.sizex,self.sizey))
        self.surface.fill((255,255,255))
        if x and y:
            new_rect = pygame.Rect.copy(self.rect)
            new_rect.left = x
            new_rect.top = y
        else:
            new_rect = pygame.Rect.copy(self.rect)
        screen.blit(self.surface, new_rect)
        if self.content == 1 and not draw_agent:
            if self.effect >= 1:
                if self.effect == 3:
                    half_rect = pygame.Rect.copy(new_rect)
                    half_rect.width,half_rect.height = half_rect.width//2,half_rect.height//2
                    half_rect.top = new_rect.top
                    half_rect.left = new_rect.left
                    screen.blit(self.half_scaled_effects[1], half_rect)
                    half_rect.right = new_rect.right
                    screen.blit(self.half_scaled_effects[2], half_rect)
                else:
                    screen.blit(self.full_scaled_effects[self.effect], new_rect)
        elif self.content >=1:
            if self.effect >= 1 and draw_effects:
                half_rect = pygame.Rect.copy(new_rect)
                half_rect.width,half_rect.height = half_rect.width//2,half_rect.height//2
                half_rect.centerx = new_rect.centerx
                half_rect.bottom = new_rect.bottom
                screen.blit(self.half_scale_img[self.content], half_rect)
                half_rect.top = new_rect.top
                if self.effect == 3:
                    half_rect.left = new_rect.left
                    screen.blit(self.half_scaled_effects[1], half_rect)
                    half_rect.right = new_rect.right
                    screen.blit(self.half_scaled_effects[2], half_rect)
                else:
                    screen.blit(self.half_scaled_effects[self.effect], half_rect)
            else:
                screen.blit(self.full_scale_img[self.content], new_rect)
        if self.content == 0:
            if self.effect >= 1:
                if self.effect == 3:
                    half_rect = pygame.Rect.copy(new_rect)
                    half_rect.width,half_rect.height = half_rect.width//2,half_rect.height//2
                    half_rect.top = new_rect.top
                    half_rect.left = new_rect.left
                    screen.blit(self.half_scaled_effects[1], half_rect)
                    half_rect.right = new_rect.right
                    screen.blit(self.half_scaled_effects[2], half_rect)
                else:
                    screen.blit(self.full_scaled_effects[self.effect], new_rect)

class setup_component:
    def __init__(self):
        self.agent_rect = pygame.Rect(435,75,200,65)
        self.gold_rect = pygame.Rect(435,155,200,65)
        self.pit_rect = pygame.Rect(435,235,200,65)
        self.wumpus_rect = pygame.Rect(435,315,200,65)
        self.clear_rect = pygame.Rect(435,395,200,65)

    def draw_options(self,screen):
        global agent_img,gold_img,pit_img,wumpus_img
        global fontH2
        scaled_agent_img = pygame.transform.scale(agent_img, (65, 65))
        scaled_gold_img = pygame.transform.scale(gold_img, (65, 65))
        scaled_pit_img = pygame.transform.scale(pit_img, (65, 65))
        scaled_wumpus_img = pygame.transform.scale(wumpus_img, (65, 65))
        text_surf = fontH2.render("Choose:",True, (0,0,0))
        text_rect = text_surf.get_rect()
        text_rect.left = 435
        text_rect.top = 25
        agent_option_surf = fontH2.render("Agent",True, (0,0,0))
        agent_option_rect = agent_option_surf.get_rect()
        agent_option_rect.left = self.agent_rect.left+5
        agent_option_rect.centery = self.agent_rect.centery
        gold_option_surf = fontH2.render("Gold",True, (0,0,0))
        gold_option_rect = gold_option_surf.get_rect()
        gold_option_rect.left = self.gold_rect.left+5
        gold_option_rect.centery = self.gold_rect.centery
        pit_option_surf = fontH2.render("Pit",True, (0,0,0))
        pit_option_rect = pit_option_surf.get_rect()
        pit_option_rect.left = self.pit_rect.left+5
        pit_option_rect.centery = self.pit_rect.centery
        wumpus_option_surf = fontH2.render("Wumpus",True, (0,0,0))
        wumpus_option_rect = wumpus_option_surf.get_rect()
        wumpus_option_rect.left = self.wumpus_rect.left+5
        wumpus_option_rect.centery = self.wumpus_rect.centery
        clear_option_surf = fontH2.render("Clear",True, (0,0,0))
        clear_option_rect = clear_option_surf.get_rect()
        clear_option_rect.center = self.clear_rect.center
        option_img_rect = scaled_agent_img.get_rect()
        option_img_rect.right = self.agent_rect.right-20
        option_img_rect.centery = self.agent_rect.centery
        agent_surf = pygame.Surface((200,65),pygame.SRCALPHA)
        agent_surf.fill((255,255,255,0))
        new_rect = pygame.Rect.copy(self.agent_rect)
        new_rect.x,new_rect.y = 0,0
        pygame.draw.rect(agent_surf, (255,255,255), new_rect,0,10)
        screen.blit(agent_surf, self.agent_rect)
        screen.blit(agent_surf, self.gold_rect)
        screen.blit(agent_surf, self.pit_rect)
        screen.blit(agent_surf, self.wumpus_rect)
        screen.blit(agent_surf, self.clear_rect)
        screen.blit(text_surf,text_rect)
        screen.blit(agent_option_surf,agent_option_rect)
        screen.blit(scaled_agent_img,option_img_rect)
        screen.blit(gold_option_surf,gold_option_rect)
        option_img_rect.centery = self.gold_rect.centery
        screen.blit(scaled_gold_img,option_img_rect)
        screen.blit(pit_option_surf,pit_option_rect)
        option_img_rect.centery = self.pit_rect.centery
        screen.blit(scaled_pit_img,option_img_rect)
        screen.blit(wumpus_option_surf,wumpus_option_rect)
        option_img_rect.centery = self.wumpus_rect.centery
        screen.blit(scaled_wumpus_img,option_img_rect)
        screen.blit(clear_option_surf,clear_option_rect)

    def option_select(self,event,prev_content):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.agent_rect.collidepoint(event.pos):
                return prev_content*10+1
            elif self.gold_rect.collidepoint(event.pos):
                return prev_content*10+2
            elif self.pit_rect.collidepoint(event.pos):
                return prev_content*10+3
            elif self.wumpus_rect.collidepoint(event.pos):
                return prev_content*10+4
            elif self.clear_rect.collidepoint(event.pos):
                return prev_content*10
            else:
                return prev_content

class Grid:
    def __init__(self,x,y):
        self.x = y
        self.y = x
        self.rect = pygame.Rect(0,0,400,400)
        self.size_x,self.size_y = 380//int(self.x),380//int(self.y)
        self.selected_grid_comp = -1
        self.gold_present = False
        self.wumpus_present = False
        self.agent_present = False
        count_x = 0
        self.grid_comp_list = []
        self.agent_position = [-1,-1]
        self.agent_index = -1
        self.start_button = Button(550,220,80,40,"Start!")
        for _ in range(self.rect.left+2,self.rect.left+380,self.size_x+2):
            count_y = 0
            for _ in range(self.rect.top+2,self.rect.top+380,self.size_y+2):
                square = Grid_comp(count_x,count_y,self.size_x,self.size_y)
                self.grid_comp_list.append(square)
                count_y += 1
            count_x += 1

    def draw(self,screen,x,y,draw_agent = True,show_button=True):
        self.rect.center = (x,y)
        clear_grid_surface = pygame.Surface((400,400))
        clear_grid_surface.fill((0,0,0))
        index = 0
        screen.blit(clear_grid_surface, self.rect)
        for i in range(self.rect.left+2,self.rect.left+380,self.size_x+2):
            for j in range(self.rect.top+2,self.rect.top+380,self.size_y+2):
                self.grid_comp_list[index].update_co_ordinates(i,j)
                self.grid_comp_list[index].draw(screen,draw_agent = draw_agent)
                index += 1 
        if show_button:
            self.start_button.draw(screen)

    def move(self,screen,direction):
        # print("Move is called")
        # print(direction)
        # print(self.agent_position)
        if self.agent_present:
            x,y = self.grid_comp_list[self.agent_index].rect.left,self.grid_comp_list[self.agent_index].rect.top
            if direction == 0 or direction == 1:
                movement_length = self.grid_comp_list[self.agent_index].sizex
            elif direction == 2 or direction == 3:
                movement_length = self.grid_comp_list[self.agent_index].sizey
            if self.agent_position[0] in range(0,int(self.x)-1) and direction == 0:
                flag = True
            elif self.agent_position[0] in range(1,int(self.x)) and direction == 1:
                flag = True
            elif self.agent_position[1] in range(0,int(self.y)-1) and direction == 2:
                flag = True
            elif self.agent_position[1] in range(1,int(self.y)) and direction == 3:
                flag = True
            else:
                flag = False
            if flag:
                screen.fill((255,255,255))
                self.draw(screen, 320, 240,False,False)
                pygame.display.update()
                if direction == 0:
                    move = [[movex,0] for movex in range(0,movement_length+3)]
                elif direction == 1:
                    move = [[-movex,0] for movex in range(0,movement_length+3)]
                elif direction == 2:
                    move = [[0,movey] for movey in range(0,movement_length+3)]
                elif direction == 3:
                    move = [[0,-movey] for movey in range(0,movement_length+3)]
                for i,j in move:
                    pygame.time.delay(50)
                    screen.fill((255,255,255))
                    self.draw(screen, 320, 240,False,False)
                    self.grid_comp_list[self.agent_index].draw(screen,x+i,y+j,draw_effects = False)
                    pygame.display.update()
                self.grid_comp_list[self.agent_index].content = 0
                if direction == 0:
                    self.agent_index += int(self.y)
                elif direction == 1:
                    self.agent_index -= int(self.y)
                elif direction == 2:
                    self.agent_index += 1
                elif direction == 3:
                    self.agent_index -= 1
                self.grid_comp_list[self.agent_index].content += 1
                self.agent_position = self.grid_comp_list[self.agent_index].position
            # print(flag)
            # print(self.agent_position)
            # print(x,y)

    def setup(self,screen,event):
        global fontH3
        flag = False
        msg_flag = False
        msg = ""
        options = setup_component()
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in self.grid_comp_list:
                j=self.grid_comp_list.index(i)
                if i.rect.collidepoint(event.pos):
                    screen.fill((255,255,255))
                    grid.draw(screen, 210, 225,show_button=False)
                    mask_surface = pygame.Surface((640,480))
                    mask_surface.fill((0,0,0))
                    mask_surface.set_alpha(50)
                    screen.blit(mask_surface, (0,0))
                    count_x,count_y = i.position
                    x = count_x*(self.size_x+2)+12
                    y = count_y*(self.size_y+2)+27
                    flag = i.draw(screen,x=x,y=y)
                    options.draw_options(screen)
                    self.selected_grid_comp = j
                    return
            if self.selected_grid_comp >= 0:
                temp = self.grid_comp_list[self.selected_grid_comp].content
                self.grid_comp_list[self.selected_grid_comp].content = options.option_select(event,self.grid_comp_list[self.selected_grid_comp].content)
                posx,posy = self.grid_comp_list[self.selected_grid_comp].position
                if self.grid_comp_list[self.selected_grid_comp].content >= 0:
                    if self.grid_comp_list[self.selected_grid_comp].content in range(10,19) :
                        self.grid_comp_list[self.selected_grid_comp].content %= 10
                        self.agent_present = False
                        self.agent_position = [-1,-1]
                    elif self.grid_comp_list[self.selected_grid_comp].content in range(20,29):
                        self.grid_comp_list[self.selected_grid_comp].content %= 10
                        self.gold_present = False
                    elif self.grid_comp_list[self.selected_grid_comp].content in range(30,39):
                        self.grid_comp_list[self.selected_grid_comp].content %= 10
                        for i in self.grid_comp_list:
                            test_posx,test_posy = i.position
                            if (test_posx == posx+1 or test_posx == posx-1) and test_posy == posy:
                                i.effect -= 1
                            elif (test_posy == posy+1 or test_posy == posy-1) and test_posx == posx:
                                i.effect -= 1
                    elif self.grid_comp_list[self.selected_grid_comp].content in range(40,49):
                        self.grid_comp_list[self.selected_grid_comp].content %= 10 
                        for i in self.grid_comp_list:
                            test_posx,test_posy = i.position
                            if (test_posx == posx+1 or test_posx == posx-1) and test_posy == posy:
                                i.effect -= 2
                            elif (test_posy == posy+1 or test_posy == posy-1) and test_posx == posx:
                                i.effect -= 2
                        self.wumpus_present = False
                    print(self.agent_position)
                    if self.grid_comp_list[self.selected_grid_comp].content == 1:
                        if self.agent_present:
                            self.grid_comp_list[self.selected_grid_comp].content = temp
                            msg = "More than one agent is not allowed."
                            msg_flag = True
                        else:
                            self.agent_present = True
                            self.agent_position = self.grid_comp_list[self.selected_grid_comp].position
                            self.agent_index = self.selected_grid_comp
                    if self.grid_comp_list[self.selected_grid_comp].content == 2:
                        if self.gold_present:
                            self.grid_comp_list[self.selected_grid_comp].content = temp 
                            if temp == 1:
                                self.agent_present = True
                            msg = "More than one gold is not allowed."
                            msg_flag = True
                        else:
                            self.gold_present = True
                    if self.grid_comp_list[self.selected_grid_comp].content == 3:
                        for i in self.grid_comp_list:
                            test_posx,test_posy = i.position
                            if (test_posx == posx+1 or test_posx == posx-1) and test_posy == posy:
                                if i.effect != 1:
                                    i.effect += 1
                            elif (test_posy == posy+1 or test_posy == posy-1) and test_posx == posx:
                                if i.effect != 1:
                                    i.effect += 1
                    if self.grid_comp_list[self.selected_grid_comp].content == 4:
                        if not self.wumpus_present:
                            for i in self.grid_comp_list:
                                test_posx,test_posy = i.position
                                if (test_posx == posx+1 or test_posx == posx-1) and test_posy == posy:
                                    i.effect += 2
                                elif (test_posy == posy+1 or test_posy == posy-1) and test_posx == posx:
                                    i.effect += 2
                            self.wumpus_present = True
                        else:
                            self.grid_comp_list[self.selected_grid_comp].content = temp
                            if temp == 1:
                                self.agent_present = True
                            if temp == 2:
                                self.gold_present = True
                            msg = "More than one Wumpus is not allowed."
                            msg_flag = True
                    
                    flag = True
                    self.selected_grid_comp = -1
            if flag:
                screen.fill((255,255,255))
                self.draw(screen, 320, 240)
                if msg_flag:
                    msg_surf = fontH3.render(msg, True, (0,0,0))
                    msg_rect = msg_surf.get_rect()
                    msg_rect.bottom = 475
                    msg_rect.centerx = 320
                    screen.blit(msg_surf,msg_rect)

    def pos_to_index(self,postion):
        return postion[0]*int(self.y)+postion[1]
    def index_to_pos(self,index):
        return ((index//int(self.y),index%int(self.y)))

class Search_Agent:
    def __init__(self,grid):
        self.safe_list = []
        self.traversed_list = set()
        self.effect_list = {}
        self.working_grid = grid
        self.finished_flag = False
        self.backtrack_flag = False
    def check_neighbours(self,grid_element=Grid_comp):
        self.effect_list[self.working_grid.pos_to_index(grid_element.position)]=grid_element.effect
        temp_list = []
        if 0 < grid_element.position[0] < int(self.working_grid.x):
            temp_list.append((grid_element.position[0]-1,grid_element.position[1]))
        if 0 <= grid_element.position[0] < int(self.working_grid.x)-1:
            temp_list.append((grid_element.position[0]+1,grid_element.position[1]))
        if 0 < grid_element.position[1] < int(self.working_grid.y):
            temp_list.append((grid_element.position[0],grid_element.position[1]-1))
        if 0 <= grid_element.position[1] < int(self.working_grid.y)-1:
            temp_list.append((grid_element.position[0],grid_element.position[1]+1))
        if grid_element.effect == 0:
            if 0 < grid_element.position[0] < int(self.working_grid.x):
                self.safe_list.append((grid_element.position[0]-1,grid_element.position[1]))
            if 0 <= grid_element.position[0] < int(self.working_grid.x)-1:
                self.safe_list.append((grid_element.position[0]+1,grid_element.position[1]))
            if 0 < grid_element.position[1] < int(self.working_grid.y):
                self.safe_list.append((grid_element.position[0],grid_element.position[1]-1))
            if 0 <= grid_element.position[1] < int(self.working_grid.y)-1:
                self.safe_list.append((grid_element.position[0],grid_element.position[1]+1))
        if grid_element.effect == 1 or grid_element.effect == 2:
            if 0 < grid_element.position[0] < int(self.working_grid.x) and 0 <= grid_element.position[1] < int(self.working_grid.y)-1 :
                print(self.working_grid.pos_to_index((grid_element.position[0]-1,grid_element.position[1]+1)))
                try:
                    if self.effect_list[self.working_grid.pos_to_index((grid_element.position[0]-1,grid_element.position[1]+1))] != grid_element.effect:
                        self.safe_list.append((grid_element.position[0]-1,grid_element.position[1]))
                        self.safe_list.append((grid_element.position[0],grid_element.position[1]+1))
                except:
                    pass
            if 0 < grid_element.position[0] < int(self.working_grid.x) and 0 < grid_element.position[1] < int(self.working_grid.y) :
                print(self.working_grid.pos_to_index((grid_element.position[0]-1,grid_element.position[1]+1)))
                try:
                    if self.effect_list[self.working_grid.pos_to_index((grid_element.position[0]-1,grid_element.position[1]-1))] != grid_element.effect:
                        self.safe_list.append((grid_element.position[0]-1,grid_element.position[1]))
                        self.safe_list.append((grid_element.position[0],grid_element.position[1]-1))
                except:
                    pass
            if 0 <= grid_element.position[0] < int(self.working_grid.x)-1 and 0 <= grid_element.position[1] < int(self.working_grid.y)-1 :
                print(self.working_grid.pos_to_index((grid_element.position[0]-1,grid_element.position[1]+1)))
                try:
                    if self.effect_list[self.working_grid.pos_to_index((grid_element.position[0]+1,grid_element.position[1]+1))] != grid_element.effect:
                        self.safe_list.append((grid_element.position[0]+1,grid_element.position[1]))
                        self.safe_list.append((grid_element.position[0],grid_element.position[1]+1))
                except:
                    pass
            if 0 <= grid_element.position[0] < int(self.working_grid.x)-1 and 0 < grid_element.position[1] < int(self.working_grid.y) :
                print(self.working_grid.pos_to_index((grid_element.position[0]+1,grid_element.position[1]-1)))
                try:
                    if self.effect_list[self.working_grid.pos_to_index((grid_element.position[0]-1,grid_element.position[1]+1))] != grid_element.effect:
                        self.safe_list.append((grid_element.position[0]+1,grid_element.position[1]))
                        self.safe_list.append((grid_element.position[0],grid_element.position[1]-1))
                except:
                    pass
        if grid_element.effect == 1 or grid_element.effect == 3:
            pass
        final_list=[value for value in temp_list if value in self.safe_list]
        print("Safe list:",self.safe_list)
        print("Effect list",self.effect_list)
        #print(final_list) 
        return final_list

    def move_to(self,screen,goal):
        # print("goal:",goal)
        # print("current:",self.working_grid.agent_position)
        if self.working_grid.agent_position[0]-1 == goal[0] and self.working_grid.agent_position[1] == goal[1]:
            direction = 1
        elif self.working_grid.agent_position[0]+1 == goal[0] and self.working_grid.agent_position[1] == goal[1]:
            direction = 0
        elif self.working_grid.agent_position[1]-1 == goal[1] and self.working_grid.agent_position[0] == goal[0]:
            direction = 3
        elif self.working_grid.agent_position[1]+1 == goal[1] and self.working_grid.agent_position[0] == goal[0]:
            direction = 2
        else:
            direction = -1
        self.working_grid.move(screen,direction)

    def search(self,screen,current_node,*next_depth_nodelist):
        self.traversed_list.add(current_node)
        temp_list = []
        print("Backtrack Flag:",self.backtrack_flag)
        if self.finished_flag:
            # print("flag")
            return
        else:
            #print("next node list:",next_depth_nodelist)
            if next_depth_nodelist:
                #print("list exist")
                for i in next_depth_nodelist:
                    #print("in ",i)
                    self.move_to(screen,current_node)
                    if i in self.traversed_list and not self.backtrack_flag:
                        temp_list.append(i)
                        continue
                    self.backtrack_flag = False
                    self.move_to(screen,i)
                    if self.working_grid.grid_comp_list[self.working_grid.agent_index].content == 3:
                        print("done")
                        self.finished_flag = True
                        return
                    check_list=self.check_neighbours(self.working_grid.grid_comp_list[self.working_grid.pos_to_index(i)])
                    # print("neibhours:",check_list)
                    # print("Agent pos:",self.working_grid.agent_position)
                    # print("current node:",current_node)
                    # print("Finish Flag:",self.finished_flag)
                    self.search(screen,self.working_grid.agent_position,*check_list)
                    if self.finished_flag:
                        return
                #else:
                self.backtrack_flag = True
                self.search(screen,self.working_grid.agent_position,*temp_list)
                print(not self.finished_flag)
                print("returning")
                return
            else:
                #print("no list")
                return

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
setup_flag = True
while setup_flag:
    for event in pygame.event.get(): 
        if event.type == pygame.MOUSEBUTTONDOWN:
            grid.setup(screen, event)
            setup_flag = grid.start_button.start_event(event,screen,grid.agent_present,grid.gold_present,grid.wumpus_present)
            pygame.display.flip()
        if event.type==pygame.QUIT:
            pygame.quit() 
            exit(0)
screen.fill((255,255,255))
grid.draw(screen,width//2,height//2,show_button=False)
pygame.display.flip()
Agent = Search_Agent(grid)
start_list = Agent.check_neighbours(grid.grid_comp_list[grid.agent_index])
print("Start list:",start_list)
grid.draw(screen,width//2,height//2,show_button=False)
pygame.display.flip()
Agent.search(screen,grid.agent_position,*start_list)
mask_surface = pygame.Surface((640,480))
mask_surface.fill((0,0,0))
mask_surface.set_alpha(50)
screen.blit(mask_surface, (0,0))
if Agent.finished_flag:
    msg = "Gold Found!!!"
else:
    msg = "Couldn't Find Gold"
msg_surf = fontH.render(msg, True, (0,0,0))
msg_rect = msg_surf.get_rect()
msg_rect.centery = height//2
msg_rect.centerx = width//2
screen.fill((127,127,127),msg_rect)
screen.blit(msg_surf,msg_rect)
pygame.display.flip()
while True:
    for event in pygame.event.get(): 
        if event.type==pygame.QUIT:
            pygame.quit() 
            exit(0)