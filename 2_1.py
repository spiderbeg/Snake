# encoding: utf8
"""
创建类实现蛇的移动
"""
import pygame
from pygame.locals import *

# 游戏对象的类 surface:表示图片 rect: 坐标属性，
class SnakeNibble:
    """移动蛇，当蛇吃果子时，身体会变大，撞墙或者撞到自己时游戏结束"""
    def __init__(self,width=400,edge=20):
        self.width = self.height = 400 # 屏幕尺寸
        self.edge = edge # 身体边长
        self.ball = pygame.Surface((edge, edge)) # Surface对象

    def makeSnake(self):
        '''创建蛇 初始方向 右'''
        self.ball.fill((220,20,60)) # 红色
        ballrect = self.ball.get_rect() # 获取 rect 对象
        a = self.edge * 5
        snake = []
        for _ in range(3):
            ballrect2 = ballrect.copy() 
            ballrect2.left += a
            ballrect2.top = 100
            a -= self.edge
            snake.append(ballrect2)
        return snake

    def move(self,snake,direct):
        """按照方向移动 并返回更新之前 snake 的尾巴"""
        for i in range(len(snake)):
            if i==0: # 每次只更新队列第一个的方向，其他方向照旧
                rect = snake[0].copy()
                temp = self._get_nextRect(rect,direct)
        snake.insert(0,temp) # 加入头部的新位置
        endPop = snake.pop() # 删除末尾
        return endPop

    def _get_nextRect(self,rect,direct):
        """蛇 获取头部的新位置"""
        if direct == 0: rect.top += self.edge # 向下
        elif direct == 1: rect.top -= self.edge # 向上
        elif direct == 2: rect.left += self.edge # 向右
        elif direct == 3: rect.left -= self.edge # 向左
        return rect


def main():
    """初始化并在循环中运行直到有返回"""
    # 初始化
    pygame.init()
    direct = 2 # 速度
    oldDirect = direct # 有效速度
    edge = 20 # 格子大小
    width,height = 400,400 # 使用正方形
    screen = pygame.display.set_mode((width,height)) # 初始化一个窗口
    pygame.display.set_caption('Snake')

    # 对象准备
    # 蛇
    s = SnakeNibble(width,edge) # 身体尺寸=格子尺寸
    snake = s.makeSnake() # 创建蛇 生成 rect 序列
    grid = pygame.Surface((edge,edge)) 

    c = 0 # 计数
    dt = 0 # 计时
    going = True # 状态
    endPop = None # snake 尾巴
    runSpeed = 300 # 每 runSpeed 毫秒移动 10 个像素位置。游戏速率越小游戏运行越快
    clock = pygame.time.Clock() # 创建帮助记录时间的对象
    while going:
        lastt = clock.tick(60) # 帧率 60
        dt += lastt # 控制显示效果
        c += 1
        print('循环次数 %d, 前一次的时间 %d，目前总时间 %d 单位毫秒'%(c,lastt,dt)) # 游戏帧率
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                going = False
            elif event.type == KEYDOWN:
                if event.key == K_UP and oldDirect != 0: direct = 1 # 按了向上 1 并且当前方向不是向下 0 ，则向上
                elif event.key == K_DOWN and oldDirect != 1: direct = 0  # 向上 1 ，向下 0
                elif event.key == K_LEFT and oldDirect != 2: direct = 3  # 向左 3， 向右 2
                elif event.key == K_RIGHT and oldDirect != 3: direct = 2 
                elif event.key == K_0:
                    going = False # 退出或重新开始游戏

        if dt > runSpeed: # 控制速度，每过 runSpeed 毫秒，开始运动
            oldDirect = direct
            dt = 0 # 初始化时间
            endPop = s.move(snake,direct)
            screen.blit(grid, endPop) # 画格子 
        else:
            for i in range(len(snake)):
                screen.blit(s.ball, snake[i])
        pygame.display.flip() # 显示图形
    pygame.quit() # 退出游戏
    
if __name__ == '__main__':
    main()