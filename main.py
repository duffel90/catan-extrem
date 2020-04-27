import pygame as pg
from matplotlib import cm, colors
import numpy as np
from collections import OrderedDict
from sklearn.utils import shuffle
import random
import time

pg.init()
screen = pg.display.set_mode((1920, 1080))
COLOR_INACTIVE = pg.Color('gray')
COLOR_ACTIVE = pg.Color('red')
FONT = pg.font.Font(None, 32)
pg.display.set_caption("Siedler EXTREME")
players  = 12
fild_size_x = 14
# Load Images
backround = pg.image.load('fig/backround.png')
water = 'fig/wasser.png'
wood = 'fig/wood.png'
grain = 'fig/food.png'
brick = 'fig/brick.png'
sheep = 'fig/sheep.png'
rock = 'fig/rock.png'
desert = 'fig/desert.png'
gold = 'fig/gold.png'
unknown = 'fig/unknown.png'
img_chip = 'fig/chip.png'
img_couronne = 'fig/couronne.png'

wood_port = pg.image.load('fig/wood_port.png')
grain_port = pg.image.load('fig/grain_port.png')
brick_port = pg.image.load('fig/brick_port.png')
rock_port = pg.image.load('fig/rock_port.png')
sheep_port = pg.image.load('fig/sheep_port.png')
three_port = pg.image.load('fig/3_port.png')

img_bandit = pg.image.load('fig/bandit.png')
boat = pg.image.load('fig/boat.png')
img_city = pg.image.load('fig/city.png')
img_village = pg.image.load('fig/village.png')

cube1 = pg.image.load('fig/cube1.png')
cube2 = pg.image.load('fig/cube2.png')
cube3 = pg.image.load('fig/cube3.png')
cube4 = pg.image.load('fig/cube4.png')
cube5 = pg.image.load('fig/cube5.png')
cube6 = pg.image.load('fig/cube6.png')




class cube:
    def __init__(self,x,y,image):
        self.x = x
        self.y = y
        self.image = image
        self.radius = []

    def diec():
        nr = np.random.randint(0,6)
        if nr == 1 :
            self.image = cube1
        if nr == 2 :
            self.image = cube2
        if nr == 3 :
            self.image = cube3
        if nr == 4 :
            self.image = cube4
        if nr == 5 :
            self.image = cube5
        if nr == 6 :
            self.image = cube6

    def draw(self, screen):
            screen.blit(self.image,(self.x,self.y))

def init_cube():
    cubes = []
    cubes.append(cube(1700,900,cube1))
    cubes.append(cube(1750,910,cube1))
    return cubes


class bandit:
    def __init__(self,image):
        self.x = []
        self.y = []
        self.image = image
        self.radius = []
        self.status = False
        self.water = False
    def draw(self, screen):
        if self.status:
            if self.water:
                img,size_ =  convert_img(self.image,self.radius*0.6,self.radius*0.6, (0,0,0))
            else:
                img,size_ =  convert_img(self.image,self.radius*0.6,self.radius*0.9, (0,0,0))
            screen.blit(img,(self.x-size_[0]/2,self.y-size_[1]/2))



class city:
    def __init__(self,x,y,hex_radius,img_city,img_village):
        self.rect = self.rect = pg.Rect(x-hex_radius*0.15, y-hex_radius*0.15, hex_radius*0.3, hex_radius*0.3)
        self.x = x
        self.y = y
        self.radius = hex_radius
        self.color = (125,125,125,0)
        self.status = 'None' # 'city','village'
        self.img_city = img_city
        self.img_village = img_village
        
    def handle_event(self, event,input_boxes):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                for box in input_boxes:
                    if box.active:
                        self.color = box.color_fill
                if event.button ==3:
                    self.status = 'city'
                if event.button ==1:
                    self.status = 'village'
                if event.button ==2:
                    # Toggle the active variable.
                    self.status = 'None'
                    
    def draw(self, screen):
        if self.status == 'city':
            img,size_ =  convert_img(self.img_city,self.radius*0.6,self.radius*0.6, self.color)
            screen.blit(img,(self.x-size_[0]/2,self.y-size_[1]/2))
        if self.status == 'village':
            img,size_ =  convert_img(self.img_village,self.radius*0.6,self.radius*0.6, self.color)
            screen.blit(img,(self.x-size_[0]/2,self.y-size_[1]/2))

