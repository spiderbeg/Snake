#encoding: utf8
"""
创建每次启动游戏随机生成一个位置的蓝色方块
"""
import pygame
from pygame.locals import *
import random
pygame.init() # 初始化 pygame 各模块

edge = 20 # 格子大小
screenColor = 230,230,250 # 屏幕颜色淡紫色
width,height = 400,400 # 窗口尺寸，后面的例子中，我们格子、窗口屏幕都设置为正方形
screen = pygame.display.set_mode((width,height)) # 初始化一个窗口, 为 Surface 对象
pygame.display.set_caption('Snake') # 设置标题名

# 格子 
# surface 对象表示图片 rect对象 表示坐标，
grid = pygame.Surface((edge, edge)) # 创建一个 20 * 20 大小的 Surface 对象
gridColor = (0,0,255) # 蓝色
grid.fill(gridColor) # 格子 Surface 对象填充颜色
gr = grid.get_rect() # Rect 对象
gr.left, gr.top = random.randrange(0,width,edge),random.randrange(0,height,edge) # 在屏幕范围内产生随机坐标

going = True # 控制是否退出循环
clock = pygame.time.Clock()
while going:
    clock.tick(10) # 游戏帧率为 10，每秒刷新 10 次
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # 监听游戏退出
            going = False
    screen.fill(screenColor) # 添加屏幕颜色
    screen.blit(grid, gr) # 将格子画到 gr 的位置 
    pygame.display.flip() # 使我们刚刚画到屏幕上的 格子 可见
pygame.quit() # 退出游戏