# encoding: utf8
"""实现画格子线的功能"""
import pygame
from pygame.locals import *
import random
pygame.init()

edge = 20 # 格子大小
screenColor = 0, 0, 0 # 黑色
width,height = 400,400 # 窗口尺寸，后面的例子中，我们格子、窗口屏幕都设置为正方形
screen = pygame.display.set_mode((width,height)) # 初始化一个窗口, 为 Surface 对象
pygame.display.set_caption('Snake') # 设置标题名

screen.fill(screenColor) # 添加屏幕颜色，覆盖之前格子留下的印记。

def drawGrid(surface,edge,width):
    """根据间隔和屏幕大小画全屏幕格子
    surface: screen 
    """
    rows = width // edge
    sizeBtwn = edge
    x,y = 0,0
    for i in range(rows):
        x += sizeBtwn
        y += sizeBtwn
        pygame.draw.line(surface,(219,112,147),(x,0),(x,width)) # (219,112,147) 表示线条颜色
        pygame.draw.line(surface, (219,112,147),(0,y),(width,y))

drawGrid(screen,edge,width)
going = True # 控制是否退出循环
clock = pygame.time.Clock()
while going:
    clock.tick(10) # 游戏帧率为 10
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            going = False
    pygame.display.flip() # 使我们刚刚画到屏幕上的 格子 可见
pygame.quit() # 退出游戏