class street:
    def __init__(self,x,y,rot,hex_radius,image):
        self.rect = self.rect = pg.Rect(x-hex_radius*0.15, y-hex_radius*0.15, hex_radius*0.3, hex_radius*0.3)
        self.x = x
        self.y = y
        self.w = 4
        self.radius = hex_radius
        self.rot = np.deg2rad(rot)
        self.x1 = self.x - np.cos(self.rot)*(hex_radius/2*0.75)
        self.y1 = self.y - np.sin(self.rot)*(hex_radius/2*0.75+self.w/2)
        self.x2 = self.x + np.cos(self.rot)*(hex_radius/2*0.75)
        self.y2 = self.y + np.sin(self.rot)*(hex_radius/2*0.75+self.w/2)
        self.color = (125,125,125,0)
        self.status = 'None' # 'street','boat'
        self.active = False
        self.image = image
        
    def handle_event(self, event,input_boxes):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                for box in input_boxes:
                    if box.active:
                        self.color = box.color_fill
                if event.button ==1:
                    self.status = 'street'
                if event.button ==3:
                    self.status = 'boat'
                if event.button ==2:
                    # Toggle the active variable.
                    self.status = 'None'
    def draw(self, screen):
        if self.status == 'boat':
            img,size_ =  convert_img(self.image,self.radius*0.6,self.radius*0.6, self.color )
            screen.blit(img,(self.x-size_[0]/2,self.y-size_[1]/2))
        if self.status == 'street':
            pg.draw.line(screen, (0,0,0), (self.x1,self.y1), (self.x2,self.y2), self.w+6)
            pg.draw.line(screen, self.color, (self.x1,self.y1), (self.x2,self.y2), self.w+2)
#            screen.blit(screen, (self.x,self.y))

def init_port(input_terrains):
    ports = []
    hex_x_distanz = input_terrains[0].hex_x_distanz
    hex_radius = input_terrains[0].radius
    for i in range(0,3):
#        load_image_ = loadImage(three_port,hex_x_distanz,hex_radius*2, colorkey=None)
        ports.append(port(100,100,30,three_port))
#    load_image_ = loadImage(brick_port,hex_x_distanz,hex_radius*2, colorkey=None)
    ports.append(port(100,100,30,brick_port))
#    load_image_ = loadImage(wood_port,hex_x_distanz,hex_radius*2, colorkey=None)
    ports.append(port(100,100,30,wood_port))
#    load_image_ = loadImage(grain_port,hex_x_distanz,hex_radius*2, colorkey=None)
    ports.append(port(100,100,30,grain_port))
#    load_image_ = loadImage(rock_port,hex_x_distanz,hex_radius*2, colorkey=None)
    ports.append(port(100,100,30,rock_port))
#    load_image_ = loadImage(sheep_port,hex_x_distanz,hex_radius*2, colorkey=None)
    ports.append(port(100,100,30,sheep_port))
    
    ports = shuffle(ports)
    ports = shuffle(ports)

    k = np.linspace(19,36,len(ports))
    print(k)
    i = 0
    for j in k:
        ports[i].x= input_terrains[int(j)].x
        ports[i].y = input_terrains[int(j)].y
        ports[i].radius = input_terrains[int(j)].radius
        ports[i].hex_x_distanz = input_terrains[int(j)].hex_x_distanz
        ports[i].img_pos = (int(ports[i].x-(ports[i].hex_x_distanz/2)*0.97),int(ports[i].y-(ports[i].radius)*0.97))
        i = i+1
        
    return ports
        

            
