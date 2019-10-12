# encoding: utf8
"""
使用方向键控制格子移动
"""
import pygame
from pygame.locals import *
import random
pygame.init()

edge = 20 # 格子大小
screenColor = 0, 0, 0 # 黑色
width,height = 400,400 # 窗口尺寸，后面的例子中，我们格子、窗口屏幕都设置为正方形
screen = pygame.display.set_mode((width,height)) # 初始化一个窗口, 为 Surface 对象
pygame.display.set_caption('Snake') # 设置标题名


# 格子 
# surface 对象表示图片 rect对象 表示坐标，
grid = pygame.Surface((edge, edge)) # 创建一个 20 * 20 大小的 Surface 对象
gridColor = (0,0,255) # 蓝色
grid.fill(gridColor) # 格子 Surface 对象填充颜色
gr = grid.get_rect() # Rect 对象
gr.left, gr.top = random.randrange(10,width,10),random.randrange(10,height,10) # 在屏幕范围内产生随机坐标

def get_nextRect(rect,direct,sWidth):
    """根据方向移动格子
    ：param rect：格子的坐标对象；
    ：param swidth：每次移动的距离
    ：param direct：方向
    ：return rect：返回新的坐标对象
    """
    if direct == 0: # 向下
        rect.top += sWidth
    elif direct == 1: # 向上
        rect.top -= sWidth
    elif direct == 2: # 向右
        rect.left += sWidth
    elif direct == 3: # 向左
        rect.left -= sWidth
    return rect

direct  = 2 # 默认方向向右
going = True # 控制是否退出循环
clock = pygame.time.Clock()
while going:
    clock.tick(10) # 游戏帧率为 10
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            going = False
        elif event.type == KEYDOWN:
            if event.key == K_UP and direct != 0:direct = 1 # 按了向上 1 并且当前方向不是向下 0 ，则向上
            elif event.key == K_DOWN and direct != 1:direct = 0 # 向上 1 ，向下 0
            elif event.key == K_LEFT and direct != 2:direct = 3 # 向左 3， 向右 2
            elif event.key == K_RIGHT and direct != 3:direct = 2 
            elif event.key == K_0:
                    going = False # 退出游戏
    # 判断是否出界
    if gr.left < 0: direct = 2
    if gr.right > width: direct = 3
    if gr.top < 0: direct = 0
    if gr.bottom > height: direct = 1 
    screen.fill(screenColor) # 添加屏幕颜色，覆盖之前格子留下的印记。
    gr = get_nextRect(gr,direct,edge) # 生成新的坐标位置
    screen.blit(grid, gr) # 将格子画到 gr 的位置 
    pygame.display.flip() # 使我们刚刚画到屏幕上的 格子 可见
pygame.quit() # 退出游戏