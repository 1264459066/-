import pygame
from pygame import *
pygame.init()

m1 = float(input("请输入第一个物体的质量(kg): "))
v1 = float(input("请输入第一个物体的初速度(m/s): "))
m2 = float(input("请输入第二个物体的质量(kg): "))
v2 = float(input("请输入第二个物体的初速度(m/s): "))

screen_size = [800, 600]
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("碰撞模拟器")

clock = pygame.time.Clock()
running = True

class Block(object):
    def __init__(self, image, mass, velocity, init_position):
        global screen
        self.mass = mass[0]
        self.speed = velocity[0]
        self.init_position = init_position
        self.the_image = pygame.image.load(image)
        self.the_image_rect = self.the_image.get_rect()

        #初始化大小、位置
        img_size = self.the_image_rect[2]+10*self.mass
        self.the_img = pygame.transform.smoothscale(self.the_image, (img_size, img_size))
        self.the_img_rect = self.the_img.get_rect()
        self.the_img_rect[0] = self.init_position[0]
        self.the_img_rect[1] = screen_size[1]-self.the_img_rect[3]-self.init_position[1]
        

    def run(self):
        self.init_position[0] += self.speed
        self.the_img_rect[0] = self.init_position[0]
        self.the_img_rect[1] = screen_size[1]-self.the_img_rect[3]-self.init_position[1]

        if self.the_img_rect[0] < 0:
            self.speed = -self.speed
            #防止卡墙
            self.init_position[0] = 0
        elif self.the_img_rect[0] > screen_size[0]-self.the_img_rect[2]:
            self.speed = -self.speed
            #防止卡墙
            self.init_position[0] = screen_size[0]-self.the_img_rect[2]

        screen.blit(self.the_img, self.the_img_rect)


def collide(object1, object2):
    if pygame.Rect.colliderect(object1.the_img_rect, object2.the_img_rect):
        #以下是弹性碰撞速度变化公式
        object1.speed_after = (object1.mass-object2.mass)/(object1.mass+object2.mass)*object1.speed + \
            2*object2.mass/(object1.mass+object2.mass)*object2.speed
        object2.speed_after = (object2.mass-object1.mass)/(object1.mass+object2.mass)*object2.speed + \
            2*object1.mass/(object1.mass+object2.mass)*object1.speed
        
        #防止卡在一起
        object1.init_position[0] = object2.init_position[0]-object1.the_img_rect[2]
        object2.init_position[0] = object1.init_position[0]+object1.the_img_rect[2]
        
        object1.speed = object1.speed_after
        object2.speed = object2.speed_after


block1 = Block(image='block.png', mass=[m1], velocity=[v1], init_position=[-30,0])
block2 = Block(image='block.png', mass=[m2], velocity=[v2], init_position=[400,0])

while running:
    screen.fill('black')

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    key_list = pygame.key.get_pressed()
    if key_list[K_q] and key_list[K_u]:
        running = False

    block1.run()
    block2.run()
    collide(object1=block1, object2=block2)

    pygame.display.flip()
    clock.tick(60)