class port:
    def __init__(self,x,y,rot,image):
        self.x = x
        self.y = y
        self.rot = np.deg2rad(rot)
        self.radius = []
        self.image = image
        self.color = (255,255,255)
        self.hex_x_distanz = []
        self.img_pos = []
                
    
    def draw(self, screen):
        img,size_ =  convert_img(self.image,self.radius*0.8,self.radius*0.8, self.color )
        screen.blit(img,(self.x-size_[0]/2,self.y-size_[1]/2))
#        screen.blit(self.image,self.img_pos)



class terrain:
    def __init__(self,x,y,hex_x_distanz,hex_radius,image,img_unknown,img_chip,chip_nr):
        self.rect = self.rect = pg.Rect(x-hex_radius*0.5, y-hex_radius*0.5, hex_radius, hex_radius)
        self.x=x
        self.y=y
        self.hex_x_distanz = hex_x_distanz
#        self.hex_y_distanz = hex_y_distanz
        self.radius = hex_radius
        self.chip = img_chip
        self.chip_nr = chip_nr
        self.water = False
        self.chip_pos = (int(self.x-self.radius*0.3),int(self.y-self.radius*0.3))
        
        self.image = image
        self.img_unknown = img_unknown
        self.img_pos = (int(self.x-(self.hex_x_distanz/2)*0.97),int(self.y-(self.radius)*0.97))
        self.text,self.rect_text = text_(self.x,self.y,self.chip_nr)
        self.status = False
    
    def handle_event(self, event,bandits):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if event.button ==1: # left mouse
                    print(event.pos)
                    self.status = True
                if event.button ==3: #right mouse
                    if self.status:
                        for bandit_i in bandits:
                            if bandit_i.water == self.water:
                                bandit_i.x = self.x
                                bandit_i.y = self.y
                                bandit_i.status = self.status
                                bandit_i.radius = self.radius

    def draw(self, screen):
        
        if self.status:
            if self.water:
                screen.blit(self.image,self.img_pos)
            else:
                screen.blit(self.image,self.img_pos)
                screen.blit(self.chip,self.chip_pos)
                screen.blit(self.text, self.rect_text.center)     
        else:
            screen.blit(self.img_unknown,self.img_pos)
        
class player_status():
    def __init__(self):
        self.status
        self.color

class InputBox:
    def __init__(self, x, y, w, h, text):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.COLOR_INACTIVE = COLOR_INACTIVE
        self.COLOR_ACTIVE = COLOR_ACTIVE
        self.color_fill = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, (0,0,0))
        self.active = False
        

    def handle_event(self, event,input_boxes):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                for box in input_boxes:
                    box.active = False
                    self.active = True
                # Toggle the active variable.
            # Change the current color of the input box.
            self.color = self.COLOR_ACTIVE if self.active else self.COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    if self.text[0] == '(' and self.text[-1] == ')':
                        input = self.text[1:-2]
                        input = input.split(',')
                        if len(input) == 3:
                            try:
                                c = self.color_fill
                                c[0] = int(input[0])
                                c[1] = int(input[1])
                                c[2] = int(input[2])
                                self.color_fill = c
                            except:
                                self.color_fill  = self.color_fill
                            
                        print(self.text)
#                    self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                    time.sleep(0.1)
                # Re-render the text.
                i = len(self.text)
                if i >13:
                    i = 11
                self.text = self.text[0:i]
                self.txt_surface = FONT.render(self.text, True, (0,0,0))

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        #self.rect.w = width

    def draw(self, screen):
        # Blit the rect.
        pg.draw.rect(screen, self.color_fill, self.rect)
        pg.draw.rect(screen, self.color, self.rect, 4)
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))

