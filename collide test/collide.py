import pygame
from pygame import *
pygame.init()

m1 = float(input("请输入第一个物体的质量(kg): "))
v1 = float(input("请输入第一个物体的初速度(m/s): "))
m2 = float(input("请输入第二个物体的质量(kg): "))
v2 = float(input("请输入第二个物体的初速度(m/s): "))

screen_size = [800, 600]
screen = pygame.display.set_mode(screen_size)

clock = pygame.time.Clock()
running = True


class Block(object):
    def __init__(self, image, mass, speed, init_position):
        global screen
        self.mass = mass[0]
        self.speed = speed[0]
        self.init_position = init_position
        self.the_image = pygame.image.load(image)
        self.the_image_rect = self.the_image.get_rect()
        self.the_image_rect[0] = self.init_position[0]
        self.the_image_rect[1] = screen_size[1]-self.the_image_rect[3]-self.init_position[1]

    def run(self):
        self.init_position[0] += self.speed
        self.the_image_rect[0] = self.init_position[0]
        self.the_image_rect[1] = screen_size[1]-self.the_image_rect[3]-self.init_position[1]

        if self.the_image_rect[0] <= 0:
            self.speed = -self.speed
            self.init_position[0] = 1
        elif self.the_image_rect[0] >= screen_size[0]-self.the_image_rect[2]:
            self.speed = -self.speed
            self.init_position[0] = screen_size[0]-self.the_image_rect[2]-1

        screen.blit(self.the_image, self.the_image_rect)


def collide(object1, object2):
    if pygame.Rect.colliderect(object1.the_image_rect, object2.the_image_rect):
        object1.speed_after = (object1.mass-object2.mass)/(object1.mass+object2.mass)*object1.speed + \
            2*object2.mass/(object1.mass+object2.mass)*object2.speed
        object2.speed_after = (object2.mass-object1.mass)/(object1.mass+object2.mass)*object2.speed + \
            2*object1.mass/(object1.mass+object2.mass)*object1.speed
        object1.speed = object1.speed_after
        object2.speed = object2.speed_after

    print(object1.speed, object2.speed)


block1 = Block(image='block.png', mass=[m1], speed=[v1], init_position=[-30,0])
block2 = Block(image='block.png', mass=[m2], speed=[v2], init_position=[400,0])

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