def text_(x,y,num):
    font = pg.font.Font('freesansbold.ttf', 24) 
    if num == 6 or num == 8:
        text = font.render(str(int(num)), True, (255 ,0,0)) 
    else:
        text = font.render(str(int(num)), True, (0 ,0,0)) 
    size_ = text.get_size()
    rect = text.get_rect()  
    rect.center = (x-int(size_[0]/2),y-int(size_[1]/2))
    return text,rect


def init_players():
    norm = colors.Normalize(vmin=0, vmax=players)
    rgba_color =cm.Paired(norm(range(0,players)),bytes=True)
    color_ = tuple(map(tuple, rgba_color))

    
    input_boxes = []
    for player in range(0,players):
        if player % 2:
            input_box = InputBox(1750, 100+70*(player-1)/2, 150,32,'Player '+str(player+1)) #1700
        else:
            input_box = InputBox(1590, 100+70*(player/2), 150, 32,'Player '+str(player+1))
        input_box.color_fill = color_[player]
        if input_box.color_fill[0]>210:
            input_box.COLOR_ACTIVE = (0,0,0)
        input_boxes.append(input_box)
    return input_boxes


def hex_mesh():
    #Berechnung der Matrix
    game_area_x = (20,1590-20)
    gamge_area_y = (20,1020-20)
    hex_x_distanz = int((game_area_x[1]-game_area_x[0])/(fild_size_x))
    hex_radius = hex_x_distanz/2/((3/4)**(1/2))
    hex_x_init = np.array(range(game_area_x[0]+hex_x_distanz,game_area_x[1]-hex_x_distanz,hex_x_distanz))
    hex_y_distanz = int(hex_radius*1.5)
    hex_y_init = np.array(range(int(gamge_area_y[0]+hex_radius),int(gamge_area_y[1]-hex_radius),hex_y_distanz))
    hex_pos_x,hex_pos_y = np.meshgrid(hex_x_init,hex_y_init,sparse=False, indexing='xy')
    hex_x = hex_pos_x
    for i in range(1,len(hex_x),2):
        hex_x[i] = (hex_x[i]+hex_x_distanz/2)
    hex_y = hex_pos_y
    hex_x = hex_x.reshape(1,len(hex_x)*len(hex_x[0])) 
    hex_y = hex_y.reshape(1,len(hex_y)*len(hex_y[0])) 
    hex_x = hex_x[0]
    hex_y = hex_y[0]
    return hex_x,hex_y,hex_radius, hex_x_distanz

def init_terrain():
    hex_x,hex_y,hex_radius, hex_x_distanz = hex_mesh()
    global id_list
    terrain_state, chip_nr ,id_list= init_nr()
    input_terrains = []
    img_unknown = loadImage(unknown,hex_x_distanz,hex_radius*2, colorkey=None)
    for j in range(0,len(hex_x)):
        t = id_list[j]
#        image = loadImage(unknown,hex_x_distanz,hex_radius*2, colorkey=None)
        if terrain_state[j] == 9:
            image = loadImage(desert,hex_x_distanz,hex_radius*2, colorkey=None)
        if terrain_state[j] == 0:
            image = loadImage(wood,hex_x_distanz,hex_radius*2, colorkey=None)
        if terrain_state[j] == 2:
            image = loadImage(grain,hex_x_distanz,hex_radius*2, colorkey=None)
        if terrain_state[j] == 6:
            image = loadImage(rock,hex_x_distanz,hex_radius*2, colorkey=None)
        if terrain_state[j] == 8:
            image = loadImage(sheep,hex_x_distanz,hex_radius*2, colorkey=None)
        if terrain_state[j] == 4:
            image = loadImage(brick,hex_x_distanz,hex_radius*2, colorkey=None)
        if terrain_state[j] == 10:
            image = loadImage(water,hex_x_distanz,hex_radius*2, colorkey=None)
        if terrain_state[j] == 12:
            image = loadImage(gold,hex_x_distanz,hex_radius*2, colorkey=None)
            
        img_chip_ = loadImage(img_chip,hex_radius*0.6,hex_radius*0.6, colorkey=None)
        input_terrain = terrain(hex_x[t],hex_y[t],hex_x_distanz,hex_radius,image,img_unknown,img_chip_,chip_nr[j])
        if terrain_state[j] == 10 or terrain_state[j] == 9:
            input_terrain.water = True
        if j <37:
            input_terrain.status = True
        input_terrains.append(input_terrain)
        
    return input_terrains
   


def street_mesh():
    hex_x,hex_y,hex_radius, hex_x_distanz  = hex_mesh()
    hex_edge_x = np.array([]) 
    hex_edge_y = np.array([]) 
    hex_edge_rot = np.array([]) 
    delta_y = hex_x_distanz/2*(3/4)**(1/2)
    for t in range(0,len(hex_x)):
        # x Vector
        hex_edge_x = np.append(hex_edge_x,hex_x[t]-hex_x_distanz/2)
        hex_edge_x = np.append(hex_edge_x,hex_x[t]-hex_x_distanz/4)
        hex_edge_x = np.append(hex_edge_x,hex_x[t]+hex_x_distanz/4)
        hex_edge_x = np.append(hex_edge_x,hex_x[t]+hex_x_distanz/2)
        hex_edge_x = np.append(hex_edge_x,hex_x[t]+hex_x_distanz/4)
        hex_edge_x = np.append(hex_edge_x,hex_x[t]-hex_x_distanz/4)
        # y Vector
        hex_edge_y = np.append(hex_edge_y,hex_y[t])      
        hex_edge_y = np.append(hex_edge_y,hex_y[t]+delta_y)  
        hex_edge_y = np.append(hex_edge_y,hex_y[t]+delta_y)  
        hex_edge_y = np.append(hex_edge_y,hex_y[t])  
        hex_edge_y = np.append(hex_edge_y,hex_y[t]-delta_y)  
        hex_edge_y = np.append(hex_edge_y,hex_y[t]-delta_y)  
        # Rotatoinsvektor
        hex_edge_rot = np.append(hex_edge_rot,90)
        hex_edge_rot = np.append(hex_edge_rot,30)
        hex_edge_rot = np.append(hex_edge_rot,-30)
        hex_edge_rot = np.append(hex_edge_rot,90)
        hex_edge_rot = np.append(hex_edge_rot,30)
        hex_edge_rot = np.append(hex_edge_rot,-30)
        
    return hex_edge_x,hex_edge_y,hex_edge_rot,hex_radius

def init_street():
    hex_edge_x,hex_edge_y,hex_edge_rot,hex_radius = street_mesh()
    input_streets = []
    for t in range(0,len(hex_edge_x)):
        input_street= street(hex_edge_x[t],hex_edge_y[t],hex_edge_rot[t],hex_radius,boat)
        input_streets.append(input_street)
    return input_streets

def city_mesh():
    hex_x,hex_y,hex_radius, hex_x_distanz  = hex_mesh()
    hex_node_x = np.array([]) 
    hex_node_y = np.array([]) 
    delta_y = hex_x_distanz/2*(3/4)**(1/2)
    for t in range(0,len(hex_x)):
        # x Vector
        hex_node_x = np.append(hex_node_x,hex_x[t]-hex_x_distanz/2)
        hex_node_x = np.append(hex_node_x,hex_x[t])
        hex_node_x = np.append(hex_node_x,hex_x[t]+hex_x_distanz/2)
        hex_node_x = np.append(hex_node_x,hex_x[t]+hex_x_distanz/2)
        hex_node_x = np.append(hex_node_x,hex_x[t])
        hex_node_x = np.append(hex_node_x,hex_x[t]-hex_x_distanz/2)
        # y Vector
        hex_node_y = np.append(hex_node_y,hex_y[t]+hex_radius/2)      
        hex_node_y = np.append(hex_node_y,hex_y[t]+hex_radius)  
        hex_node_y = np.append(hex_node_y,hex_y[t]+hex_radius/2)  
        hex_node_y = np.append(hex_node_y,hex_y[t]-hex_radius/2)
        hex_node_y = np.append(hex_node_y,hex_y[t]-hex_radius)  
        hex_node_y = np.append(hex_node_y,hex_y[t]-hex_radius/2)  
        
    return hex_node_x,hex_node_y,hex_radius

def init_city():
    hex_node_x,hex_node_y,hex_radius = city_mesh()
    input_citys = []
    for t in range(0,len(hex_node_x)):
        input_city= city(hex_node_x[t],hex_node_y[t],hex_radius,img_city,img_village)
        input_citys.append(input_city)
    return input_citys
     
def loadImage(filename,img_w,img_h, colorkey=None):
    img_w = int(img_w)
    img_h = int(img_h)
    # Pygame das Bild laden lassen.
    image = pg.image.load(filename)
    # Das Pixelformat der Surface an den Bildschirm (genauer: die screen-Surface) anpassen.
    # Dabei die passende Funktion verwenden, je nach dem, ob wir ein Bild mit Alpha-Kanal haben oder nicht.
    if image.get_alpha() is None:
        image = image.convert()
    else:
        image = image.convert_alpha()
    # Colorkey des Bildes setzen, falls nicht None.
    # Bei -1 den Pixel im Bild an Position (0, 0) als Colorkey verwenden.
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, pg.RLEACCEL)
    image = pg.transform.scale(image,(int(img_w*0.97),int(img_h*0.97)))
    return image

def convert_img(image,img_w,img_h ,color,colorkey=(255,255,255)):
    img_w = int(img_w)
    img_h = int(img_h)

    if image.get_alpha() is None:
        image = image.convert()
    else:
        image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, pg.RLEACCEL)
    image = pg.transform.scale(image,(int(img_w*0.95),int(img_h*0.95)))
    w, h = image.get_size()
    for x1 in range(w):
        for y1 in range(h):
            b = image.get_at((x1, y1))[0:4]
            if b[0] ==0 and b[1]==255 and b[2]==0:
                image.set_at((x1, y1), pg.Color(int(color[0]),int(color[1]),int(color[2]), b[3]))
    rect = image.get_rect()
    size_ = image.get_size()
    
    return image,size_


def find_nerest_ids(x,y,id):
        id_list = np.array(range(0,len(x)))
        error = ((x-x[id])**2+(y-y[id])**2)**(1/2)
        sort_list = np.argsort(error)
        id_list= id_list[sort_list]
        return id_list

def init_nr():
    x,y,hex_radius, hex_x_distanz = hex_mesh()
    
    id_rand_ = random.randrange(int(len(x)*0.4),int(len(x)*0.6))
    id_list = find_nerest_ids(x,y,id_rand_)
    id_list[0:18] = shuffle(id_list[0:18])
    id_list[0:18] = shuffle(id_list[0:18])
    id_list[39:-1] = shuffle(id_list[39:-1])
    id_list[39:-1] = shuffle(id_list[39:-1])
    nr_start = np.array([0,2,3,3,4,4,5,5,6,6,8,8,9,9,10,10,11,11,12])
#    nr_start = shuffle(nr_start)
#    nr_start = shuffle(nr_start)
    nr_start = np.append(nr_start,np.ones(18)*0)
    
    
    terrain_start = np.array([9, 0,0,0,0 , 2,2,2,2 , 4,4,4 , 6,6,6 , 8,8,8,8 ])
    terrain_start = np.append(terrain_start,np.ones(18)*10)
    len_rest = len(id_list)-len(terrain_start)
    # Terrain
    water_per = 50
    len_wood = int(len_rest*4/water_per)# 0
    len_grain= int(len_rest*4/water_per)# 2
    len_brick= int(len_rest*3/water_per)# 4
    len_stone= int(len_rest*4/water_per)# 6
    len_sheep= int(len_rest*4/water_per)# 8
    len_water= len_rest-len_wood-len_grain-len_brick-len_stone-len_sheep#10
    #gold 12
    
    terrain_end = np.array(np.ones(len_wood)*0)
    terrain_end = np.append(terrain_end,np.ones(len_grain)*2)
    terrain_end = np.append(terrain_end,np.ones(len_brick)*4)
    terrain_end = np.append(terrain_end,np.ones(len_stone)*6)
    terrain_end = np.append(terrain_end,np.ones(len_sheep)*8)
    terrain_end = np.append(terrain_end,np.ones(len_water)*10)
    terrain_out = terrain_start
    terrain_out = np.append(terrain_out,terrain_end)
    
    
    gold_id = np.random.randint(40,len(terrain_out)-len_water)
    terrain_out[gold_id] = 12
    
     
    len_rest = len(id_list)-len(nr_start)-len_water
    two = int(len_rest*1/18)
    three = int(len_rest*2/18)
    four = int(len_rest*2/18)
    fife = int(len_rest*2/18)
    six = int(len_rest*2/18)
    eight = int(len_rest*2/18)
    nine = int(len_rest*2/18)
    ten = int(len_rest*2/18)
    eleven = int(len_rest*1/18)
    twelf = len_rest-two-three-four-fife-six-eight-nine-ten-eleven
    
    chip_end = np.array(np.ones(two)*2)
    chip_end = np.append(chip_end,np.ones(three)*3) 
    chip_end = np.append(chip_end,np.ones(four)*4) 
    chip_end = np.append(chip_end,np.ones(fife)*5) 
    chip_end = np.append(chip_end,np.ones(six)*6) 
    chip_end = np.append(chip_end,np.ones(eight)*8) 
    chip_end = np.append(chip_end,np.ones(nine)*9) 
    chip_end = np.append(chip_end,np.ones(ten)*10) 
    chip_end = np.append(chip_end,np.ones(eleven)*11) 
    chip_end = np.append(chip_end,np.ones(twelf)*12) 
    chip_end = shuffle(chip_end)
    chip_end = shuffle(chip_end)
    chip_nr = nr_start
    chip_nr = np.append(chip_nr,chip_end)
    chip_nr = np.append(chip_nr,np.ones(len(id_list)-len(chip_nr)))
    

    return terrain_out, chip_nr, id_list


    
def init_nr2():
    x,y,hex_radius, hex_x_distanz = hex_mesh()
#    id_rand_ = np.random.randint(0,len(x))
    id_rand_ = random.randrange(int(len(x)*0.4),int(len(x)*0.6))
    id_list = find_nerest_ids(x,y,id_rand_)
    print((x[id_list]**2+y[id_list]**2)**(1/2))

    terrain_start = np.ones(len(x))
    terrain= np.ones(len(x)-39)
    terrain[0:round(len(terrain)*0.11)] = terrain[:round(len(terrain)*0.11)]*2 # wood
    terrain[round(len(terrain)*0.11):round(len(terrain)*0.22)] = terrain[round(len(terrain)*0.11):round(len(terrain)*0.22)]*3 # food
    terrain[round(len(terrain)*0.22):round(len(terrain)*0.303)] = terrain[round(len(terrain)*0.22):round(len(terrain)*0.303)]*4 # rock
    terrain[round(len(terrain)*0.303):round(len(terrain)*0.413)] = terrain[round(len(terrain)*0.303):round(len(terrain)*0.413)]*5 # sheep
    terrain[round(len(terrain)*0.413):round(len(terrain)*0.5)] = terrain[round(len(terrain)*0.413):round(len(terrain)*0.5)]*6 # brick
    terrain[round(len(terrain)*0.5):] = terrain[round(len(terrain)*0.5):]*7 # wasser
    terrain = shuffle(terrain)
    terrain = shuffle(terrain)
    terrain = shuffle(terrain)
    terrain_start[id_list[39:]]=terrain
    start = []
    start = [1,2,2,2,2,3,3,3,3,4,4,4,5,5,5,5,6,6,6]
    start=shuffle(start)
    start=shuffle(start)
    start=shuffle(start)
    terrain_start[id_list[0:19]] =start
    terrain_start[id_list[19:39]] = np.ones(20)*7
#    
    terrain=terrain_start
    terrain_state= np.zeros(len(terrain))
    terrain_state[0:39] = 1
    
    numstart= [2,12,3,3,4,4,5,5,6,6,8,8,9,9,10,10,10,11,11,0]
    numstart = shuffle(numstart)
    numstart = shuffle(numstart)
    numstart = shuffle(numstart)     
    

    
    numend= np.ones(len(terrain)-18)
    numend[0:round(len(numend)*0.055)] = numend[:round(len(numend)*0.055)]*2 # wood
    numend[round(len(numend)*0.055):round(len(numend)*0.11)] = numend[round(len(numend)*0.055):round(len(numend)*0.11)]*12 # 12
    numend[round(len(numend)*0.11):round(len(numend)*0.22)] = numend[round(len(numend)*0.11):round(len(numend)*0.22)]*3 # 3
    numend[round(len(numend)*0.22):round(len(numend)*0.33)] = numend[round(len(numend)*0.22):round(len(numend)*0.33)]*4 # 4
    numend[round(len(numend)*0.33):round(len(numend)*0.44)] = numend[round(len(numend)*0.33):round(len(numend)*0.44)]*5 # 5
    numend[round(len(numend)*0.44):round(len(numend)*0.55)] = numend[round(len(numend)*0.44):round(len(numend)*0.55)]*6 # 6
    numend[round(len(numend)*0.55):round(len(numend)*0.66)] = numend[round(len(numend)*0.55):round(len(numend)*0.66)]*8 # 8
    numend[round(len(numend)*0.66):round(len(numend)*0.77)] = numend[round(len(numend)*0.66):round(len(numend)*0.77)]*9 # 9
    numend[round(len(numend)*0.77):round(len(numend)*0.88)] = numend[round(len(numend)*0.77):round(len(numend)*0.88)]*10 # 10
    numend[round(len(numend)*0.88):round(len(numend)*1)] = numend[round(len(numend)*0.88):round(len(numend)*1)]*11 # 11

    numend = shuffle(numend)
    numend = shuffle(numend)
    numend = shuffle(numend)
    num = numstart
    num[39:] = numend
    return terrain, num, id_list

def init_bandit():
    list_bandits = []
    bandit_ = bandit(img_bandit)
    bandit.water = False
    list_bandits.append(bandit_)
    bandit_ = bandit(boat)
    bandit_.water = True
    list_bandits.append(bandit_)
    return list_bandits

def main():
    screen.fill((0, 0, 0))
    screen.blit(backround,(0, 0))
    clock = pg.time.Clock()
    input_boxes = init_players()
    input_terrains = init_terrain()
    input_streets = init_street()
    input_citys = init_city()
    input_bandit = init_bandit()
    input_port= init_port(input_terrains)
#    input_cubes = init_cube()
    done = False

    while not done:
        screen.blit(backround,(0, 0))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            for box in input_boxes:
                box.handle_event(event,input_boxes)
            for terr in input_terrains:
                terr.handle_event(event,input_bandit)
            for street_i in input_streets:
                street_i.handle_event(event,input_boxes)
            for city_i in input_citys :
                city_i.handle_event(event,input_boxes)

        #for box in input_boxes:
            #box.update()
        for terr in input_terrains:
            terr.draw(screen)
        for street_i in input_streets :
            street_i.draw(screen)
        for city_i in input_citys :
            city_i.draw(screen)
        
        for box in input_boxes:
            box.draw(screen)
        for bandit_i in input_bandit:
            bandit_i.draw(screen)
        for port_i in input_port:
            port_i.draw(screen)
#        for cube_i in input_cubes:
#            cube_i.draw(screen)            
        
        
        pg.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    main()
    pg.quit()